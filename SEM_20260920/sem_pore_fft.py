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

def load(n):
    m = meta_of(n)
    px = float(m["$CM_PIXEL_SIZE"].split("nm")[0]); mag = int(m["$CM_MAG"])
    barh = int(m.get("$SM_PNU_HEIGHT","132"))
    full = np.array(Image.open(os.path.join(SRC, f"{n}.tif")).convert("L")).astype(np.float32)
    return full[:full.shape[0]-barh, :], px, mag

def pores(n):
    img, px, mag = load(n)
    sm = ndi.gaussian_filter(img, 2.0)
    fg = sm > otsu(sm)
    if fg.mean() > 0.65 or fg.mean() < 0.05: fg = ~fg      # 纤维=前景
    fg = ndi.binary_opening(fg, np.ones((3,3)))            # 去噪，不闭运算（保留孔）
    void = ~fg
    lab, nlab = ndi.label(void)                            # 8 连通
    border = set(np.unique(np.r_[lab[0,:], lab[-1,:], lab[:,0], lab[:,-1]]))
    areas, closed, open_ = [], 0, 0
    for i in range(1, nlab+1):
        a = int((lab == i).sum())
        if i in border: open_ += 1
        else:
            closed += 1; areas.append(a)
    areas = np.array(areas, float) * (px**2)               # nm^2
    d_eq = 2*np.sqrt(areas/np.pi)/1000.0                   # μm
    area_um2 = img.size * px**2 / 1e6
    return dict(img=f"{n}.tif", mag=mag, nm_px=px,
        void_fraction=round(float(void.mean()),3),
        pores_closed=closed, pores_open=open_,
        pores_per_100um2=round(closed/area_um2*100,1),
        d_eq_med_um=round(float(np.median(d_eq)),3) if d_eq.size else None,
        d_eq_iqr_um=[round(float(np.percentile(d_eq,25)),3), round(float(np.percentile(d_eq,75)),3)] if d_eq.size else None,
        d_eq_p90_um=round(float(np.percentile(d_eq,90)),3) if d_eq.size else None)

def groove_spacing(n, pmin=30.0, pmax=1200.0):
    img, px, mag = load(n)
    h, w = img.shape
    cy, cx = h//2, w//2; s = min(h, w)//2
    crop = img[cy-s:cy+s, cx-s:cx+s]
    hp = crop - ndi.gaussian_filter(crop, 8)               # 高通：只留条纹纹理
    win = np.outer(np.hanning(hp.shape[0]), np.hanning(hp.shape[1]))
    F = np.fft.fftshift(np.abs(np.fft.fft2(hp*win))**2)
    yy, xx = np.mgrid[-s:s, -s:s]
    r = np.sqrt(yy**2 + xx**2).astype(int)
    prof = np.bincount(r.ravel(), F.ravel()) / np.maximum(np.bincount(r.ravel()), 1)
    rmin, rmax = int(w/(2*pmax/px)), int(w/(2*pmin/px))    # 周期 p → 半径 w/(2p)
    rmin, rmax = max(rmin,1), min(rmax, len(prof)-1)
    band = prof[rmin:rmax]
    if band.size == 0: return None
    k = int(np.argmax(band)) + rmin
    period_nm = w*px/(2*max(k,1))
    fig, ax = plt.subplots(1,2, figsize=(11,3.6))
    ax[0].imshow(crop, cmap="gray"); ax[0].set_title(f"{n}.tif {mag}x crop"); ax[0].axis("off")
    ax[1].plot(np.arange(len(prof))*w*px/(2*np.maximum(np.arange(len(prof)),1)), prof)
    ax[1].set_xscale("log"); ax[1].set_xlabel("spatial period (nm)"); ax[1].set_ylabel("power")
    ax[1].axvline(period_nm, color="r", ls="--"); ax[1].set_title(f"peak {period_nm:.0f} nm")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"fft_{n}.png"), dpi=100); plt.close()
    return dict(img=f"{n}.tif", mag=mag, nm_px=px, groove_period_nm=round(period_nm,1))

print("=== 孔隙 ===")
for n in (1,2,3,4,5,6,7,8,9,10,11,12): print(json.dumps(pores(n), ensure_ascii=False))
print("=== 沟槽间距（FFT 主周期）===")
for n in (1,2,3,7,8,9,4,10): 
    r = groove_spacing(n)
    if r: print(json.dumps(r, ensure_ascii=False))
