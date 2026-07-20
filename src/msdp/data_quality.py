from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

def assess_quality(df: pd.DataFrame) -> dict:
    cols=set(df.columns); issues=[]
    if {"open","high","low","close"} <= cols:
        bad_high=int((df.high < df[["open","close"]].max(axis=1)).sum())
        bad_low=int((df.low > df[["open","close"]].min(axis=1)).sum())
        if bad_high or bad_low: issues.append(f"OHLC constraint violations: high={bad_high}, low={bad_low}")
    else: issues.append("OHLC incomplete; range features disabled")
    if "volume" not in cols: issues.append("Volume missing; volume features disabled")
    return {"rows":len(df), "start":str(df.date.min().date()), "end":str(df.date.max().date()),
            "duplicate_dates":int(df.date.duplicated().sum()), "missing":df.isna().sum().to_dict(), "issues":issues}

def save_quality(report: dict, path: str | Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(report, indent=2), encoding="utf-8")

