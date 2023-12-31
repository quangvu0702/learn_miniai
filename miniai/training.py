# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_minibatch_training.ipynb.

# %% auto 0
__all__ = ['def_device', 'accuracy', 'report', 'Dataset', 'get_dls', 'fit', 'to_device', 'collate_device']

# %% ../nbs/04_minibatch_training.ipynb 1
import gzip, pickle
from pathlib import Path
from urllib.request import urlretrieve
import torch
from torch.utils.data import DataLoader, default_collate
from torch import tensor

# %% ../nbs/04_minibatch_training.ipynb 31
def accuracy(pred, yb): return (pred.argmax(1) == yb).float().mean()

# %% ../nbs/04_minibatch_training.ipynb 32
def report(loss, pred, yb): print(f"Loss {loss:.2f} and accuracy: {accuracy(pred, yb):.1%}")

# %% ../nbs/04_minibatch_training.ipynb 46
class Dataset():
    def __init__(self, x, y): self.x, self.y = x, y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i], self.y[i]

# %% ../nbs/04_minibatch_training.ipynb 86
def get_dls(train_ds, val_ds, bs, collate_fn=default_collate, **kwargs):
    train_dl = DataLoader(train_ds, batch_size=bs, drop_last=False, shuffle=True, collate_fn=collate_fn, **kwargs)
    val_dl   = DataLoader(val_ds,   batch_size=bs*2, drop_last=False, shuffle=True, collate_fn=collate_fn, **kwargs)
    return train_dl, val_dl

# %% ../nbs/04_minibatch_training.ipynb 88
def fit(epoch, model, loss_func, opt, train_dl, val_dl):
    for _ in range(epoch):
        for xb, yb in train_dl:
            pred = model(xb)
            loss = loss_func(pred, yb)
            loss.backward()
            opt.step()
            opt.zero_grad()
        model.eval()
        with torch.no_grad():
            tot_loss, tot_acc = 0, 0
            for xb, yb in val_dl:
                pred = model(xb)
                loss = loss_func(pred, yb)
                tot_loss += loss.item()
                tot_acc += (pred.argmax(1) == yb).float().sum().item()
            print(f"Loss {tot_loss/len(val_dl.dataset):.4f}. Acc = {tot_acc/len(val_dl.dataset):.2f}")

# %% ../nbs/04_minibatch_training.ipynb 91
from typing import Mapping

def_device = 'cuda' if torch.cuda.is_available() else 'cpu'

def to_device(x):
    if isinstance(x, torch.Tensor): return x.to(def_device)
    if isinstance(x, Mapping): return {k: v.to(def_device) for k,v in x.items()}
    return type(x)(o.to(def_device) for o in x)

def collate_device(b): return to_device(default_collate(b))
