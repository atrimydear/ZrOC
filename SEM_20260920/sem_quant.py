import numpy as np, os, json
from PIL import Image
from scipy import ndimage

SRC = r"C:\Users\ATRI\Desktop\20260920\20260920"

def otsu(g):
    h,_ = np.histogram(g, bins=256, range=(0,255)); h = h.astype(float)
    w0 = np.cumsum(h); w1 = h.sum()-w0; i = np.arange(256); m0 = np.cumsum(h*i); mt = m0[-1]
    with np.errstate(invalid="ignore", divide="ignore"):
        v = w0*w1*((m0/w0)-((mt-m0)/w1))**2
    return int(np.nanargmax(v))

def runwidth(mask, px_nm):
    """扫描线断宽法：逐行/逐列取连续前景段宽度，取物理合理区间内的中位数"""
    widths = []
    for arr in (mask, mask.T):
        for line in arr:
            idx = np.flatnonzero(np.diff(np.r_[0, line.view(np.int8), 0]))
            starts, ends = idx[0::2], idx[1::2]
            widths.extend((ends-starts).tolist())
    w = np.array(widths, dtype=float) * px_nm
    w = w[(w >= 50) & (w <= 3000)]          # 50 nm - 3 um 视为纤维截面
    return w

def analyze(n):
    meta = {}
    for line in open(os.path.join(SRC, f"{n}.txt"), encoding="utf-8", errors="ignore"):
        p = line.split(None,1)
        if len(p)==2: meta[p[0]] = p[1].strip()
    px = float(meta["$CM_PIXEL_SIZE"].split("nm")[0]); mag = int(meta["$CM_MAG"])
    bar = int(meta.get("$SM_PNU_HEIGHT", "132"))
    img = np.array(Image.open(os.path.join(SRC, f"{n}.tif")).convert("L")).astype(np.float32)
    img = img[:img.shape[0]-bar, :]          # 裁掉底部信息栏
    thr = otsu(img)
    bright = img > thr
    # 选“少数类且更细长”的一类做前景
    def score(m):
        dt = ndimage.distance_transform_edt(m)
        return float(np.median(dt[m])) if m.any() else 1e9
    fg = bright if score(bright) < score(~bright) else ~bright
    fg = ndimage.binary_opening(fg, np.ones((3,3)))
    w = runwidth(fg, px)
    dt = ndimage.distance_transform_edt(fg)
    ridge = (dt >= ndimage.maximum_filter(dt, 5)-1e-6) & (dt > 2)
    d_ridge = 2*dt[ridge]*px
    return dict(img=f"{n}.tif", mag=mag, nm_px=px, thr=thr,
                fg_frac=round(float(fg.mean()),3),
                n_runs=int(w.size),
                run_p25_um=round(float(np.percentile(w,25))/1000,3) if w.size else None,
                run_med_um=round(float(np.median(w))/1000,3) if w.size else None,
                run_p75_um=round(float(np.percentile(w,75))/1000,3) if w.size else None,
                ridge_med_um=round(float(np.median(d_ridge))/1000,3) if d_ridge.size else None)

for n in (1,2,3,4,5,6,7,9,10,11,12):
    print(json.dumps(analyze(n), ensure_ascii=False))
