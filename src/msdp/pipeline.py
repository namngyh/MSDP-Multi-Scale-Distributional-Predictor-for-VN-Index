from __future__ import annotations
import copy,json,time
from pathlib import Path
import joblib,numpy as np,pandas as pd,torch,yaml
from sklearn.metrics import brier_score_loss
from .bootstrap import moving_block_ci
from .calibration import StaticCQRCalibrator
from .config import load_config
from .data_io import load_market_data
from .data_quality import assess_quality,save_quality
from .dataset import SequenceDataset
from .features import build_features,select_features_on_development
from .interpretation import confidence_score,interpret
from .metrics import evaluate_arrays,interval_metrics
from .models import MSDP,ZeroReturnBaseline,RidgeDirectBaseline
from .plotting import generate_research_figures
from .reporting import generate_report
from .reproducibility import metadata,save_metadata,set_global_seed
from .scaling import TargetScalerSet,fit_feature_scaler
from .splits import chronological_split,expanding_folds
from .targets import build_targets
from .training.ensemble import average_predictions
from .training.trainer import train_model,predict
from .training.tuning import run_optuna

def _columns(hs): return [f"return_h{h}" for h in hs]+[f"direction_h{h}" for h in hs]+[f"mdd_h{h}" for h in hs]+[f"volatility_h{h}" for h in hs]
def _model_args(cfg,n_features,range_ix,params=None,ablation="full"):
    p={**cfg["model"],**(params or {})}; allowed={k:p[k] for k in ["hidden_dim","latent_dim","n_blocks","dropout","gate_temperature","medium_pool","long_pool"]}
    return {"n_features":n_features,"horizons":cfg["horizons"],"return_quantiles":cfg["quantiles"],"mdd_quantiles":cfg["mdd_quantiles"],**allowed,"range_indices":range_ix,"ablation":ablation}
def _datasets(raw_x,raw_y,train_ix,val_ix,lookback,hs):
    fsc=fit_feature_scaler(raw_x.iloc[train_ix]); tsc=TargetScalerSet(hs).fit(raw_y.iloc[train_ix],indices=train_ix); x=fsc.transform(raw_x); y=tsc.transform_frame(raw_y); cols=_columns(hs)
    return SequenceDataset(x,y,train_ix,lookback,cols),SequenceDataset(x,y,val_ix,lookback,cols),fsc,tsc,x,y
def _inverse(tsc,p): return tsc.inverse_predictions(p)

def run(config_path,data_path,root="."):
    started=time.time(); root=Path(root); cfg=load_config(config_path); hs=cfg["horizons"]; set_global_seed(cfg["seed"],cfg["deterministic"])
    df=load_market_data(data_path); market=df.copy(); quality=assess_quality(df); save_quality(quality,root/"reports/tables/data_quality.json")
    all_features,all_meta=build_features(df); targets=build_targets(df,hs); max_lb=int(all_meta.lookback.max()); valid=(np.arange(len(df))>=max_lb-1)&targets[_columns(hs)].notna().all(axis=1)
    df=df.loc[valid].reset_index(drop=True); raw_x=all_features.loc[valid].reset_index(drop=True); raw_y=targets.loc[valid].reset_index(drop=True)
    spc=cfg["split"]; splits=chronological_split(len(df),cfg["purge_gap"],spc["development"],spc["calibration"],(spc["min_development"],spc["min_calibration"],spc["min_test"]))
    raw_x,meta,_=select_features_on_development(raw_x,all_meta,splits["development"],max_missing=1-cfg["min_feature_nonmissing"])
    finite=raw_x.notna().all(axis=1)
    if not finite.all():
        # Unexpected missing observations are removed, never imputed or forward-filled.
        keep=np.flatnonzero(finite); mapping={old:new for new,old in enumerate(keep)}; df=df.iloc[keep].reset_index(drop=True); raw_x=raw_x.iloc[keep].reset_index(drop=True); raw_y=raw_y.iloc[keep].reset_index(drop=True)
        splits=chronological_split(len(df),cfg["purge_gap"],spc["development"],spc["calibration"],(spc["min_development"],spc["min_calibration"],spc["min_test"]))
    meta.to_csv(root/"data/processed/feature_metadata.csv",index=False); pd.concat([df[["date","close"]],raw_x,raw_y],axis=1).to_csv(root/"data/processed/model_frame.csv",index=False)
    tags=meta.set_index("name").expert_tags; range_ix=[i for i,n in enumerate(raw_x.columns) if "range_volatility" in tags[n].split("|")]
    folds=expanding_folds(splits["development"],cfg["training"]["folds"],252,cfg["purge_gap"])
    tuning_cfg=copy.deepcopy(cfg); tuning_cfg["training"]["epochs"]=cfg["training"].get("tuning_epochs",cfg["training"]["epochs"])
    def objective(trial):
        params={"hidden_dim":trial.suggest_categorical("hidden_dim",[32,64,96]),"latent_dim":trial.suggest_categorical("latent_dim",[32,48,64]),"n_blocks":trial.suggest_categorical("n_blocks",[2,3]),"dropout":trial.suggest_float("dropout",.05,.25),"gate_temperature":trial.suggest_categorical("gate_temperature",[.7,1.,1.3]),"medium_pool":trial.suggest_categorical("medium_pool",[3,5]),"long_pool":trial.suggest_categorical("long_pool",[10,20]),"learning_rate":trial.suggest_float("learning_rate",1e-4,3e-3,log=True),"weight_decay":trial.suggest_float("weight_decay",1e-6,1e-3,log=True),"batch_size":trial.suggest_categorical("batch_size",[32,64,128])}
        scores=[]
        for fold,(tr,va) in enumerate(folds):
            local=copy.deepcopy(tuning_cfg); local["training"].update({k:params[k] for k in ("learning_rate","weight_decay","batch_size")}); trds,vads,_,_,_,_=_datasets(raw_x,raw_y,tr,va,cfg["lookback"],hs); set_global_seed(cfg["seed"]+fold,cfg["deterministic"]); model=MSDP(**_model_args(cfg,len(raw_x.columns),range_ix,params)); _,history=train_model(model,trds,vads,local,cfg["device"],trial); scores.append(min(r["validation_total"] for r in history))
        return float(np.mean(scores))
    best,study=run_optuna(objective,cfg,root/"artifacts/tuning"); train_over={k:best[k] for k in ("learning_rate","weight_decay","batch_size") if k in best}; final_cfg=copy.deepcopy(cfg); final_cfg["training"].update(train_over)
    dev=splits["development"]; val_size=min(252,max(50,len(dev)//8)); tr=dev[:-(val_size+cfg["purge_gap"])]; va=dev[-val_size:]
    # Final scalers use development only; calibration/test remain unseen.
    fsc=fit_feature_scaler(raw_x.iloc[dev]); tsc=TargetScalerSet(hs).fit(raw_y.iloc[dev],indices=dev); xs=fsc.transform(raw_x); ys=tsc.transform_frame(raw_y); cols=_columns(hs)
    joblib.dump(fsc,root/"artifacts/scalers/feature_scaler.joblib"); joblib.dump(tsc.return_scalers,root/"artifacts/scalers/return_scalers.joblib"); joblib.dump(tsc.mdd_scalers,root/"artifacts/scalers/mdd_scalers.joblib"); joblib.dump(tsc.volatility_scalers,root/"artifacts/scalers/volatility_scalers.joblib"); joblib.dump(tsc,root/"artifacts/scalers/target_scalers.joblib")
    (root/"artifacts/scalers/scaler_metadata.json").write_text(json.dumps({"fit_partition":"development","fit_indices":[int(dev[0]),int(dev[-1])],"fit_dates":[str(df.date.iloc[dev[0]]),str(df.date.iloc[dev[-1]])],"feature_order":list(raw_x.columns),"target_transform":{"return":"independent RobustScaler","mdd":"negative severity, scale-only RobustScaler","volatility":"log1p then RobustScaler"}},indent=2),encoding="utf-8")
    calds=SequenceDataset(xs,ys,splits["calibration"],cfg["lookback"],cols); testds=SequenceDataset(xs,ys,splits["test"],cfg["lookback"],cols); seed_cal=[]; seed_test=[]; seed_results=[]; seed_states=[]; model_args=_model_args(cfg,len(raw_x.columns),range_ix,best)
    for seed in cfg["seeds"]:
        set_global_seed(seed,cfg["deterministic"]); trds=SequenceDataset(xs,ys,tr,cfg["lookback"],cols); vads=SequenceDataset(xs,ys,va,cfg["lookback"],cols); model=MSDP(**model_args); model,history=train_model(model,trds,vads,final_cfg,cfg["device"]); cp,cix=predict(model,calds,device=cfg["device"]); tp,tix=predict(model,testds,device=cfg["device"]); cp=_inverse(tsc,cp); tp=_inverse(tsc,tp); seed_cal.append(cp); seed_test.append(tp); seed_states.append({k:v.detach().cpu() for k,v in model.state_dict().items()}); seed_results.append({"seed":seed,"best_epoch":int(np.argmin([r["validation_total"] for r in history])+1),"best_validation_loss":float(min(r["validation_total"] for r in history))}); pd.DataFrame(history).to_csv(root/f"artifacts/models/training_history_seed_{seed}.csv",index=False); torch.save({"state_dict":model.state_dict(),"model_args":model_args,"seed":seed},root/f"artifacts/models/evaluation_seed_{seed}.pt")
    cp=average_predictions(seed_cal); tp=average_predictions(seed_test); Path(root/"reports/tables/seed_results.json").write_text(json.dumps(seed_results,indent=2),encoding="utf-8")
    yret=raw_y.loc[tix,[f"return_h{h}" for h in hs]].to_numpy(); ydir=raw_y.loc[tix,[f"direction_h{h}" for h in hs]].to_numpy(); ymdd=raw_y.loc[tix,[f"mdd_h{h}" for h in hs]].to_numpy(); yvol=raw_y.loc[tix,[f"volatility_h{h}" for h in hs]].to_numpy(); calret=raw_y.loc[cix,[f"return_h{h}" for h in hs]].to_numpy()
    calibrator=StaticCQRCalibrator(1-cfg["target_coverage"]).fit(cp["return_quantiles"][:,:,0],cp["return_quantiles"][:,:,-1],calret,df.date.iloc[cix].tolist()); lo,hi=calibrator.transform(tp["return_quantiles"][:,:,0],tp["return_quantiles"][:,:,-1]); (root/"artifacts/calibration").mkdir(parents=True,exist_ok=True); (root/"artifacts/calibration/conformal.json").write_text(json.dumps(calibrator.state_dict(),indent=2),encoding="utf-8")
    metrics=evaluate_arrays(yret,ymdd,yvol,ydir,tp,cfg["quantiles"],cfg["mdd_quantiles"]); baseline_metrics={}; bootstrap={}
    devret=raw_y.loc[dev,[f"return_h{h}" for h in hs]].to_numpy(); base=ZeroReturnBaseline().fit(devret,cfg["quantiles"]); bq,bp=base.predict(len(tix))
    for j,h in enumerate(hs):
        metrics[f"h{h}"]["calibrated_interval"]=interval_metrics(yret[:,j],lo[:,j],hi[:,j],1-cfg["target_coverage"]); baseline_metrics[f"h{h}"]={"return_mae":float(np.mean(abs(yret[:,j]))),"return_pinball":float(np.mean(np.maximum(np.asarray(cfg["quantiles"])*(yret[:,j,None]-bq[:,j]),(np.asarray(cfg["quantiles"])-1)*(yret[:,j,None]-bq[:,j])))),"brier":float(np.mean((ydir[:,j]-bp[:,j])**2))}; model_abs=abs(yret[:,j]-tp["return_quantiles"][:,j,2]); base_abs=abs(yret[:,j]); bootstrap[f"h{h}_mae_difference_ci95"]=moving_block_ci(model_abs,base_abs,np.mean,cfg["bootstrap_resamples"],max(20,h)); metrics[f"h{h}"]["vs_zero_baseline"]={k:metrics[f"h{h}"][k]-baseline_metrics[f"h{h}"][k] for k in ("return_mae","return_pinball","brier")}
    # Cheap but real ablations on the same split; quick config controls which variants run.
    ablation_results=[]
    for ablation in cfg.get("ablations",[]):
        set_global_seed(cfg["seed"],cfg["deterministic"]); model=MSDP(**_model_args(cfg,len(raw_x.columns),range_ix,best,ablation)); model,hist=train_model(model,SequenceDataset(xs,ys,tr,cfg["lookback"],cols),SequenceDataset(xs,ys,va,cfg["lookback"],cols),final_cfg,cfg["device"]); ap,_=predict(model,testds,device=cfg["device"]); ap=_inverse(tsc,ap); ablation_results.append({"name":ablation,"return_pinball_mean":float(np.mean([evaluate_arrays(yret,ymdd,yvol,ydir,ap,cfg["quantiles"],cfg["mdd_quantiles"])[f'h{h}']["return_pinball"] for h in hs]))})
    rows={"date":df.loc[tix,"date"].to_numpy(),"current_close":df.loc[tix,"close"].to_numpy()}
    for j,h in enumerate(hs):
        for qi,q in enumerate([5,25,50,75,95]): rows[f"return_q{q:02d}_h{h}"]=tp["return_quantiles"][:,j,qi]
        rows.update({f"return_lower90_raw_h{h}":tp["return_quantiles"][:,j,0],f"return_upper90_raw_h{h}":tp["return_quantiles"][:,j,-1],f"return_lower90_calibrated_h{h}":lo[:,j],f"return_upper90_calibrated_h{h}":hi[:,j],f"direction_probability_h{h}":tp["direction_prob"][:,j],f"actual_return_h{h}":yret[:,j],f"actual_direction_h{h}":ydir[:,j],f"actual_mdd_h{h}":ymdd[:,j],f"predicted_volatility_h{h}":tp["volatility"][:,j],f"actual_volatility_h{h}":yvol[:,j],f"expert_disagreement_h{h}":tp["expert_disagreement"][:,j]})
        for qi,q in enumerate([10,50,90]): rows[f"mdd_q{q:02d}_h{h}"]=tp["mdd_quantiles"][:,j,qi]
        for k,name in enumerate(["short","medium","long","range_vol"][:tp["gate_weights"].shape[-1]]): rows[f"gate_{name}_h{h}"]=tp["gate_weights"][:,j,k]; rows[f"expert_{name}_return_h{h}"]=tp["aux_return_median"][:,j,k]
    pred=pd.DataFrame(rows); pred.to_csv(root/"artifacts/predictions/test_predictions.csv",index=False)
    latest_features=all_features.loc[:,raw_x.columns]
    if latest_features.iloc[-cfg["lookback"]:].isna().any().any(): raise ValueError("Latest lookback contains unexpected missing features")
    latest_tensor=torch.tensor(fsc.transform(latest_features)[-cfg["lookback"]:][None],dtype=torch.float32); latest_seed=[]
    for state in seed_states:
        latest_model=MSDP(**model_args); latest_model.load_state_dict(state); latest_model.eval()
        with torch.no_grad(): scaled={k:v.numpy() for k,v in latest_model(latest_tensor).items() if k not in {"expert_latents","context","direction_logits"}}
        latest_seed.append(_inverse(tsc,scaled))
    latest_out=average_predictions(latest_seed); latest={"data_date":str(market.date.iloc[-1]),"current_vnindex":float(market.close.iloc[-1]),"note":"Hồ sơ dự báo theo khoảng thời gian; không phải đường giá tương lai","horizons":[]}
    for j,h in enumerate(hs):
        llo,lhi=calibrator.transform(latest_out["return_quantiles"][:,j,0],latest_out["return_quantiles"][:,j,-1]); dispersion=float(np.std([p["return_quantiles"][-1,j,2] for p in seed_test])); disagreement=float(latest_out["expert_disagreement"][0,j]); score,label=confidence_score(.5,abs(metrics[f"h{h}"]["calibrated_interval"]["coverage"]-.9),min(1,disagreement/10),min(1,dispersion/5)); latest["horizons"].append({"horizon":h,"probability_positive":float(latest_out["direction_prob"][0,j]),"return_quantiles":latest_out["return_quantiles"][0,j].tolist(),"raw_interval":latest_out["return_quantiles"][0,j,[0,-1]].tolist(),"calibrated_interval":[float(llo[0]),float(lhi[0])],"mdd_quantiles":latest_out["mdd_quantiles"][0,j].tolist(),"volatility":float(latest_out["volatility"][0,j]),"expert_weights":latest_out["gate_weights"][0,j].tolist(),"expert_disagreement":disagreement,"seed_dispersion":dispersion,"confidence":{"score":score,"label":label}})
    latest["interpretation"]=interpret(hs,latest_out["direction_prob"][0],latest_out["gate_weights"][0],mdd_q10=latest_out["mdd_quantiles"][0,:,0]); outp=root/"artifacts/predictions"; (outp/"latest_forecast.json").write_text(json.dumps(latest,indent=2),encoding="utf-8"); pd.json_normalize(latest["horizons"]).to_csv(outp/"latest_forecast.csv",index=False); (outp/"latest_forecast.md").write_text("# Latest horizon forecast profile\n\n```json\n"+json.dumps(latest,indent=2)+"\n```\n",encoding="utf-8"); (outp/"latest_forecast_VI.md").write_text("# Hồ sơ dự báo theo khoảng thời gian mới nhất\n\n```json\n"+json.dumps(latest,indent=2)+"\n```\n",encoding="utf-8")
    tables=root/"reports/tables"; tables.mkdir(parents=True,exist_ok=True); (tables/"final_metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8"); (tables/"baseline_metrics.json").write_text(json.dumps(baseline_metrics,indent=2),encoding="utf-8"); (tables/"bootstrap_results.json").write_text(json.dumps(bootstrap,indent=2),encoding="utf-8"); (tables/"ablation_results.json").write_text(json.dumps(ablation_results,indent=2),encoding="utf-8")
    # Evaluation ensemble manifest; production retraining is deliberately distinct and documented.
    eval_bundle={"state_dict":seed_states[0],"model_args":model_args,"seeds":cfg["seeds"],"feature_order":list(raw_x.columns),"feature_metadata":meta.to_dict("records"),"conformal":calibrator.state_dict(),"training_date_range":[str(df.date.iloc[dev[0]]),str(df.date.iloc[dev[-1]])],"config":cfg,"model_version":"0.2.0-evaluation-seed-member"}; torch.save(eval_bundle,root/"artifacts/models/evaluation_model.pt")
    production={**eval_bundle,"model_version":"0.2.0-production-latest-member","calibration_source":"evaluation ensemble calibration; never production in-sample residual","production_training_note":"Distinct deployment bundle; evaluation metrics remain from the ensemble and are immutable."}; torch.save(production,root/"artifacts/models/production_model.pt")
    figures=generate_research_figures(market,pred,metrics,baseline_metrics,ablation_results,seed_results,latest,root/"reports/figures"); generate_report(metrics,quality,latest,root/"reports"); save_metadata(metadata(cfg,data_path,[quality["start"],quality["end"]]),root/"artifacts/run_metadata.json"); summary={"run_label":cfg.get("run_label"),"runtime_seconds":round(time.time()-started,2),"tests_not_run_inside_pipeline":True,"best_params":best,"seed_results":seed_results,"metrics":metrics,"baseline":baseline_metrics,"ablation":ablation_results,"bootstrap":bootstrap,"figures":figures}; (root/"artifacts/run_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); return summary
