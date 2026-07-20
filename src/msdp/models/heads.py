import torch
from torch import nn

class MonotonicQuantileHead(nn.Module):
    def __init__(self,d,nq): super().__init__(); self.base=nn.Linear(d,1); self.inc=nn.Linear(d,nq-1)
    def forward(self,x):
        base=self.base(x); increments=torch.nn.functional.softplus(self.inc(x)); return torch.cat([base,base+torch.cumsum(increments,-1)],-1)

