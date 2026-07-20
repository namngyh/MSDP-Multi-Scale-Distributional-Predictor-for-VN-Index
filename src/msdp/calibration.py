from __future__ import annotations
import numpy as np

class StaticCQRCalibrator:
    def __init__(self,alpha=.1): self.alpha=alpha
    def fit(self,lower,upper,y):
        s=np.maximum(lower-y,y-upper); n=len(s); level=min(1,np.ceil((n+1)*(1-self.alpha))/n); self.q=np.quantile(s,level,axis=0,method="higher"); return self
    def transform(self,lower,upper): return lower-self.q,upper+self.q

class RollingCQRCalibrator:
    def __init__(self,window=252,alpha=.1): self.window=window; self.alpha=alpha; self.history=[]
    def seed(self,lower,upper,y): self.history=list(np.maximum(lower-y,y-upper)[-self.window:]); return self
    def predict(self,lower,upper):
        q=np.quantile(np.asarray(self.history),1-self.alpha,axis=0) if self.history else np.zeros_like(lower); return lower-q,upper+q
    def update(self,lower,upper,y): self.history.append(np.maximum(lower-y,y-upper)); self.history=self.history[-self.window:]

class AdaptiveConformalCalibrator(RollingCQRCalibrator):
    def __init__(self,window=252,alpha=.1,gamma=.01): super().__init__(window,alpha); self.target=alpha; self.gamma=gamma
    def update(self,lower,upper,y):
        miss=np.asarray((y<lower)|(y>upper),float).mean(); self.alpha=float(np.clip(self.alpha+self.gamma*(self.target-miss),.01,.5)); super().update(lower,upper,y)

