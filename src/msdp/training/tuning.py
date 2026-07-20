from __future__ import annotations
from pathlib import Path
import yaml

def save_default_best(config,path):
    """Fallback used when a full Optuna study is intentionally skipped in quick mode."""
    Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(yaml.safe_dump(config["model"],sort_keys=False),encoding="utf-8")

