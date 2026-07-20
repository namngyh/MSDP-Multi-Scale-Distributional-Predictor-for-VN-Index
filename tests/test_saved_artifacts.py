from pathlib import Path
import json,torch
from msdp.calibration import StaticCQRCalibrator
def test_saved_calibrator_load_and_bundle_distinction():
    p=Path("artifacts/calibration/conformal.json")
    if not p.exists(): return
    c=StaticCQRCalibrator.from_state_dict(json.loads(p.read_text())); assert (c.qhat>=0).all()
    e=torch.load("artifacts/models/evaluation_model.pt",weights_only=False); p=torch.load("artifacts/models/production_model.pt",weights_only=False); assert e["model_version"]!=p["model_version"]

