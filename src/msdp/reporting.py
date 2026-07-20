from __future__ import annotations
import json
from pathlib import Path
import markdown

def generate_report(metrics,quality,latest,out_dir="reports",synthetic=False):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    verdict="No claim of superiority is made without paired bootstrap evidence."
    text=f"""# MSDP Report

## Executive summary

This report was generated from saved pipeline outputs. {verdict}

## Research question

Does horizon-dependent multi-scale expert fusion improve out-of-sample distribution forecasts over simple baselines?

## Data description and quality

Rows: {quality.get('rows')}; range: {quality.get('start')} to {quality.get('end')}. Issues: {quality.get('issues')}.

## Method

Features are causal rolling statistics. Targets are forward 5/20/60-session log returns, realized volatility and path drawdown. Chronological development/calibration/test partitions use a 60-session purge. Scalers are fit on development only. Test observations are never used for tuning or calibration.

The model uses short, medium, long and range-volatility convolutional experts. A horizon-conditioned softmax gate fuses their latent states. Ordered quantiles use positive softplus increments. CQR intervals are calibrated only from the calibration partition.

## Final test results

```json
{json.dumps(metrics,indent=2)}
```

## Latest forecast

```json
{json.dumps(latest,indent=2)}
```

## Limitations

This is research software, not investment advice. Non-stationarity, limited samples, transaction costs, model/seed sensitivity and time-series dependence constrain interpretation. Conformal coverage is empirical; no iid finite-sample guarantee is claimed. A forecast profile across horizons is not a future price path.

## Conclusion

Conclusions must follow the metrics and uncertainty intervals above. {verdict}
"""
    (out/"MSDP_Report.md").write_text(text,encoding="utf-8"); (out/"MSDP_Report.html").write_text(markdown.markdown(text,extensions=["fenced_code"]),encoding="utf-8")
    vi=text.replace("# MSDP Report","# Báo cáo MSDP").replace("This is research software, not investment advice.","Đây là phần mềm nghiên cứu, không phải khuyến nghị đầu tư.")
    (out/"MSDP_Report_VI.md").write_text(vi,encoding="utf-8")
    (out/"model_card.md").write_text("# Model card\n\nMSDP is a CPU-capable probabilistic VN-Index research model. Intended for research only. See MSDP_Report.md for evaluation and limitations.\n",encoding="utf-8")
    (out/"limitations.md").write_text("# Limitations\n\nRegime shifts, data quality, finite calibration history, seed dispersion and wide intervals may reduce usefulness. This project does not provide investment advice.\n",encoding="utf-8")

