"""Sample candidate symbols from the procedural terrains and filter them
against the brief's rules (grid ≤ 8×8, 8–24 cells, one connected form,
asymmetric, a small summit). Output: contact sheets for designer selection."""
import numpy as np, json, cairosvg, io
from PIL import Image
from terrain import massif

PAL = dict(basalt="#0E2423", moss="#2E4B43", sage="#6F8E7A", lichen="#D6E65D", chalk="#F4F5EF", flag="#EC5D2F")
LV = {1: PAL["sage"], 2: PAL["lichen"], 3: PAL["chalk"]}

def components(mask):
    h, w = mask.shape; seen = np.zeros_like(mask, bool); n = 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not seen[y, x]:
                n += 1; st = [(y, x)]; seen[y, x] = True
                while st:
                    cy, cx = st.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True; st.append((ny, nx))
    return n

def plan_candidates(E, seed):
    out = []
    H, W = E.shape
    # local summits
    from numpy.lib.stride_tricks import sliding_window_view
    k = 41; pad = k // 2
    Ep = np.pad(E, pad, mode="edge")
    mx = sliding_window_view(Ep, (k, k)).max(axis=(2, 3))
    peaks = np.argwhere((E == mx) & (E > np.quantile(E, 0.80)))
    for (py, px) in peaks[:400]:
        for win in (48, 64, 80, 96, 128):
            for N in (6, 7, 8):
                y0, x0 = py - win // 2, px - win // 2
                if y0 < 0 or x0 < 0 or y0 + win > H or x0 + win > W: continue
                sub = E[y0:y0 + win, x0:x0 + win]
                cells = np.asarray(Image.fromarray(sub.astype(np.float32), mode="F").resize((N, N), Image.BOX))
                lo, hi = cells.min(), cells.max()
                if hi - lo < 1e-6: continue
                v = (cells - lo) / (hi - lo)
                for t in (0.35, 0.45, 0.55):
                    q = np.zeros_like(v, int)
                    q[v >= t] = 1; q[v >= t + (1 - t) * 0.45] = 2; q[v >= t + (1 - t) * 0.85] = 3
                    m = q > 0; n = int(m.sum())
                    if not (10 <= n <= 24): continue
                    if components(m) != 1: continue
                    if (q == 3).sum() not in (1, 2, 3): continue
                    rows = np.where(m.any(1))[0]; cols = np.where(m.any(0))[0]
                    if len(rows) < 4 or len(cols) < 5: continue
                    sym = min((m != np.fliplr(m)).sum(), (m != np.flipud(m)).sum(), (m != m.T).sum())
                    if sym < 4: continue
                    fill = n / (len(rows) * len(cols))
                    if fill > 0.8: continue
                    q = q[rows.min():rows.max() + 1, cols.min():cols.max() + 1]
                    out.append(dict(kind="plan", seed=seed, q=q.tolist(), n=n, fill=round(fill, 2)))
    return out

def ridge_candidates(E, seed, rng):
    out = []; H, W = E.shape
    for _ in range(1500):
        N = int(rng.choice([7, 8])); R = int(rng.choice([5, 6]))
        L = int(rng.integers(120, 420)); ang = rng.uniform(-0.6, 0.6)
        cx, cy = rng.integers(60, W - 60), rng.integers(60, H - 60)
        xs = cx + np.cos(ang) * np.linspace(-L / 2, L / 2, N * 6); ys = cy + np.sin(ang) * np.linspace(-L / 2, L / 2, N * 6)
        if xs.min() < 0 or ys.min() < 0 or xs.max() >= W or ys.max() >= H: continue
        prof = E[ys.astype(int), xs.astype(int)].reshape(N, 6).max(1)
        lo, hi = prof.min(), prof.max()
        if hi - lo < 0.15: continue
        lv = np.round((prof - lo) / (hi - lo) * (R - 1)).astype(int)
        top = int(np.argmax(lv))
        if top in (0, N - 1) or (lv == R - 1).sum() != 1: continue
        if abs(top - (N - 1) / 2) < 0.6: continue                    # summit off-centre
        g = np.zeros((R, N), int)
        for i, l in enumerate(lv):
            g[R - 1 - l, i] = 1
            if i:                                                    # connect large jumps
                a, b = sorted((lv[i - 1], l))
                for k in range(a + 1, b): g[R - 1 - k, i if l > lv[i - 1] else i - 1] = 1
        n = int(g.sum())
        if n > 14: continue
        q = np.where(g > 0, 1, 0)
        for r in range(R):                                            # colour by height band
            q[r][g[r] > 0] = 3 if r == 0 else (2 if r <= R // 2 - 1 else 1)
        out.append(dict(kind="ridge", seed=seed, q=q.tolist(), n=n))
    return out

def cell_svg(q, size, mono=None, bg=PAL["basalt"], gap=0.0):
    q = np.array(q); R, C = q.shape; u = size / max(R, C)
    ox = (size - C * u) / 2; oy = (size - R * u) / 2
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" fill="{bg}"/>']
    for r in range(R):
        for c in range(C):
            if q[r, c]:
                col = mono or (PAL["flag"] if q[r, c] == 9 else LV[q[r, c]])
                s.append(f'<rect x="{ox + c*u + gap:.2f}" y="{oy + r*u + gap:.2f}" width="{u - 2*gap:.2f}" height="{u - 2*gap:.2f}" fill="{col}"/>')
    s.append("</svg>"); return "".join(s)

def sheet(cands, path, cols=12, cell=110):
    rows = (len(cands) + cols - 1) // cols
    img = Image.new("RGB", (cols * (cell * 2 + 30), rows * (cell + 30)), "#d9d9d6")
    for i, c in enumerate(cands):
        x = (i % cols) * (cell * 2 + 30) + 10; y = (i // cols) * (cell + 30) + 10
        a = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=cell_svg(c["q"], cell).encode())))
        b = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=cell_svg(c["q"], cell, mono=PAL["basalt"], bg=PAL["chalk"]).encode())))
        img.paste(a, (x, y)); img.paste(b, (x + cell + 4, y))
    img.save(path)

if __name__ == "__main__":
    rng = np.random.default_rng(3)
    allp, allr = [], []
    for seed in (5, 11, 23, 37):
        E = np.load(f"assets/dem-{seed}.npy")
        allp += plan_candidates(E, seed); allr += ridge_candidates(E, seed, rng)
    # de-duplicate identical shapes
    def key(c): return json.dumps(c["q"])
    up = list({key(c): c for c in allp}.values()); ur = list({key(c): c for c in allr}.values())
    rng.shuffle(up); rng.shuffle(ur)
    print("plan", len(allp), "unique", len(up), "| ridge", len(allr), "unique", len(ur))
    json.dump(up[:96], open("explore/plan.json", "w")); json.dump(ur[:72], open("explore/ridge.json", "w"))
    sheet(up[:96], "explore/plan-sheet.png"); sheet(ur[:72], "explore/ridge-sheet.png")
