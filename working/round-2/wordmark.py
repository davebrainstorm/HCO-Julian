"""Wordmarks on the symbol module. Module m = 200 units; cap height = 5m = 1000.
W1 High Bar: drawn letters, stem = 1m, crossbar centred in row 4 of 5 (70%).
W2 Grid-built: letters made of module rectangles, squared counters."""
import sys
sys.path.insert(0, "../geometry")
from glyphs import oval, rect, union, diff, translate, svg_d, count_points
import pathops

M = 200; CAP = 1000

def W1_H(w=800, stem=200, bar=164, bar_c=700):
    return union(rect(0, 0, stem, CAP), rect(w - stem, 0, stem, CAP), rect(stem - 1, bar_c - bar / 2, w - 2 * stem + 2, bar))
def W1_O(w=940, side=212, tb=168, os_=12, k_out=0.61, k_in=0.64):
    rx, ry = w / 2, CAP / 2 + os_
    return diff(oval(rx, CAP / 2, rx, ry, kx=k_out, ky=k_out), oval(rx, CAP / 2, rx - side, ry - tb, kx=k_in, ky=k_in + .02))
def W1_C(w=885, cut_hi=700, cut_lo=300, open_x=0.53):
    return diff(W1_O(w), rect(w * open_x, cut_lo, w, cut_hi - cut_lo))

def W2_H(): return union(rect(0, 0, M, CAP), rect(3 * M, 0, M, CAP), rect(M - 1, 3 * M, 2 * M + 2, M))
def _rounded_box(w, h, r):
    p = pathops.Path()
    k = 0.5523 * r
    p.moveTo(r, 0); p.lineTo(w - r, 0); p.cubicTo(w - r + k, 0, w, r - k, w, r); p.lineTo(w, h - r)
    p.cubicTo(w, h - r + k, w - r + k, h, w - r, h); p.lineTo(r, h); p.cubicTo(r - k, h, 0, h - r + k, 0, h - r)
    p.lineTo(0, r); p.cubicTo(0, r - k, r - k, 0, r, 0); p.close(); return p
def W2_O(w=4.5 * M): return diff(_rounded_box(w, CAP, M * 0.9), rect(M, M, w - 2 * M, CAP - 2 * M))
def W2_C(w=4.3 * M): return diff(W2_O(w), rect(w - M - 1, 2 * M, M + 2, CAP - 4 * M))

def word(kind="W1"):
    if kind == "W1":
        h, c, o = W1_H(), W1_C(), W1_O(); g1, g2 = 92, 60
    else:
        h, c, o = W2_H(), W2_C(), W2_O(); g1, g2 = M * 0.6, M * 0.45
    xc = h.bounds[2] + g1; xo = xc + c.bounds[2] + g2
    return union(h, translate(c, xc, 0), translate(o, xo, 0))

if __name__ == "__main__":
    for k in ("W1", "W2"):
        w = word(k); print(k, "width", round(w.bounds[2]), "points", count_points(w))
