import torch
from torch import nn

class HorizonGate(nn.Module):
    def __init__(self,latent,n_features,n_horizons,n_experts=4,temperature=1.0,horizon_dependent=True):
        super().__init__(); self.temperature=temperature; self.horizon_dependent=horizon_dependent
        self.embedding=nn.Embedding(n_horizons,latent); self.score=nn.Linear(latent*2+n_features,1)
    def forward(self,latents,context):
        b,k,d=latents.shape; h=self.embedding.num_embeddings; outs=[]
        for j in range(h):
            e=self.embedding.weight[j if self.horizon_dependent else 0].expand(b,k,-1); c=context[:,None,:].expand(-1,k,-1)
            outs.append(self.score(torch.cat([latents,e,c],-1)).squeeze(-1))
        return torch.softmax(torch.stack(outs,1)/self.temperature,dim=-1)

