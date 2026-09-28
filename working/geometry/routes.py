"""Concept-stage artwork for the three routes. Outputs outlined SVG geometry
(no fonts, no raster) into ../concepts/marks/."""
import os, json, math
import pathops
from glyphs import *
from textpath import shape

OUT = "../concepts/marks"; os.makedirs(OUT, exist_ok=True)
F = "../fonts-ofl/"
INS = F + "instrumentsans/InstrumentSans[wdth,wght].ttf"
PLEX = F + "ibmplexsans/IBMPlexSans[wdth,wght].ttf"
NEWS = F + "newsreader/Newsreader[opsz,wght].ttf"
PUB = F + "publicsans/PublicSans[wght].ttf"

def svg(w, h, body, bg=None):
    r = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}">{r}{body}</svg>'

def save(name, s):
    open(f"{OUT}/{name}.svg", "w").write(s)

# ---------------------------------------------------------------- Route 1
def H(w=820, stem=194, bar=138, bar_c=715, cap=1000):
    return union(rect(0, 0, stem, cap), rect(w - stem, 0, stem, cap),
                 rect(stem - 1, bar_c - bar / 2, w - 2 * stem + 2, bar))

def O(w=935, side=204, tb=160, os_=12, k_out=0.61, k_in=0.64, cap=1000):
    rx, ry = w / 2, cap / 2 + os_
    return diff(oval(rx, cap / 2, rx, ry, kx=k_out, ky=k_out),
                oval(rx, cap / 2, rx - side, ry - tb, kx=k_in, ky=k_in + .02))

def C(w=880, side=200, tb=160, os_=12, cut_hi=715, cut_lo=290, open_x=0.52, cap=1000):
    return diff(O(w, side, tb, os_), rect(w * open_x, cut_lo, w, cut_hi - cut_lo))

def r1_word(gaps=(94, 62)):
    h, c, o = H(), C(), O()
    xc = h.bounds[2] + gaps[0]
    xo = xc + c.bounds[2] + gaps[1]
    return union(h, translate(c, xc, 0), translate(o, xo, 0))

# ---------------------------------------------------------------- Route 2
def offset_polyline(pts, t):
    """Polygon for a polyline stroked to width t with mitre joins (y-down)."""
    def seg_normal(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        return (-dy / L, dx / L)
    def side(sign):
        out = []
        n = len(pts)
        for i in range(n):
            if i == 0:
                nx, ny = seg_normal(pts[0], pts[1]); out.append((pts[0][0] + sign*nx*t/2, pts[0][1] + sign*ny*t/2))
            elif i == n - 1:
                nx, ny = seg_normal(pts[-2], pts[-1]); out.append((pts[-1][0] + sign*nx*t/2, pts[-1][1] + sign*ny*t/2))
            else:
                n1 = seg_normal(pts[i-1], pts[i]); n2 = seg_normal(pts[i], pts[i+1])
                mx, my = n1[0] + n2[0], n1[1] + n2[1]; ml = math.hypot(mx, my)
                mx, my = mx / ml, my / ml
                cosh = mx * n1[0] + my * n1[1]
                L = (t / 2) / cosh
                out.append((pts[i][0] + sign*mx*L, pts[i][1] + sign*my*L))
        return out
    a = side(+1); b = side(-1)
    return a + b[::-1]

RISE = [(-40, 640), (395, 640), (605, 330), (1040, 330)]
def r2_parts(S=1000, t=86):
    sq = rect(0, 0, S, S)
    track = poly(offset_polyline(RISE, t))
    both = diff(sq, track)
    # split contours: upper (high ground / sky) and lower (ground)
    contours = []
    cur = None
    for verb, pts in both:
        if verb == pathops.PathVerb.MOVE:
            cur = pathops.Path(); cur.moveTo(*pts[0]); contours.append(cur)
        elif verb == pathops.PathVerb.LINE: cur.lineTo(*pts[0])
        elif verb == pathops.PathVerb.CLOSE: cur.close()
    contours.sort(key=lambda p: (p.bounds[1] + p.bounds[3]))
    return both, contours[0], contours[-1]

def ydown_d(path, s=1.0, dx=0, dy=0):
    return svg_d(path, cap=0, scale=1).replace("-", "\x00") if False else _plain(path, s, dx, dy)

def _plain(path, s=1.0, dx=0, dy=0):
    d = []; V = pathops.PathVerb
    f = lambda x, y: f"{round(x*s+dx,2):g} {round(y*s+dy,2):g}"
    for verb, pts in path:
        if verb == V.MOVE: d.append("M" + f(*pts[0]))
        elif verb == V.LINE: d.append("L" + f(*pts[0]))
        elif verb == V.CUBIC: d.append("C" + " ".join(f(*p) for p in pts))
        elif verb == V.CLOSE: d.append("Z")
    return "".join(d)

if __name__ == "__main__":
    INK, WHITE = "#111111", "#FFFFFF"
    meta = {}
    # ---- Route 1: wordmark, compact H, lockup
    w1 = r1_word(); W1 = w1.bounds[2]
    pad = 0
    d1 = svg_d(w1, cap=1012, dy=0)  # flip around top incl. overshoot
    H1 = 1024
    for nm, fg, bg in [("r1-wordmark-black", INK, None), ("r1-wordmark-white", WHITE, None)]:
        save(nm, svg(W1, H1, f'<path d="{d1}" fill="{fg}"/>'))
    h = H(); dH = svg_d(h, cap=1000)
    save("r1-compact-black", svg(820, 1000, f'<path d="{dH}" fill="{INK}"/>'))
    save("r1-compact-white", svg(820, 1000, f'<path d="{dH}" fill="{WHITE}"/>'))
    # lockup: descriptor hangs from the underside of the high bar and stands on the baseline
    _, _, _, cap100 = shape(INS, "H", 100, {"wght": 560, "wdth": 100})
    capr = cap100 / 100; lead = 1.18
    top_u = 715 - 69                      # crossbar underside (y-up units)
    fs = top_u / (capr + lead)
    l1, lw1, _, cap = shape(INS, "High Country", fs, {"wght": 560, "wdth": 100})
    l2, lw2, _, _ = shape(INS, "Observations", fs, {"wght": 560, "wdth": 100})
    base1 = 1012 - (top_u - cap)
    base2 = 1012
    x0 = W1 + 170
    lock_w = x0 + max(lw1, lw2)
    body = (f'<path d="{d1}" fill="{{c}}"/>'
            f'<g transform="translate({x0},{base1:.1f})"><path d="{l1}" fill="{{c}}"/></g>'
            f'<g transform="translate({x0},{base2})"><path d="{l2}" fill="{{c}}"/></g>')
    save("r1-lockup-black", svg(lock_w, H1, body.format(c=INK)))
    save("r1-lockup-white", svg(lock_w, H1, body.format(c=WHITE)))
    meta["r1"] = {"word_w": W1, "lock_w": lock_w, "desc_em": fs}

    # ---- Route 2: Rise symbol + Plex lockup
    both, upper, lower = r2_parts()
    dB, dU, dL = _plain(both), _plain(upper), _plain(lower)
    save("r2-symbol-black", svg(1000, 1000, f'<path d="{dB}" fill="{INK}"/>'))
    save("r2-symbol-white", svg(1000, 1000, f'<path d="{dB}" fill="{WHITE}"/>'))
    save("r2-symbol-twotone", svg(1000, 1000, f'<path d="{dU}" fill="#8F9A8C"/><path d="{dL}" fill="{INK}"/>'))
    wm, wmw, _, wcap = shape(PLEX, "HCO", 1000 / 0.698, {"wght": 600, "wdth": 100}, tracking=0.01)
    # scale HCO so cap height == 0.62 of symbol, sitting on symbol baseline
    capH = 620; sc = capH / wcap
    d2, d2w, _, d2cap = shape(PLEX, "High Country Observations", 150, {"wght": 450})
    x = 1000 + 190
    body = (f'<path d="{dB}" fill="{{c}}"/>'
            f'<g transform="translate({x},{1000 - 380}) scale({sc:.4f})"><path d="{wm}" fill="{{c}}"/></g>'
            f'<g transform="translate({x+8},{1000})"><path d="{d2}" fill="{{c}}"/></g>')
    lw = x + max(wmw * sc, d2w)
    save("r2-lockup-black", svg(lw, 1045, body.format(c=INK)))
    save("r2-lockup-white", svg(lw, 1045, body.format(c=WHITE)))
    meta["r2"] = {"lock_w": lw}

    # ---- Route 3: serif wordmark + square point
    fs3 = 1000 / 0.62
    w3, w3w, s3, cap3 = shape(NEWS, "HCO", fs3, {"wght": 560, "opsz": 72}, tracking=0.035)
    sc3 = 1000 / cap3
    pt = 190  # square point side, ~ stem weight
    gap = 60
    W3 = w3w * sc3 + gap + pt
    body = (f'<g transform="translate(0,1000) scale({sc3:.4f})"><path d="{w3}" fill="{{c}}"/></g>'
            f'<rect x="{w3w*sc3+gap:.1f}" y="{1000-pt}" width="{pt}" height="{pt}" fill="{{p}}"/>')
    save("r3-wordmark-black", svg(W3, 1015, body.format(c=INK, p=INK)))
    save("r3-wordmark-white", svg(W3, 1015, body.format(c=WHITE, p=WHITE)))
    save("r3-wordmark-accent", svg(W3, 1015, body.format(c=INK, p="#E4502A")))
    h3, h3w, _, _ = shape(NEWS, "H", fs3, {"wght": 600, "opsz": 72})
    Wc = h3w * sc3 + gap + pt
    bodyc = (f'<g transform="translate(0,1000) scale({sc3:.4f})"><path d="{h3}" fill="{{c}}"/></g>'
             f'<rect x="{h3w*sc3+gap-40:.1f}" y="{1000-pt}" width="{pt}" height="{pt}" fill="{{p}}"/>')
    save("r3-compact-black", svg(Wc - 40, 1015, bodyc.format(c=INK, p=INK)))
    save("r3-compact-white", svg(Wc - 40, 1015, bodyc.format(c=WHITE, p=WHITE)))
    json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1)
    print(meta)
