from __future__ import annotations
from pathlib import Path
import joblib,numpy as np,torch
from .data_io import load_market_data
from .features import build_features
from .models import MSDP

def load_bundle(model_path):
    bundle=torch.load(model_path,map_location="cpu",weights_only=False)
    if "state_dict" not in bundle: raise ValueError("Bundle does not contain a deployable state_dict")
    model=MSDP(**bundle["model_args"]); model.load_state_dict(bundle["state_dict"]); model.eval(); return model,bundle

def predict_latest(data_path,model_path,scaler_path,target_scaler_path=None):
    model,bundle=load_bundle(model_path); df=load_market_data(data_path); feat,_=build_features(df); expected=bundle["feature_order"]
    if any(c not in feat for c in expected): raise ValueError("Feature order mismatch; required feature is absent")
    feat=feat[expected]; lb=bundle["config"]["lookback"]
    if feat.iloc[-lb:].isna().any().any(): raise ValueError("Latest lookback contains missing features")
    scaler=joblib.load(scaler_path); x=scaler.transform(feat); 
    with torch.no_grad(): out={k:v.numpy() for k,v in model(torch.tensor(x[-lb:][None],dtype=torch.float32)).items() if k not in {"expert_latents","context","direction_logits"}}
    target_scaler_path=target_scaler_path or Path(scaler_path).with_name("target_scalers.joblib"); tsc=joblib.load(target_scaler_path); out=tsc.inverse_predictions(out)
    return df.iloc[-1],{k:v[0] for k,v in out.items()},bundle
