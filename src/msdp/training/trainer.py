from __future__ import annotations
import copy
import numpy as np
import torch
from torch.utils.data import DataLoader
from ..losses import multitask_loss

def train_model(model,train_ds,val_ds,cfg,device="cpu"):
    model.to(device); tc=cfg["training"]; opt=torch.optim.AdamW(model.parameters(),lr=tc["learning_rate"],weight_decay=tc["weight_decay"])
    train=DataLoader(train_ds,batch_size=tc["batch_size"],shuffle=True); val=DataLoader(val_ds,batch_size=tc["batch_size"],shuffle=False)
    best=float("inf"); state=None; patience=0; history=[]
    for epoch in range(tc["epochs"]):
        model.train(); tl=[]
        for x,y,_ in train:
            x=x.to(device); y=y.to(device); opt.zero_grad(); out=model(x); loss,_=multitask_loss(out,y,cfg["horizons"],cfg["quantiles"],cfg["mdd_quantiles"],cfg["loss_weights"]); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1); opt.step(); tl.append(loss.item())
        model.eval(); vl=[]
        with torch.no_grad():
            for x,y,_ in val:
                loss,_=multitask_loss(model(x.to(device)),y.to(device),cfg["horizons"],cfg["quantiles"],cfg["mdd_quantiles"],cfg["loss_weights"]); vl.append(loss.item())
        score=float(np.mean(vl)); history.append({"epoch":epoch+1,"train_loss":float(np.mean(tl)),"validation_loss":score})
        if score<best: best=score; state=copy.deepcopy(model.state_dict()); patience=0
        else: patience+=1
        if patience>=tc["patience"]: break
    model.load_state_dict(state); return model,history

def predict(model,ds,batch_size=256,device="cpu"):
    model.eval(); bags={}; indices=[]
    with torch.no_grad():
        for x,_,ix in DataLoader(ds,batch_size=batch_size,shuffle=False):
            out=model(x.to(device)); indices.extend(ix.numpy().tolist())
            for k,v in out.items():
                if k!="expert_latents": bags.setdefault(k,[]).append(v.cpu().numpy())
    return {k:np.concatenate(v) for k,v in bags.items()},np.asarray(indices)

