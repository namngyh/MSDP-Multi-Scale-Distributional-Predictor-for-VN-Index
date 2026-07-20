from __future__ import annotations
import numpy as np
from sklearn.linear_model import Ridge,LogisticRegression

class ZeroPointForecastBaseline:
    def predict(self,n,n_horizons): return np.zeros((n,n_horizons))

class UnconditionalEmpiricalDistributionBaseline:
    def fit(self,returns,mdd,volatility,quantiles,mdd_quantiles):
        self.return_q=np.quantile(returns,quantiles,axis=0).T; self.mdd_q=np.quantile(mdd,mdd_quantiles,axis=0).T; self.vol=np.median(volatility,axis=0); return self
    def predict(self,n): return {"return_quantiles":np.tile(self.return_q[None],(n,1,1)),"mdd_quantiles":np.tile(self.mdd_q[None],(n,1,1)),"volatility":np.tile(self.vol[None],(n,1))}

class HistoricalFrequencyDirectionBaseline:
    def fit(self,direction): self.frequency=np.mean(direction,axis=0); return self
    def predict(self,n): return np.tile(self.frequency[None],(n,1))

class HistoricalMeanBaseline:
    def fit(self,returns,quantiles): self.mean=np.mean(returns,axis=0); self.residual_q=np.stack([np.quantile(returns[:,j]-self.mean[j],quantiles) for j in range(returns.shape[1])]); return self
    def predict(self,n): return np.tile(self.mean[None],(n,1)),np.tile((self.mean[:,None]+self.residual_q)[None],(n,1,1))

class RidgeDirectBaseline:
    def __init__(self,alpha=1.): self.alpha=alpha
    def fit(self,x,y,residual_x=None,residual_y=None):
        self.models=[Ridge(alpha=self.alpha).fit(x,y[:,j]) for j in range(y.shape[1])]; rx=x if residual_x is None else residual_x; ry=y if residual_y is None else residual_y; self.residuals=np.stack([ry[:,j]-self.models[j].predict(rx) for j in range(y.shape[1])],1); return self
    def predict(self,x,quantiles):
        point=np.stack([m.predict(x) for m in self.models],1); q=np.stack([point[:,j,None]+np.quantile(self.residuals[:,j],quantiles) for j in range(point.shape[1])],1); return point,q

class LogisticDirectionBaseline:
    def __init__(self,c=1.,class_weight=None): self.c=c; self.class_weight=class_weight
    def fit(self,x,y): self.models=[LogisticRegression(C=self.c,class_weight=self.class_weight,max_iter=1000).fit(x,y[:,j].astype(int)) for j in range(y.shape[1])]; return self
    def predict(self,x): return np.stack([m.predict_proba(x)[:,1] for m in self.models],1)

# Tên cũ chỉ để đọc artifact cũ; mã mới không dùng tên này trong báo cáo.
class ZeroReturnBaseline(UnconditionalEmpiricalDistributionBaseline):
    def fit(self,y,quantiles): self.return_q=np.quantile(y,quantiles,axis=0).T; self.p=(y>0).mean(axis=0); return self
    def predict(self,n): return np.tile(self.return_q[None],(n,1,1)),np.tile(self.p,(n,1))
