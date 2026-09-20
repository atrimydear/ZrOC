import numpy as np, os, json
from PIL import Image
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = r"C:\Users\ATRI\Desktop\20260920\20260920"
OUT = r"D:\Knowledge\LaTeX\实验计划\SEM_20260920\analysis"
os.makedirs(OUT, exist_ok=True)

def otsu(gray):
    hist,_ = np.histogram(gray, bins=256, range=(0,255)); hist = hist.astype(float)
    w0 = np.cumsum(hist); w1 = hist.sum()-w0; idx = np.arange(256); m0 = np.cumsum(hist*idx); mt = m0[-1]
    with np.errstate(invalid="ignore", divide="ignore"):
        var = w0*w1*((m0/w0)-((mt-m0)/w1))**2
    return int(np.nanargmax(var))

def run(n):
    meta = {}
    for line in open(os.path.join(SRC, f"{n}.txt"), encoding="utf-8", errors="ignore"):
        p = line.split(None,1)
        if len(p)==2: meta[p[0]] = p[1].strip()
    px = float(meta["$CM_PIXEL_SIZE"].split("nm")[0]); mag = int(meta["$CM_MAG"])
    img = np.array(Image.open(os.path.join(SRC, f"{n}.tif")).convert("L")).astype(np.float32)
    H,W = img.shape
    thr = otsu(img); m1 = img > thr
    fg = m1 if m1.mean() < 0.5 else ~m1
    void = 1.0 - fg.mean()
    dt = ndimage.distance_transform_edt(fg)
    ridge = (dt >= ndimage.maximum_filter(dt, size=7)-1e-6) & (dt > 2.5)
    diam_nm = 2*dt[ridge]*px
    h16, w16 = H//16*16, W//16*16
    blocks = fg[:h16,:w16].reshape(16,h16//16,16,w16//16).mean(axis=(1,3))
    lap = ndimage.laplace(img)
    res = dict(img=f"{n}.tif", size=f"{W}x{H}", mag=mag, nm_px=px, thr=thr,
               void=round(float(void),4), ridge_pts=int(ridge.sum()),
               d_mean_um=round(float(diam_nm.mean()/1000),3) if diam_nm.size else None,
               d_med_um=round(float(np.median(diam_nm)/1000),3) if diam_nm.size else None,
               d_std_um=round(float(diam_nm.std()/1000),3) if diam_nm.size else None,
               coverCV=round(float(blocks.std()/max(blocks.mean(),1e-9)),3),
               lapVar=round(float(lap.var()),0), gray_mean=round(float(img.mean()),1))
    fig, ax = plt.subplots(1,3, figsize=(15,4.2))
    ax[0].imshow(img, cmap="gray"); ax[0].set_title(f"{n}.tif  {mag}x  {W}x{H}"); ax[0].axis("off")
    ax[1].imshow(fg, cmap="gray"); ax[1].set_title(f"mask  void={void:.3f}"); ax[1].axis("off")
    if diam_nm.size: ax[2].hist(diam_nm/1000, bins=40); ax[2].set_xlabel("diameter (um)"); ax[2].set_title("ridge-based diameter")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"analysis_{n}.png"), dpi=110); plt.close()
    return res

rows = [run(n) for n in (1,2,3,4,5,7,8,9,10,11,12)]
print(json.dumps(rows, ensure_ascii=False))
