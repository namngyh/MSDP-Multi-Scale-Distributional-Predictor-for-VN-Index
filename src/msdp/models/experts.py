import torch
from torch import nn
from .blocks import ResidualBlock

class ScaleExpert(nn.Module):
    def __init__(self,n_features,hidden,latent,window,pool=1,n_blocks=2,dropout=.1,feature_indices=None):
        super().__init__(); self.window=window; self.pool=pool; self.register_buffer("feature_indices",torch.tensor(feature_indices or list(range(n_features)),dtype=torch.long))
        n_in=len(feature_indices or list(range(n_features))); self.proj=nn.Conv1d(n_in,hidden,3,padding=1)
        self.blocks=nn.Sequential(*[ResidualBlock(hidden,dropout) for _ in range(n_blocks)])
        self.out=nn.Sequential(nn.AdaptiveAvgPool1d(1),nn.Flatten(),nn.Linear(hidden,latent),nn.LayerNorm(latent),nn.GELU())
    def forward(self,x):
        x=x[:,-self.window:,self.feature_indices].transpose(1,2)
        if self.pool>1: x=torch.nn.functional.avg_pool1d(x,self.pool,self.pool)
        return self.out(self.blocks(self.proj(x)))

ShortScaleExpert=MediumScaleExpert=LongScaleExpert=RangeVolatilityExpert=ScaleExpert

