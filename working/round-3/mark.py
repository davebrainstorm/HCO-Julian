"""HCO Round 3 — master artwork. Units: module M = 200 = one sample = one stem.
Symbol 'Ridgeline': eight samples of a terrain section, one per column."""
import sys, numpy as np
sys.path.insert(0, "../geometry"); sys.path.insert(0, "../round-2")
from glyphs import oval, rect, union, diff, translate, svg_d, count_points
from textpath import shape
from palette import E, BASALT, CHALK, LICHEN, FLAG

M, CAP = 200, 1000
HEIGHTS = [0, 1, 1, 2, 3, 4, 3, 2]                     # the measured section, in modules
INS = "../fonts-static/InstrumentSans-Medium.ttf"

def H_(w=800, stem=200, bar=164, bar_c=700):
    return union(rect(0, 0, stem, CAP), rect(w - stem, 0, stem, CAP), rect(stem - 1, bar_c - bar / 2, w - 2 * stem + 2, bar))
def O_(w=940, side=212, tb=168, os_=12, k_out=0.61, k_in=0.64):
    rx, ry = w / 2, CAP / 2 + os_
    return diff(oval(rx, CAP / 2, rx, ry, kx=k_out, ky=k_out), oval(rx, CAP / 2, rx - side, ry - tb, kx=k_in, ky=k_in + .02))
def C_(w=885, cut_hi=700, cut_lo=300, open_x=0.53):
    return diff(O_(w), rect(w * open_x, cut_lo, w, cut_hi - cut_lo))
def wordmark(*_):
    """Primary wordmark from Round 3b: pixel HCO (see pixel.py). 3000 × 1000 units = 15M × 5M."""
    from pixel import wordmark as _pw, FINAL
    return _pw(**FINAL)[0]

def wordmark_drawn(g1=84, g2=54):
    """Round 2/3a drawn High Bar wordmark, kept for reference."""
    h, c, o = H_(), C_(), O_()
    xc = h.bounds[2] + g1; xo = xc + c.bounds[2] + g2
    return union(h, translate(c, xc, 0), translate(o, xo, 0))

def symbol_rects(gap=0.0, x0=0, y0=0, u=M, mono=None, heights=HEIGHTS, rows=5):
    out = []; g = gap * u
    for i, h in enumerate(heights):
        x = x0 + i * u + g / 2; y = y0 + (rows - 1 - h) * u + g / 2
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{u - g:.1f}" height="{u - g:.1f}" fill="{mono or E[h]}"/>')
    return "".join(out)

def lockup(gap=0.0, mono=None, ink=None, desc=True, g_sym=1.0, wm_gaps=(84, 54)):
    ink = ink or mono or CHALK
    w = wordmark(*wm_gaps); ww = w.bounds[2]
    body = [symbol_rects(gap, 0, 0, mono=mono)]
    x = 8 * M + g_sym * M
    body.append(f'<path transform="translate({x},0)" d="{svg_d(w, cap=CAP)}" fill="{ink}"/>')
    W, H = x + ww, CAP
    if desc:
        d, dx, bb, dcap = descriptor(ww)
        y = desc_baseline(bb); iy1 = bb[3]
        body.append(f'<g transform="translate({x + dx:.2f},{y:.1f})"><path d="{d}" fill="{ink}"/></g>')
        H = y + iy1
    return "".join(body), W, H

DESC = "HIGH COUNTRY OBSERVATIONS"; DESC_TRACK = 0.04; DESC_GAP = 100   # one letter-pixel
def descriptor(ww, text=DESC, tracking=DESC_TRACK):
    """Descriptor outlined, tracked uppercase, scaled so its INK spans exactly 0…ww (the ink width of HCO).
    Returns (path d, x offset to apply, ink bounds after offset, cap height)."""
    from fontTools.svgLib.path import parse_path
    from fontTools.pens.boundsPen import BoundsPen
    def ink(fs):
        d, dw, _, dcap = shape(INS, text, fs, tracking=tracking); bp = BoundsPen(None); parse_path(d, bp); return d, bp.bounds, dcap
    _, b, _ = ink(100); fs = 100 * ww / (b[2] - b[0])
    d, b, dcap = ink(fs)
    return d, -b[0], (0, b[1], b[2] - b[0], b[3]), dcap

def desc_baseline(b):
    """Baseline of the descriptor below the HCO baseline (y = CAP): cap top sits one letter-pixel down."""
    return CAP + DESC_GAP - b[1]

def svg(body, W, H, y0=0.0, bg=None):
    """viewBox from (0, y0) to (W, H): y0 < 0 keeps the round letters' overshoot inside the artboard."""
    r = f'<rect x="0" y="{y0}" width="{W:.1f}" height="{H - y0:.1f}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {y0:g} {W:.1f} {H - y0:.1f}">{r}{body}</svg>'

