from __future__ import annotations
from pathlib import Path
import json,yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import optuna

def run_optuna(objective,config,out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); storage=f"sqlite:///{(out/'optuna_study.db').resolve().as_posix()}"
    study=optuna.create_study(study_name=f"msdp_{config.get('run_label','run')}",direction="minimize",storage=storage,load_if_exists=True,pruner=optuna.pruners.MedianPruner(n_startup_trials=1))
    remaining=max(0,int(config["training"]["trials"])-len(study.trials));
    if remaining: study.optimize(objective,n_trials=remaining)
    study.trials_dataframe().to_csv(out/"trials.csv",index=False); best={**config["model"],**study.best_params}; (out/"best_params.yaml").write_text(yaml.safe_dump(best,sort_keys=False),encoding="utf-8")
    complete=[t for t in study.trials if t.value is not None]; plt.figure(figsize=(8,4)); plt.plot([t.number for t in complete],[t.value for t in complete],marker="o",color="black"); plt.xlabel("Trial"); plt.ylabel("Validation objective"); plt.title("Optuna optimization history"); plt.tight_layout(); plt.savefig(out/"optimization_history.png",dpi=180); plt.close()
    try: importance=optuna.importance.get_param_importances(study)
    except Exception: importance={}
    plt.figure(figsize=(8,4)); plt.barh(list(importance),list(importance.values()),color="0.35"); plt.xlabel("Importance"); plt.title("Optuna parameter importance"); plt.tight_layout(); plt.savefig(out/"parameter_importance.png",dpi=180); plt.close()
    (out/"tuning_summary_VI.md").write_text(f"# Kết quả tuning\n\nLoại chạy: **{config.get('run_label','run')} tuning result**.\n\nSố trial hoàn tất: {len(complete)}. Best objective: {study.best_value:.6f}.\n\n```yaml\n{yaml.safe_dump(best,sort_keys=False)}```\n",encoding="utf-8")
    return best,study
