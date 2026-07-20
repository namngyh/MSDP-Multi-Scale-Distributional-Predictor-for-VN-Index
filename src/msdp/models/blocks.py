import torch
from torch import nn

class ResidualBlock(nn.Module):
    def __init__(self, channels, dropout=.1):
        super().__init__(); self.net=nn.Sequential(nn.Conv1d(channels,channels,3,padding=1),nn.GELU(),nn.Dropout(dropout),nn.Conv1d(channels,channels,3,padding=1)); self.norm=nn.LayerNorm(channels)
    def forward(self,x): return self.norm((x+self.net(x)).transpose(1,2)).transpose(1,2)

