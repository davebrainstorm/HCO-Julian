"""Pixel HCO — wordmark drawn on a pixel grid tied to the module.
p = pixel size in units (M/2, M/3, M/4…). Stroke = 1M = M/p pixels. Cap = 5M.
Round letters are stepped with 1-pixel stairs; the inner stair is set so the
45° stroke keeps (≈) the straight-stroke thickness."""
import math, numpy as np, sys
sys.path.insert(0, "../geometry")
from glyphs import rect as prect, union, svg_d
M, CAP = 200, 1000

def H_px(n, w, s, bar0):
    g = np.zeros((n, w), bool); g[:, :s] = True; g[:, w - s:] = True; g[bar0:bar0 + s, :] = True; return g
def O_px(n, w, s, c, cin=None):
    """n rows × w cols ring of stroke s; outer corners cut by c stairs, inner by cin stairs."""
    cin = max(0, round(c - s * (2 - math.sqrt(2)))) if cin is None else cin
    y, x = np.mgrid[0:n, 0:w]
    def cut(xx, yy, ww, hh, k):      # True inside a rectangle with k-stair corners
        inside = (xx >= 0) & (xx < ww) & (yy >= 0) & (yy < hh)
        if k == 0: return inside
        dx = np.minimum(xx, ww - 1 - xx); dy = np.minimum(yy, hh - 1 - yy)
        return inside & (dx + dy >= k)
    outer = cut(x, y, w, n, c); inner = cut(x - s, y - s, w - 2 * s, n - 2 * s, cin)
    return outer & ~inner
def C_px(n, w, s, c, a0, a1, open_x=None, cin=None):
    g = O_px(n, w, s, c, cin); ox = w - s - 1 if open_x is None else open_x
    g[a0:a1 + 1, ox:] = False; return g

def to_path(g, p, x0=0):
    """Merge pixels into one clean outline (union of row runs)."""
    rs = []
    for j, row in enumerate(g):
        i = 0
        while i < len(row):
            if row[i]:
                k = i
                while k < len(row) and row[k]: k += 1
                rs.append(prect(x0 + i * p, CAP - (j + 1) * p, (k - i) * p, p)); i = k
            else: i += 1
    return union(*rs)

def wordmark(p=100, wH=8, wC=9, wO=10, c=2, gaps=(1, 1), bar_top=200, cinC=None, cinO=None, ap=(300, 700)):
    n = round(CAP / p); s = round(M / p)
    h = H_px(n, wH, s, round(bar_top / p))
    cc = C_px(n, wC, s, c, round(ap[0] / p), round(ap[1] / p) - 1, cin=cinC)
    o = O_px(n, wO, s, c, cinO)
    xs = [0, (wH + gaps[0]) * p, (wH + gaps[0] + wC + gaps[1]) * p]
    path = union(to_path(h, p, xs[0]), to_path(cc, p, xs[1]), to_path(o, p, xs[2]))
    return path, (wH + gaps[0] + wC + gaps[1] + wO) * p, dict(H=h, C=cc, O=o, xs=xs, p=p, n=n, s=s)

# ---- HCO Pixel Numerals: tabular, 8 × 10 px, same pen as the wordmark ----
_D = {
"0": """..####..|.######.|###..###|##....##|##....##|##....##|##....##|###..###|.######.|..####..""",
"1": """..####..|..####..|....##..|....##..|....##..|....##..|....##..|....##..|....##..|....##..""",
"2": """..####..|.######.|###..###|##....##|.....###|...####.|.####...|###.....|########|########""",
"3": """..####..|.######.|###..###|......##|...####.|...####.|......##|###..###|.######.|..####..""",
"4": """##...##.|##...##.|##...##.|##...##.|##...##.|########|########|.....##.|.....##.|.....##.""",
"5": """########|########|##......|##......|######..|#######.|.....###|###..###|.######.|..####..""",
"6": """..####..|.######.|###..###|##......|######..|#######.|##...###|###..###|.######.|..####..""",
"7": """########|########|.....###|....###.|...###..|..###...|..##....|..##....|..##....|..##....""",
"8": """..####..|.######.|###..###|.######.|.######.|###..###|##....##|###..###|.######.|..####..""",
}
_D["9"] = "|".join(r[::-1] for r in _D["6"].split("|")[::-1])
DIGITS = {k: np.array([[c == "#" for c in r] for r in v.split("|")]) for k, v in _D.items()}
def number(s, p=100, track=1):
    """Pixel numerals as one outline; returns (path, width in units)."""
    import numpy as _np
    paths = []; x = 0
    for ch in s:
        if ch == " ": x += 4 * p; continue
        g = DIGITS[ch]; paths.append(to_path(g, p, x)); x += (g.shape[1] + track) * p
    return union(*paths), x - track * p

FINAL = dict(p=100, wH=8, wC=9, wO=10, c=2, gaps=(2, 1), ap=(400, 700))
