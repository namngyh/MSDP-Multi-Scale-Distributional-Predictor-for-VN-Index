from __future__ import annotations
from pathlib import Path
import os
os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd()/".matplotlib"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def _save(path): plt.tight_layout(); plt.savefig(path,dpi=180); plt.close()
def line_plot(x,series,title,ylabel,path):
    plt.figure(figsize=(10,4));
    for label,y in series.items(): plt.plot(x,y,label=label,linewidth=1)
    plt.title(title); plt.xlabel("Date"); plt.ylabel(ylabel); plt.legend(); _save(path)
def bar_plot(labels,values,title,ylabel,path):
    plt.figure(figsize=(8,4)); plt.bar(labels,values); plt.title(title); plt.xlabel("Category"); plt.ylabel(ylabel); _save(path)
