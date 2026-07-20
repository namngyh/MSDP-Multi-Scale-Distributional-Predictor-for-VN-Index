from __future__ import annotations
import json
from pathlib import Path
import joblib, numpy as np, pandas as pd, torch
from .data_io import load_market_data
from .features import build_features
from .models import MSDP

def load_bundle(model_path):
    bundle=torch.load(model_path,map_location="cpu",weights_only=False); model=MSDP(**bundle["model_args"]); model.load_state_dict(bundle["state_dict"]); model.eval(); return model,bundle

def predict_latest(data_path,model_path,scaler_path):
    model,bundle=load_bundle(model_path); df=load_market_data(data_path); feat,_=build_features(df,bundle["min_feature_nonmissing"])
    if list(feat.columns)!=bundle["feature_order"]: raise ValueError("Feature order mismatch; training and inference schemas differ")
    feat=feat.fillna(pd.Series(bundle["feature_medians"])); scaler=joblib.load(scaler_path); x=scaler.transform(feat); lb=bundle["lookback"]
    seq=x[-lb:];
    if not np.isfinite(seq).all(): raise ValueError("Latest lookback contains missing features")
    with torch.no_grad(): out={k:v.numpy()[0] for k,v in model(torch.tensor(seq[None],dtype=torch.float32)).items() if k!="expert_latents"}
    return df.iloc[-1],out,bundle
