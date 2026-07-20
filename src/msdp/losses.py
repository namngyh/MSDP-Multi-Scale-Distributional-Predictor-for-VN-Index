import torch

def pinball(pred,target,quantiles):
    e=target.unsqueeze(-1)-pred; q=torch.as_tensor(quantiles,device=pred.device,dtype=pred.dtype); return torch.maximum(q*e,(q-1)*e).mean()

def multitask_loss(out,y,horizons,qr,qm,weights):
    h=len(horizons); ret=y[:,:h]; direction=y[:,h:2*h]; mdd=y[:,2*h:3*h]; vol=y[:,3*h:4*h]
    losses={"return":pinball(out["return_quantiles"],ret,qr),"direction":torch.nn.functional.binary_cross_entropy(out["direction_prob"],direction),"mdd":pinball(out["mdd_quantiles"],mdd,qm),"volatility":torch.nn.functional.l1_loss(out["volatility"],vol)}
    entropy=-(out["gate_weights"]*torch.log(out["gate_weights"].clamp_min(1e-8))).sum(-1).mean(); losses["gate_entropy"]=-entropy
    return sum(weights.get(k,1)*v for k,v in losses.items()),losses

