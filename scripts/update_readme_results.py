"""Sinh to�n b? README ti?ng Vi?t t? artifact th?c t? c?a pipeline."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument("--run",default="latest"); args=p.parse_args()
metrics=json.loads((ROOT/"reports/tables/final_metrics.json").read_text(encoding="utf-8")); baseline=json.loads((ROOT/"reports/tables/baseline_metrics.json").read_text(encoding="utf-8")); bootstrap=json.loads((ROOT/"reports/tables/bootstrap_results.json").read_text(encoding="utf-8")); ablations=json.loads((ROOT/"reports/tables/ablation_results.json").read_text(encoding="utf-8")); seeds=json.loads((ROOT/"reports/tables/seed_results.json").read_text(encoding="utf-8")); quality=json.loads((ROOT/"reports/tables/data_quality.json").read_text(encoding="utf-8")); latest=json.loads((ROOT/"artifacts/predictions/latest_forecast.json").read_text(encoding="utf-8")); summary=json.loads((ROOT/"artifacts/run_summary.json").read_text(encoding="utf-8")); pred=pd.read_csv(ROOT/"artifacts/predictions/test_predictions.csv"); manifest=json.loads((ROOT/"reports/figures/figure_manifest.json").read_text(encoding="utf-8")); hs=[5,20,60]

titles={
"data_quality_overview.png":"T?ng quan ch?t lu?ng d? li?u","vnindex_close_history.png":"L?ch s? di?m d�ng c?a VN-Index","vnindex_drawdown_history.png":"L?ch s? drawdown VN-Index","return_distribution.png":"Ph�n ph?i l?i su?t ng�y","rolling_volatility.png":"Bi?n d?ng cu?n chi?u","target_distribution_by_horizon.png":"Ph�n ph?i target theo k? h?n","training_total_loss_by_seed.png":"T?ng loss hu?n luy?n","training_return_loss.png":"Loss ph�n v? l?i su?t","training_direction_loss.png":"Loss x�c su?t hu?ng","training_mdd_loss.png":"Loss maximum drawdown","training_volatility_loss.png":"Loss bi?n d?ng","learning_rate_history.png":"L?ch s? learning rate","seed_validation_comparison.png":"So s�nh validation gi?a c�c seed","raw_vs_calibrated_coverage.png":"Coverage tru?c v� sau conformal","interval_width_by_horizon.png":"�? r?ng kho?ng theo k? h?n","interval_score_by_horizon.png":"Interval score theo k? h?n","conditional_coverage_by_volatility.png":"Coverage theo tr?ng th�i bi?n d?ng","direction_probability_vs_actual.png":"X�c su?t tang v� k?t qu? th?c t?","brier_score_by_horizon.png":"Brier score theo k? h?n","mean_gate_weights_by_horizon.png":"Tr?ng s? gate trung b�nh","gate_entropy_by_horizon.png":"Entropy gate chu?n h�a","expert_disagreement.png":"M?c b?t d?ng gi?a c�c expert","expert_latent_correlation.png":"Tuong quan d? b�o gi?a c�c expert","expert_usage_by_market_condition.png":"M?c s? d?ng expert","predicted_vs_actual_volatility.png":"Bi?n d?ng d? b�o v� th?c t?","mdd_threshold_calibration.png":"T?n su?t vu?t ngu?ng MDD","baseline_return_pinball_comparison.png":"So s�nh pinball v?i baseline","baseline_direction_brier_comparison.png":"So s�nh Brier v?i baseline","baseline_interval_coverage_comparison.png":"So s�nh coverage","baseline_interval_score_comparison.png":"So s�nh interval score","ablation_comparison.png":"K?t qu? ablation","bootstrap_confidence_intervals.png":"Kho?ng tin c?y bootstrap","performance_by_market_condition.png":"Hi?u nang theo di?u ki?n th? tru?ng","seed_stability.png":"�? ?n d?nh theo seed","latest_horizon_return_profile.png":"H? so l?i su?t m?i nh?t","latest_projected_index_interval.png":"Kho?ng ch? s? d? ph�ng m?i nh?t","latest_gate_weights.png":"Gate m?i nh?t","latest_risk_profile.png":"H? so r?i ro m?i nh?t","latest_confidence_components.png":"C�c th�nh ph?n confidence m?i nh?t"}
for h in hs:
    titles.update({f"predicted_vs_actual_return_h{h}.png":f"L?i su?t d? b�o v� th?c t? � {h} phi�n",f"return_fan_chart_h{h}.png":f"Bi?u d? qu?t l?i su?t � {h} phi�n",f"residual_return_h{h}.png":f"Ph?n du l?i su?t � {h} phi�n",f"rolling_coverage_h{h}.png":f"Coverage cu?n chi?u � {h} phi�n",f"direction_reliability_h{h}.png":f"�? tin c?y x�c su?t hu?ng � {h} phi�n",f"gate_weights_h{h}.png":f"Tr?ng s? gate � {h} phi�n",f"expert_predictions_h{h}.png":f"D? b�o ri�ng t?ng expert � {h} phi�n",f"predicted_vs_actual_mdd_h{h}.png":f"MDD d? b�o v� th?c t? � {h} phi�n"})

def h_from(name):
    for h in hs:
        if f"h{h}" in name: return h
    return None
def comment(name):
    h=h_from(name)
    if "predicted_vs_actual_return" in name: return f"MAE k? h?n {h} l� {metrics[f'h{h}']['return_mae']:.3f}% v� Spearman {metrics[f'h{h}']['spearman']:.3f}. D? b�o trung v? chua b�m s�t m?nh bi?n d?ng th?c t?; m� h�nh ph� h?p hon v?i m� t? ph�n ph?i r?i ro so v?i d? b�o di?m."
    if "fan_chart" in name: return f"Kho?ng g?c d?t coverage {metrics[f'h{h}']['coverage']:.1%}. Sau conformal, coverage d?t {metrics[f'h{h}']['calibrated_interval']['coverage']:.1%}, nhung d? r?ng tang t? {metrics[f'h{h}']['width']:.2f}% l�n {metrics[f'h{h}']['calibrated_interval']['width']:.2f}%."
    if "residual_return" in name: return f"Ph?n du k? h?n {h} ph?n �nh sai s? d? b�o trung v?; RMSE th?c t? l� {metrics[f'h{h}']['return_rmse']:.3f}%. C�c c?m sai s? l?n cho th?y ?nh hu?ng c?a regime v� volatility clustering."
    if "rolling_coverage" in name: return f"Coverage cu?n chi?u k? h?n {h} kh�ng ?n d?nh tuy?t d?i theo th?i gian. Coverage t?ng th? sau hi?u ch?nh l� {metrics[f'h{h}']['calibrated_interval']['coverage']:.1%}; d�y l� coverage th?c nghi?m, kh�ng ph?i b?o d?m iid."
    if "direction_reliability" in name: return f"Brier score k? h?n {h} l� {metrics[f'h{h}']['brier']:.4f}, ROC AUC {metrics[f'h{h}'].get('roc_auc',float('nan')):.3f}. X�c su?t c� th�ng tin h?n ch? v� chua t?o ph�n t�ch l?p m?nh."
    if "gate_weights_h" in name:
        means={n:pred[f"gate_{n}_h{h}"].mean() for n in ["short","medium","long","range_vol"]}; dom=max(means,key=means.get); return f"Expert c� tr?ng s? trung b�nh cao nh?t l� `{dom}` ({means[dom]:.3f}). " + ("K?t qu? h? tr? chuy�n m�n h�a ng?n h?n." if h==5 and dom=="short" else "K?t qu? chua h? tr? gi? thuy?t short expert chi ph?i k? h?n 5 phi�n." if h==5 else "Long expert tang vai tr� ? k? h?n d�i, nhung m?c ph�n h�a gate v?n tuong d?i th?p.")
    if "expert_predictions" in name: return f"�? l?ch chu?n trung b�nh gi?a auxiliary expert forecasts ? k? h?n {h} l� {pred[f'expert_disagreement_h{h}'].mean():.3f}%. ��y l� b?t d?ng d? b�o, kh�c v?i entropy c?a tr?ng s? gate."
    if "predicted_vs_actual_mdd" in name: return f"MDD MAE k? h?n {h} l� {metrics[f'h{h}']['mdd_mae']:.3f}%. q10 bi?u di?n k?ch b?n drawdown x?u hon, c�n q90 g?n 0 hon; to�n b? quantile d� du?c audit kh�ng duong."
    if "coverage" in name or "interval" in name: return "Conformal c?i thi?n d? bao ph? nhung l�m kho?ng r?ng hon, d?c bi?t ? k? h?n d�i. Gi� tr? ch�nh l� m� t? b?t d?nh; d? s?c n�t c?a d? b�o gi?m khi y�u c?u coverage cao."
    if "brier" in name or "direction_probability" in name: return "Brier gi?m so v?i ZeroReturn ? c? ba k? h?n, nhung balanced accuracy v?n g?n v�ng 0,5. Kh�ng n�n di?n gi?i x�c su?t tang nhu t�n hi?u giao d?ch ch?c ch?n."
    if "gate" in name or "expert" in name: return "Gate c� xu hu?ng g?n tr?ng s? d?u; long expert nh?n tr?ng s? cao nh?t ? c? ba k? h?n. Learned gate chua ch?ng minh gi� tr? vu?t equal-weight trong quick ablation."
    if "baseline" in name: return "H5 v� H20 c� pinball k�m ZeroReturn; H60 c� pinball t?t hon nhung MAE k�m hon. Kh�ng c� c?i thi?n nh?t qu�n tr�n m?i metric v� horizon."
    if "ablation" in name: return f"Equal-weight d?t mean pinball {ablations[0]['return_pinball_mean']:.4f}, th?p hon Full MSDP kho?ng {np.mean([metrics[f'h{h}']['return_pinball'] for h in hs]):.4f}; single-scale d?t {ablations[1]['return_pinball_mean']:.4f}. Learned gate chua vu?t equal-weight."
    if "bootstrap" in name: return "C? ba CI95 c?a ch�nh l?ch MAE d?u ch?a 0. Ch�nh l?ch metric chua c� � nghia r� r�ng theo moving-block bootstrap."
    if "latest" in name: return f"H? so ng�y {latest['data_date']} cho th?y median return duong ? c? ba horizon, nhung calibrated interval d?u bao g?m 0 v� m? r?ng m?nh theo k? h?n. ��y kh�ng ph?i du?ng gi� tuong lai hay khuy?n ngh? mua b�n."
    if "training" in name or "learning_rate" in name or "seed" in name: return f"Quick run d�ng {len(seeds)} seed; best epoch l� {seeds[0]['best_epoch']} v?i validation loss {seeds[0]['best_validation_loss']:.4f}. M?t seed kh�ng d? d�nh gi� d? ?n d?nh da seed."
    if "volatility" in name: return "Volatility MAE l?n lu?t l� " + ", ".join("{:.2f}%".format(metrics[f"h{h}"]["volatility_mae"]) for h in hs) + " cho H5/H20/H60. Sai s? gi?m theo horizon nhung v?n d�ng k?."
    if "drawdown" in name or "mdd" in name: return "Drawdown l?ch s? th? hi?n c�c giai do?n stress r� r?t. MDD head d� b? ch?n ? mi?n kh�ng duong v� kh�ng di?n gi?i q90 l� k?ch b?n nghi�m tr?ng nh?t."
    if "return_distribution" in name or "target_distribution" in name: return "Ph�n ph?i l?i su?t c� du�i v� d? ph�n t�n tang theo horizon, l� l� do d�ng quantile regression thay cho gi? d?nh Gaussian c? d?nh."
    if "quality" in name: return f"C� {quality['rows']} phi�n t? {quality['start']} d?n {quality['end']}. Pipeline ghi nh?n {quality['issues']} v� kh�ng �m th?m s?a file ngu?n."
    return "Bi?u d? du?c sinh tr?c ti?p t? d? li?u ho?c artifact c?a quick pipeline; kh�ng s? d?ng s? li?u minh h?a gi?."

groups=[("D? li?u",manifest[:6]),("Hu?n luy?n",manifest[6:13]),("D? b�o l?i su?t",[x for x in manifest if any(k in x for k in ["predicted_vs_actual_return","return_fan_chart","residual_return"])]),("Hi?u ch?nh conformal",[x for x in manifest if "coverage" in x or "interval_width" in x or "interval_score" in x]),("X�c su?t hu?ng",[x for x in manifest if "direction_" in x or "brier" in x]),("Expert v� gate",[x for x in manifest if "gate" in x or "expert" in x]),("R?i ro",[x for x in manifest if "mdd" in x or "volatility" in x]),("So s�nh m� h�nh",[x for x in manifest if "baseline" in x or "ablation" in x or "bootstrap" in x or "performance" in x or "seed_stability" in x]),("D? b�o m?i nh?t",[x for x in manifest if "latest" in x])]
used=set(); figure_sections=[]
for group,files in groups:
    unique=[x for x in files if x not in used]; used.update(unique)
    if not unique: continue
    parts=[f"## {group}"]
    for name in unique: parts.extend([f"### {titles.get(name,name)}",f"![{titles.get(name,name)}](reports/figures/{name})",f"**Nh?n x�t:** {comment(name)}"])
    figure_sections.append("\n\n".join(parts))
left=[x for x in manifest if x not in used]
if left:
    figure_sections.append("## Bi?u d? b? sung\n\n"+"\n\n".join(f"### {titles.get(x,x)}\n\n![{titles.get(x,x)}](reports/figures/{x})\n\n**Nh?n x�t:** {comment(x)}" for x in left))

metric_rows="\n".join(f"| {h} | {metrics[f'h{h}']['return_mae']:.4f} | {metrics[f'h{h}']['return_pinball']:.4f} | {metrics[f'h{h}']['brier']:.4f} | {metrics[f'h{h}']['coverage']:.1%} | {metrics[f'h{h}']['calibrated_interval']['coverage']:.1%} | {metrics[f'h{h}']['vs_zero_baseline']['return_pinball']:+.4f} |" for h in hs)
latest_rows="".join(f"| {x['horizon']} | {x['probability_positive']:.1%} | {x['return_quantiles'][2]:+.3f}% | [{x['calibrated_interval'][0]:+.3f}%; {x['calibrated_interval'][1]:+.3f}%] |\n" for x in latest['horizons'])
figure_text="\n\n".join(figure_sections)
readme=f"""# MSDP � B? d? b�o ph�n ph?i da thang do cho VN-Index

## T�m t?t nghi�n c?u

MSDP d? b�o tr?c ti?p ph�n ph?i l?i su?t VN-Index cho 5, 20 v� 60 phi�n b?ng b?n chuy�n gia causal: ng?n h?n, trung h?n, d�i h?n v� range�volatility. M� h�nh d?ng th?i d? b�o x�c su?t tang, c�c ph�n v? l?i su?t, maximum drawdown, realized volatility, tr?ng s? gate v� m?c b?t d?ng gi?a c�c expert.

Repository n�y l� ph?n m?m nghi�n c?u, kh�ng ph?i khuy?n ngh? d?u tu. To�n b? s? li?u v� bi?u d? du?i d�y du?c d?c t? artifact c?a `{summary.get('run_label')}` run; kh�ng d�ng s? li?u minh h?a.

## K?t lu?n ch�nh

**Trong c?u h�nh v� giai do?n d? li?u hi?n t?i, chua c� b?ng ch?ng cho th?y MSDP vu?t baseline.** H5 v� H20 c� pinball k�m ZeroReturn. H60 c� pinball v� Brier t?t hon nhung MAE k�m hon. M?i CI95 bootstrap c?a ch�nh l?ch MAE d?u ch?a 0. Equal-weight ablation c� pinball trung b�nh th?p hon learned gate.

Gi� tr? ch�nh c?a MSDP hi?n n?m ? d? b�o ph�n ph?i v� hi?u ch?nh r?i ro, chua ph?i ? d? b�o di?m.

## D? li?u v� giao th?c ngo�i m?u

- {quality['rows']} phi�n, t? {quality['start']} d?n {quality['end']}.
- Development/calibration/test theo th?i gian, purge 60 phi�n.
- Feature selection v� scaler kh�ng d�ng test.
- CQR fit tr�n ensemble calibration prediction.
- Final test c� {len(pred)} origin d? b�o.
- Quick run: {summary['runtime_seconds']:.2f} gi�y, {len(seeds)} seed, 3 Optuna trials, hai ablation v� 50 bootstrap resamples.

## Ki?n tr�c v� t�nh d�ng to�n h?c

- Convolution causal d�ng left padding; kh�ng d�ng symmetric padding.
- Return head l?y median l�m t�m v� b?o d?m `q05 = q25 = q50 = q75 = q95`.
- MDD head b?o d?m `q10 = q50 = q90 = 0`; q10 l� k?ch b?n x?u hon.
- CQR score l� `max(lower-y, y-upper, 0)`; qhat ri�ng horizon v� kh�ng �m.
- Target scaler ri�ng theo type/horizon; volatility d�ng `log1p` v� Huber loss.
- Gate nh?n expert latent, learned context v� horizon embedding.
- Expert disagreement l� d? l?ch chu?n auxiliary return forecast, kh�ng ph?i d? l?ch gate weights.

## K?t qu? final test

| Horizon | MAE | Pinball | Brier | Coverage g?c | Coverage conformal | Pinball ? so v?i ZeroReturn |
|---:|---:|---:|---:|---:|---:|---:|
{metric_rows}

## D? b�o m?i nh?t

Ng�y d? li?u: **{latest['data_date']}**; VN-Index: **{latest['current_vnindex']:.2f}**.

| Horizon | X�c su?t tang | Median return | Kho?ng conformal |
|---:|---:|---:|---:|
{latest_rows}

Ba horizon t?o th�nh **h? so d? b�o theo kho?ng th?i gian**, kh�ng ph?i du?ng gi� d? b�o t?ng bu?c.

## C�i d?t v� l?nh Windows

```powershell
conda create -n msdp python=3.11 -y
conda activate msdp
pip install -r requirements.txt
pytest -q
python scripts/inspect_data.py --data data/raw/VNINDEX_Daily.csv
python scripts/run_all.py --config configs/quick.yaml --data data/raw/VNINDEX_Daily.csv
python scripts/run_all.py --config configs/default.yaml --data data/raw/VNINDEX_Daily.csv
python scripts/predict_latest.py --config configs/default.yaml --data data/raw/VNINDEX_Daily.csv --model artifacts/models/production_model.pt
python scripts/generate_report.py --run latest
python scripts/update_readme_results.py --run latest
```

## H?n ch?

- Artifact hi?n t?i l� quick run m?t seed, chua ph?i default three-seed study.
- D? li?u ngu?n c� vi ph?m OHLC du?c ghi trong data-quality report.
- Coverage tang nh? conformal nhung interval d�i h?n r?t r?ng.
- Gate g?n equal-weight v� chua vu?t equal-weight ablation.
- Production full retraining v� OOF production calibration chua ho�n t?t.

# To�n b? bi?u d? v� nh?n x�t

{figure_text}

## T�i li?u chi ti?t

- [B�o c�o nghi�n c?u d?y d?](reports/MSDP_BAO_CAO_DAY_DU_VI.md)
- [Nh?n x�t k?t qu?](reports/MSDP_NHAN_XET_KET_QUA_VI.md)
- [Review repository](reports/MSDP_REPOSITORY_REVIEW_VI.md)
- [K?t qu? ki?m th?](reports/test_results.txt)
- [H?n ch?](reports/MSDP_LIMITATIONS_VI.md)

## Tuy�n b? mi?n tr? tr�ch nhi?m

Kh�ng s? d?ng k?t qu? nhu b?o d?m l?i nhu?n ho?c l?i khuy�n mua b�n. Ngu?i d�ng t? ch?u tr�ch nhi?m ki?m tra d? li?u, gi? d?nh, chi ph� giao d?ch v� r?i ro th? tru?ng.
"""
(ROOT/"README.md").write_text(readme,encoding="utf-8"); (ROOT/"README_VI.md").write_text(readme,encoding="utf-8"); print(f"Đã cập nhật README tiếng Việt với {len(manifest)} biểu đồ cho run {args.run}.")
