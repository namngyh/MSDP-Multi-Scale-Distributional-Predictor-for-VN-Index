from __future__ import annotations
import torch
from torch import nn
from .experts import ScaleExpert
from .gate import HorizonGate
from .heads import MonotonicQuantileHead

class MSDP(nn.Module):
    def __init__(self,n_features,horizons=(5,20,60),return_quantiles=(.05,.25,.5,.75,.95),mdd_quantiles=(.1,.5,.9),hidden_dim=64,latent_dim=48,n_blocks=2,dropout=.1,gate_temperature=1.,medium_pool=5,long_pool=10,range_indices=None,ablation="full"):
        super().__init__(); self.horizons=list(horizons); self.return_quantiles=list(return_quantiles); self.mdd_quantiles=list(mdd_quantiles); self.ablation=ablation
        specs=[(63,1,None),(126,medium_pool,None),(252,long_pool,None),(126,3,range_indices or list(range(n_features)))]
        if ablation=="no_range": specs=specs[:3]
        if ablation=="single": specs=specs[:1]
        self.experts=nn.ModuleList([ScaleExpert(n_features,hidden_dim,latent_dim,w,p,n_blocks,dropout,ix) for w,p,ix in specs])
        self.gate=HorizonGate(latent_dim,n_features,len(horizons),len(specs),gate_temperature,ablation!="shared_gate")
        self.ret=MonotonicQuantileHead(latent_dim,len(return_quantiles)); self.mdd=MonotonicQuantileHead(latent_dim,len(mdd_quantiles))
        self.direction=nn.Linear(latent_dim,1); self.volatility=nn.Linear(latent_dim,1)
    def forward(self,x):
        lat=torch.stack([e(x) for e in self.experts],1)
        weights=self.gate(lat,x[:,-1])
        if self.ablation=="equal": weights=torch.ones_like(weights)/weights.shape[-1]
        fused=torch.einsum("bhk,bkd->bhd",weights,lat)
        return {"return_quantiles":self.ret(fused),"direction_prob":torch.sigmoid(self.direction(fused).squeeze(-1)),"mdd_quantiles":self.mdd(fused),"volatility":torch.nn.functional.softplus(self.volatility(fused).squeeze(-1)),"gate_weights":weights,"expert_latents":lat}
