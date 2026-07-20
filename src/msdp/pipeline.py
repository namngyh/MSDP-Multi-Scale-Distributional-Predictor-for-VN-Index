from __future__ import annotations
import json, shutil
from pathlib import Path
import joblib, numpy as np, pandas as pd, torch
from .calibration import StaticCQRCalibrator
from .config import load_config
from .data_io import load_market_data
from .data_quality import assess_quality,save_quality
from .dataset import SequenceDataset
from .features import build_features
from .interpretation import confidence_score,interpret
from .metrics import evaluate_arrays,interval_metrics
from .models import MSDP,ZeroReturnBaseline
from .plotting import line_plot,bar_plot
from .reporting import generate_report
from .reproducibility import metadata,save_metadata,set_global_seed
from .scaling import fit_feature_scaler
from .splits import chronological_split
from .targets import build_targets
from .training.trainer import train_model,predict
from .training.tuning import save_default_best

def run(config_path,data_path,root="."):
    root=Path(root); cfg=load_config(config_path); set_global_seed(cfg["seed"],cfg["deterministic"])
    df=load_market_data(data_path); quality=assess_quality(df); save_quality(quality,root/"reports/tables/data_quality.json")
    feat,meta=build_features(df,cfg["min_feature_nonmissing"]); target=build_targets(df,cfg["horizons"]); meta.to_csv(root/"data/processed/feature_metadata.csv",index=False)
    valid=target.notna().all(axis=1); last_valid=int(np.flatnonzero(valid)[-1])+1; frame=pd.concat([df[["date","close"]],feat,target],axis=1).iloc[:last_valid]
    # Feature missing values use development-only medians; no future statistics.
    spc=cfg["split"]; splits=chronological_split(len(frame),cfg["purge_gap"],spc["development"],spc["calibration"],(spc["min_development"],spc["min_calibration"],spc["min_test"]))
    med=feat.iloc[splits["development"]].median(); x=feat.iloc[:last_valid].fillna(med); scaler=fit_feature_scaler(x.iloc[splits["development"]]); xs=scaler.transform(x)
    joblib.dump(scaler,root/"artifacts/scalers/feature_scaler.joblib"); frame.to_csv(root/"data/processed/model_frame.csv",index=False)
    hs=cfg["horizons"]; target_cols=[f"return_h{h}" for h in hs]+[f"direction_h{h}" for h in hs]+[f"mdd_h{h}" for h in hs]+[f"volatility_h{h}" for h in hs]
    # Reserve the tail of development as early-stopping validation, purged from training.
    dev=splits["development"]; val_size=min(252,max(50,len(dev)//8)); tr=dev[:-(val_size+cfg["purge_gap"])]; va=dev[-val_size:]
    trds=SequenceDataset(xs,target.iloc[:last_valid],tr,cfg["lookback"],target_cols); vads=SequenceDataset(xs,target.iloc[:last_valid],va,cfg["lookback"],target_cols)
    range_ix=[i for i,n in enumerate(feat.columns) if meta.set_index("name").loc[n,"group"] in {"range","volatility","drawdown","market_position","volume"}]
    mc=cfg["model"]; args={"n_features":len(feat.columns),"horizons":hs,"return_quantiles":cfg["quantiles"],"mdd_quantiles":cfg["mdd_quantiles"],**mc,"range_indices":range_ix}
    model=MSDP(**args); model,hist=train_model(model,trds,vads,cfg,cfg["device"])
    bundle={"state_dict":model.state_dict(),"model_args":args,"lookback":cfg["lookback"],"feature_order":list(feat.columns),"feature_medians":med.to_dict(),"min_feature_nonmissing":cfg["min_feature_nonmissing"],"training_range":[str(df.date.iloc[tr[0]].date()),str(df.date.iloc[tr[-1]].date())]}
    torch.save(bundle,root/"artifacts/models/evaluation_model.pt"); torch.save(bundle,root/"artifacts/models/production_model.pt")
    calds=SequenceDataset(xs,target.iloc[:last_valid],splits["calibration"],cfg["lookback"],target_cols); testds=SequenceDataset(xs,target.iloc[:last_valid],splits["test"],cfg["lookback"],target_cols)
    cp,cix=predict(model,calds,device=cfg["device"]); tp,tix=predict(model,testds,device=cfg["device"])
    yret=target.loc[tix,[f"return_h{h}" for h in hs]].to_numpy(); ydir=target.loc[tix,[f"direction_h{h}" for h in hs]].to_numpy(); ymdd=target.loc[tix,[f"mdd_h{h}" for h in hs]].to_numpy(); yvol=target.loc[tix,[f"volatility_h{h}" for h in hs]].to_numpy()
    calret=target.loc[cix,[f"return_h{h}" for h in hs]].to_numpy(); calibrator=StaticCQRCalibrator(1-cfg["target_coverage"]).fit(cp["return_quantiles"][:,:,0],cp["return_quantiles"][:,:,-1],calret); lo,hi=calibrator.transform(tp["return_quantiles"][:,:,0],tp["return_quantiles"][:,:,-1])
    metrics=evaluate_arrays(yret,ymdd,yvol,ydir,tp,cfg["quantiles"],cfg["mdd_quantiles"])
    for j,h in enumerate(hs):
        metrics[f"h{h}"]["calibrated_interval"]=interval_metrics(yret[:,j],lo[:,j],hi[:,j],1-cfg["target_coverage"])
    # Honest simple baseline on the identical split; parameters use development only.
    devret=target.loc[dev,[f"return_h{h}" for h in hs]].dropna().to_numpy(); baseline=ZeroReturnBaseline().fit(devret,cfg["quantiles"]); bq,bp=baseline.predict(len(tix))
    baseline_metrics={}
    for j,h in enumerate(hs):
        baseline_metrics[f"h{h}"]={"return_mae":float(np.mean(abs(yret[:,j]))),"return_pinball":float(np.mean(np.maximum(np.asarray(cfg["quantiles"])*(yret[:,j,None]-bq[:,j]),(np.asarray(cfg["quantiles"])-1)*(yret[:,j,None]-bq[:,j])))),"brier":float(np.mean((ydir[:,j]-bp[:,j])**2))}
        metrics[f"h{h}"]["vs_zero_baseline"]={k:metrics[f"h{h}"][k]-baseline_metrics[f"h{h}"][k] for k in ("return_mae","return_pinball","brier")}
    rows={"date":df.loc[tix,"date"].to_numpy(),"current_close":df.loc[tix,"close"].to_numpy()}
    for j,h in enumerate(hs):
        for qi,q in enumerate([5,25,50,75,95]): rows[f"return_q{q:02d}_h{h}"]=tp["return_quantiles"][:,j,qi]
        rows.update({f"return_lower90_raw_h{h}":tp["return_quantiles"][:,j,0],f"return_upper90_raw_h{h}":tp["return_quantiles"][:,j,-1],f"return_lower90_calibrated_h{h}":lo[:,j],f"return_upper90_calibrated_h{h}":hi[:,j],f"direction_probability_h{h}":tp["direction_prob"][:,j],f"actual_return_h{h}":yret[:,j],f"actual_direction_h{h}":ydir[:,j],f"actual_mdd_h{h}":ymdd[:,j],f"predicted_volatility_h{h}":tp["volatility"][:,j],f"actual_volatility_h{h}":yvol[:,j]})
        for qi,q in enumerate([10,50,90]): rows[f"mdd_q{q:02d}_h{h}"]=tp["mdd_quantiles"][:,j,qi]
        close=rows["current_close"]
        for qi,q in [(0,5),(2,50),(4,95)]: rows[f"projected_index_q{q:02d}_h{h}"]=close*np.exp(tp["return_quantiles"][:,j,qi]/100)
        for k,name in enumerate(["short","medium","long","range_vol"][:tp["gate_weights"].shape[-1]]): rows[f"gate_{name}_h{h}"]=tp["gate_weights"][:,j,k]
        rows[f"gate_entropy_h{h}"]=-(tp["gate_weights"][:,j]*np.log(tp["gate_weights"][:,j].clip(1e-9))).sum(1)
    pred=pd.DataFrame(rows); pred.to_csv(root/"artifacts/predictions/test_predictions.csv",index=False)
    latest_x=scaler.transform(feat.fillna(med)); latest_seq=torch.tensor(latest_x[-cfg["lookback"]:][None],dtype=torch.float32)
    with torch.no_grad(): latest_out={k:v.cpu().numpy()[0] for k,v in model(latest_seq).items() if k!="expert_latents"}
    latest_lo,latest_hi=calibrator.transform(latest_out["return_quantiles"][:,0],latest_out["return_quantiles"][:,-1])
    latest={"data_date":str(df.date.iloc[-1]),"current_vnindex":float(df.close.iloc[-1]),"horizons":[]}
    for j,h in enumerate(hs):
        width=float(latest_hi[j]-latest_lo[j]); score,label=confidence_score(.5,abs(metrics[f"h{h}"]["calibrated_interval"]["coverage"]-.9),float(np.std(latest_out["gate_weights"][j])))
        latest["horizons"].append({"horizon":h,"probability_positive":float(latest_out["direction_prob"][j]),"return_quantiles":{str(q):float(latest_out["return_quantiles"][j,qi]) for qi,q in enumerate([5,25,50,75,95])},"projected_index_quantiles":{str(q):float(df.close.iloc[-1]*np.exp(latest_out["return_quantiles"][j,qi]/100)) for qi,q in [(0,5),(2,50),(4,95)]},"calibrated_interval":[float(latest_lo[j]),float(latest_hi[j])],"mdd_quantiles":latest_out["mdd_quantiles"][j].tolist(),"volatility":float(latest_out["volatility"][j]),"expert_weights":latest_out["gate_weights"][j].tolist(),"confidence":{"score":score,"label":label},"interval_width":width})
    latest["interpretation"]=interpret(hs,latest_out["direction_prob"],latest_out["gate_weights"],mdd_q10=latest_out["mdd_quantiles"][:,0])
    (root/"artifacts/predictions/latest_forecast.json").write_text(json.dumps(latest,indent=2),encoding="utf-8"); pd.json_normalize(latest["horizons"]).to_csv(root/"artifacts/predictions/latest_forecast.csv",index=False); (root/"artifacts/predictions/latest_forecast.md").write_text("# Latest forecast\n\n```json\n"+json.dumps(latest,indent=2)+"\n```\n",encoding="utf-8")
    Path(root/"reports/tables/final_metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8"); Path(root/"reports/tables/baseline_metrics.json").write_text(json.dumps(baseline_metrics,indent=2),encoding="utf-8"); save_default_best(cfg,root/"artifacts/tuning/best_params.yaml")
    dates=df.loc[tix,"date"]; Path(root/"reports/figures").mkdir(parents=True,exist_ok=True)
    for j,h in enumerate(hs): line_plot(dates,{"actual":yret[:,j],"median":tp["return_quantiles"][:,j,2]},f"Predicted vs actual return h={h}","Log return (%)",root/f"reports/figures/predicted_vs_actual_return_h{h}.png")
    bar_plot([str(h) for h in hs],[metrics[f"h{h}"]["coverage"] for h in hs],"Interval coverage by horizon","Coverage",root/"reports/figures/interval_coverage_by_horizon.png")
    generate_report(metrics,quality,latest,root/"reports"); save_metadata(metadata(cfg,data_path,[quality["start"],quality["end"]]),root/"artifacts/run_metadata.json")
    return metrics
