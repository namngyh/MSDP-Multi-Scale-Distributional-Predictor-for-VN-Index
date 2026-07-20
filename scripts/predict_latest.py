from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from msdp.inference import predict_latest
p=argparse.ArgumentParser(); p.add_argument("--config"); p.add_argument("--data",required=True); p.add_argument("--model",required=True); a=p.parse_args(); row,out,bundle=predict_latest(a.data,a.model,ROOT/"artifacts/scalers/feature_scaler.joblib"); payload={"data_date":str(row.date),"current_close":float(row.close),"outputs":{k:v.tolist() for k,v in out.items()}}; target=ROOT/"artifacts/predictions/latest_forecast.json"; target.write_text(json.dumps(payload,indent=2),encoding="utf-8"); print(json.dumps(payload,indent=2))

