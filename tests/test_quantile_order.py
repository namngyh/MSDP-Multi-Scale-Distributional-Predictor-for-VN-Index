import torch
from msdp.models import MSDP
def test_order():
    o=MSDP(4,hidden_dim=8,latent_dim=8)(torch.randn(3,252,4)); assert (o["return_quantiles"].diff(dim=-1)>=0).all(); assert (o["mdd_quantiles"].diff(dim=-1)>=0).all()

