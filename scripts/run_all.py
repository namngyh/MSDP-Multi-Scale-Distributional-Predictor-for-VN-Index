from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from msdp.pipeline import run
p=argparse.ArgumentParser(); p.add_argument("--config",default="configs/default.yaml"); p.add_argument("--data",required=True); a=p.parse_args(); print(json.dumps(run(a.config,a.data,ROOT),indent=2))

