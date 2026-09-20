import numpy as np, os, json
from PIL import Image
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = r"C:\Users\ATRI\Desktop\20260920\20260920"
OUT = r"D:\Knowledge\LaTeX\实验计划\SEM_20260920\analysis2"
os.makedirs(OUT, exist_ok=True)

def meta_of(n):
    m = {}
    for line in open(os.path.join(SRC, f"{n}.txt"), encoding="utf-8", errors="ignore"):
        p = line.split(None,1)
        if len(p)==2: m[p[0]] = p[1].strip()
    return m

def otsu(g):
    h,_ = np.histogram(g, bins=256, range=(0,255)); h = h.astype(float)
    w0 = np.cumsum(h); w1 = h.sum()-w0; i = np.arange(256); m0 = np.cumsum(h*i); mt = m0[-1]
    with np.errstate(invalid="ignore", divide="ignore"):
        v = w0*w1*((m0/w0)-((mt-m0)/w1))**2
    return float(np.nanargmax(v))

def analyze(n, sigma=3.0, close_r=3):
    m = meta_of(n)
    px = float(m["$CM_PIXEL_SIZE"].split("nm")[0]); mag = int(m["$CM_MAG"])
    bar_expect = int(m["$SM_MICRON_BAR"]); marker = m["$SM_MICRON_MARKER"]
    barh = int(m.get("$SM_PNU_HEIGHT", "132"))
    full = np.array(Image.open(os.path.join(SRC, f"{n}.tif")).convert("L")).astype(np.float32)
    H, W = full.shape
    info = full[H-barh:, :]; img = full[:H-barh, :]

    runs = []
    for row in (info > 200):
        idx = np.flatnonzero(np.diff(np.r_[0, row.view(np.int8), 0]))
        runs += (idx[1::2] - idx[0::2]).tolist()
    bar_meas = int(max(runs)) if runs else None

    sm = ndi.gaussian_filter(img, sigma)
    thr = otsu(sm); fg = sm > thr
    if fg.mean() > 0.65 or fg.mean() < 0.05: fg = ~fg
    fg = ndi.binary_closing(fg, structure=np.ones((2*close_r+1,)*2))
    fg = ndi.binary_opening(fg, structure=np.ones((5,5)))
    lab, nlab = ndi.label(fg)
    if nlab:
        sizes = np.bincount(lab.ravel()); sizes[0]=0
        fg = sizes[lab] > 300

    dt = ndi.distance_transform_edt(fg)
    ridge = (dt >= ndi.maximum_filter(dt,5)-1e-6) & (dt > 2.0)
    d = 2*dt[ridge]*px; d = d[(d>100)&(d<3000)]
    ws = []
    for arr in (fg, fg.T):
        for line in arr:
            idx = np.flatnonzero(np.diff(np.r_[0, line.view(np.int8), 0]))
            ws += (idx[1::2]-idx[0::2]).tolist()
    w = np.array(ws,float)*px; w = w[(w>100)&(w<3000)]

    res = dict(img=f"{n}.tif", mag=mag, nm_px=px, bar_expect=bar_expect, bar_measured=bar_meas, marker=marker,
               fg_frac=round(float(fg.mean()),3),
               lens_med_um=round(float(np.median(d))/1000,3) if d.size else None,
               lens_iqr=[round(float(np.percentile(d,25))/1000,3), round(float(np.percentile(d,75))/1000,3)] if d.size else None,
               run_med_um=round(float(np.median(w))/1000,3) if w.size else None,
               ridge_n=int(d.size))
    fig, ax = plt.subplots(1,2, figsize=(13,5))
    ax[0].imshow(img, cmap="gray"); ax[0].set_title(f"{n}.tif {mag}x bar {bar_meas}/{bar_expect}px"); ax[0].axis("off")
    ax[1].imshow(img, cmap="gray"); ax[1].contour(fg, levels=[.5], colors="r", linewidths=.6)
    if d.size:
        ys,xs = np.nonzero(ridge); ax[1].scatter(xs[::7], ys[::7], s=1.5, c="cyan", alpha=.25)
    ax[1].set_title(f"seg fg={fg.mean():.2f}"); ax[1].axis("off")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"seg_{n}.png"), dpi=100); plt.close()
    return res

for n in (1,2,3,4,5,6,7,8,9,10,11,12):
    print(json.dumps(analyze(n), ensure_ascii=False))
