"""S1 candidates: one closed contour around a summit, rasterised to ≤8×8 cells,
with the summit cell inside. Sampled from the procedural terrains."""
import numpy as np, json
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view
from explore import components, sheet

def ring_from(v, t):
    blob = v >= t
    if components(blob) != 1: return None
    edge = np.zeros_like(blob)
    h, w = blob.shape
    for y in range(h):
        for x in range(w):
            if blob[y, x]:
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = y+dy, x+dx
                    if not (0 <= ny < h and 0 <= nx < w) or not blob[ny, nx]:
                        edge[y, x] = True; break
    inner = blob & ~edge
    return blob, edge, inner

out = []
for seed in (5, 11, 23, 37):
    E = np.load(f"assets/dem-{seed}.npy"); H, W = E.shape
    k = 31; Ep = np.pad(E, k // 2, mode="edge")
    mx = sliding_window_view(Ep, (k, k)).max(axis=(2, 3))
    peaks = np.argwhere((E == mx) & (E > np.quantile(E, 0.7)))
    for (py, px) in peaks:
        for win in (40, 56, 72, 96):
            for N in (7, 8):
                y0, x0 = py - win // 2, px - win // 2
                if y0 < 0 or x0 < 0 or y0 + win > H or x0 + win > W: continue
                sub = E[y0:y0+win, x0:x0+win]
                v = np.asarray(Image.fromarray(sub.astype(np.float32), mode="F").resize((N, N), Image.BOX))
                v = (v - v.min()) / (v.max() - v.min() + 1e-9)
                for t in (0.3, 0.4, 0.5, 0.6):
                    r = ring_from(v, t)
                    if r is None: continue
                    blob, edge, inner = r
                    n = int(edge.sum())
                    if not (11 <= n <= 20) or inner.sum() < 2: continue
                    if components(edge) != 1: continue
                    # ring must be closed: interior not touching the frame
                    if inner[0].any() or inner[-1].any() or inner[:, 0].any() or inner[:, -1].any(): continue
                    if edge[0].sum() == N or edge[:, 0].sum() == N: continue
                    sym = min((edge != np.fliplr(edge)).sum(), (edge != np.flipud(edge)).sum())
                    if sym < 4: continue
                    q = np.where(edge, 2, 0)
                    iy, ix = np.unravel_index(np.argmax(np.where(inner, v, -1)), v.shape)
                    q[iy, ix] = 3
                    rows = np.where(blob.any(1))[0]; cols = np.where(blob.any(0))[0]
                    q = q[rows.min():rows.max()+1, cols.min():cols.max()+1]
                    out.append(dict(kind="contour", seed=seed, q=q.tolist(), n=n + 1))
u = list({json.dumps(c["q"]): c for c in out}.values())
np.random.default_rng(4).shuffle(u)
print("contour candidates", len(out), "unique", len(u))
json.dump(u[:72], open("explore/contour.json", "w")); sheet(u[:72], "explore/contour-sheet.png")
