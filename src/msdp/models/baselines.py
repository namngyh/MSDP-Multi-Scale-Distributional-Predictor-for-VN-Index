from __future__ import annotations
import numpy as np
from sklearn.linear_model import Ridge, LogisticRegression

class ZeroReturnBaseline:
    def fit(self,y,quantiles): self.q=np.quantile(y,quantiles,axis=0).T; self.p=(y>0).mean(axis=0); return self
    def predict(self,n): return np.tile(self.q[None,:,:],(n,1,1)),np.tile(self.p,(n,1))

class HistoricalMeanBaseline(ZeroReturnBaseline): pass

class RidgeDirectBaseline:
    def fit(self,x,y):
        self.reg=[Ridge(alpha=1).fit(x,y[:,j]) for j in range(y.shape[1])]
        self.cls=[]
        for j in range(y.shape[1]): self.cls.append(LogisticRegression(max_iter=500).fit(x,(y[:,j]>0).astype(int)))
        self.res=np.stack([y[:,j]-self.reg[j].predict(x) for j in range(y.shape[1])],1); return self
    def predict(self,x,quantiles):
        med=np.stack([m.predict(x) for m in self.reg],1); q=np.stack([med[:,j,None]+np.quantile(self.res[:,j],quantiles) for j in range(med.shape[1])],1)
        p=np.stack([m.predict_proba(x)[:,1] for m in self.cls],1); return q,p

