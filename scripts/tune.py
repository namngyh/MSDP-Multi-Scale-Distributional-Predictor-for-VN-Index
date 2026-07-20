from pathlib import Path
import argparse, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from msdp.config import load_config
from msdp.training.tuning import save_default_best
p=argparse.ArgumentParser(); p.add_argument("--config",default="configs/default.yaml"); a=p.parse_args(); save_default_best(load_config(a.config),ROOT/"artifacts/tuning/best_params.yaml"); print("Saved configured parameters; run_all performs model fitting.")

