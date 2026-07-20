from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from msdp.reporting import generate_report
generate_report(json.loads((ROOT/"reports/tables/final_metrics.json").read_text()),json.loads((ROOT/"reports/tables/data_quality.json").read_text()),json.loads((ROOT/"artifacts/predictions/latest_forecast.json").read_text()),ROOT/"reports")

