"""Compose symbol + wordmark + descriptor as outlined SVG (units: module M = 200)."""
import numpy as np, sys
sys.path.insert(0, "../geometry")
from glyphs import svg_d
from textpath import shape
from wordmark import word, M, CAP
from designs import ALL

PAL = dict(basalt="#0E2423", moss="#2E4B43", sage="#72907C", lichen="#C9D36E", chalk="#F4F5EF", flag="#EC5D2F")
INS = "../fonts-ofl/instrumentsans/InstrumentSans[wdth,wght].ttf"

def ramp(pal): return {1: pal["sage"], 2: pal["lichen"], 3: pal["chalk"], 9: pal["flag"]}

def symbol_paths(q, x0=0, y0=0, u=M, mono=None, pal=PAL):
    q = np.array(q); out = []
    cols = ramp(pal)
    for r in range(q.shape[0]):
        for c in range(q.shape[1]):
            if q[r, c]:
                out.append(f'<rect x="{x0 + c*u:.1f}" y="{y0 + r*u:.1f}" width="{u}" height="{u}" fill="{mono or cols[q[r, c]]}"/>')
    return "".join(out)

def lockup(sym, wm="W1", desc="below", mono=None, ink=None, pal=PAL, gap=1.0):
    """Returns (svg_body, width, height). ink = wordmark colour."""
    q = np.array(ALL[sym]); R, C = q.shape
    ink = ink or mono or pal["chalk"]
    sym_h = R * M
    # symbol bottom sits on the baseline; HCO cap height = 5 modules
    base = max(sym_h, CAP)
    body = [symbol_paths(q, 0, base - sym_h, mono=mono, pal=pal)]
    w = word(wm); ww = w.bounds[2]
    x = C * M + gap * M
    body.append(f'<path transform="translate({x},{base - CAP})" d="{svg_d(w, cap=CAP)}" fill="{ink}"/>')
    W = x + ww; Hh = base
    if desc == "below":
        # descriptor set to the width of HCO, cap top one module under the baseline
        d0, dw0, _, dcap0 = shape(INS, "High Country Observations", 100, {"wght": 520, "wdth": 100})
        fs = 100 * ww / dw0
        d, dw, _, dcap = shape(INS, "High Country Observations", fs, {"wght": 520, "wdth": 100})
        y = base + 1.5 * M                                   # descriptor baseline on the half-module line
        body.append(f'<g transform="translate({x},{y:.1f})"><path d="{d}" fill="{ink}"/></g>')
        Hh = y + 0.32 * dcap                                 # room for descenders
    elif desc == "right":
        fs = 0
        _, _, _, cap100 = shape(INS, "H", 100, {"wght": 520, "wdth": 100})
        capr = cap100 / 100; lead = 1.18; top = 600            # hangs from the crossbar's underside (row 4)
        fs = top / (capr + lead)
        l1, w1, _, c1 = shape(INS, "High Country", fs, {"wght": 520, "wdth": 100})
        l2, w2, _, _ = shape(INS, "Observations", fs, {"wght": 520, "wdth": 100})
        xd = W + 0.85 * M
        body.append(f'<g transform="translate({xd},{base - top + c1:.1f})"><path d="{l1}" fill="{ink}"/></g>')
        body.append(f'<g transform="translate({xd},{base})"><path d="{l2}" fill="{ink}"/></g>')
        W = xd + max(w1, w2)
    return "".join(body), W, Hh

def svg(body, W, H, pad=0, bg=None):
    r = f'<rect x="{-pad}" y="{-pad}" width="{W + 2*pad}" height="{H + 2*pad}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {W + 2*pad:.1f} {H + 2*pad:.1f}">{r}{body}</svg>'

def stacked(sym, mono=None, ink=None, pal=PAL):
    """Symbol above the wordmark, both on the module, left-aligned; descriptor below."""
    q = np.array(ALL[sym]); R, Cc = q.shape
    ink = ink or mono or pal["chalk"]
    body = [symbol_paths(q, 0, 0, mono=mono, pal=pal)]
    w = word("W1"); ww = w.bounds[2]
    top = R * M + 1.0 * M
    body.append(f'<path transform="translate(0,{top})" d="{svg_d(w, cap=CAP)}" fill="{ink}"/>')
    base = top + CAP
    _, dw0, _, _ = shape(INS, "High Country Observations", 100, {"wght": 520, "wdth": 100})
    fs = 100 * ww / dw0
    d, dw, _, dcap = shape(INS, "High Country Observations", fs, {"wght": 520, "wdth": 100})
    y = base + 1.5 * M
    body.append(f'<g transform="translate(0,{y:.1f})"><path d="{d}" fill="{ink}"/></g>')
    return "".join(body), max(ww, Cc * M), y + 0.32 * dcap
