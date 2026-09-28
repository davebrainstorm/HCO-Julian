"""Route 1 sketches: custom HCO with raised ('high-bar') H crossbar."""
from glyphs import *
import json, sys

def H(w=800, stem=196, bar=150, bar_c=640, cap=1000):
    return union(rect(0, 0, stem, cap), rect(w - stem, 0, stem, cap),
                 rect(stem - 1, bar_c - bar / 2, w - 2 * stem + 2, bar))

def O(w=960, side=206, tb=172, os=14, k_out=0.58, k_in=0.60, cap=1000):
    rx, ry = w / 2, cap / 2 + os
    outer = oval(rx, cap / 2, rx, ry, kx=k_out, ky=k_out)
    inner = oval(rx, cap / 2, rx - side, ry - tb, kx=k_in, ky=k_in + .02)
    return diff(outer, inner)

def C(w=880, side=206, tb=172, os=14, cut_hi=690, cut_lo=300, open_x=0.50, k_out=0.58, k_in=0.60, cap=1000):
    ring = O(w, side, tb, os, k_out, k_in, cap)
    # horizontal-cut aperture on the right
    return diff(ring, rect(w * open_x, cut_lo, w, cut_hi - cut_lo))

def word(params, gaps=(120, 70)):
    h = H(**params.get("H", {}))
    c = C(**params.get("C", {}))
    o = O(**params.get("O", {}))
    hw = h.bounds[2]; cw = c.bounds[2]
    c = translate(c, hw + gaps[0], 0)
    o = translate(o, hw + gaps[0] + cw + gaps[1], 0)
    return union(h, c, o)

if __name__ == "__main__":
    variants = {
      "v1 bar 640, C cut 690/300": {},
      "v2 bar 660, C upper cut = bar top": {"H": {"bar_c": 660, "bar": 150}, "C": {"cut_hi": 735, "cut_lo": 270}},
      "v3 bar 700 (higher)": {"H": {"bar_c": 700, "bar": 145}, "C": {"cut_hi": 700}},
      "v4 lighter 168 stem": {"H": {"stem": 168, "bar": 132, "bar_c": 650}, "C": {"side": 176, "tb": 150}, "O": {"side": 176, "tb": 150}},
      "v5 standard bar (control)": {"H": {"bar_c": 500}},
    }
    out = {}
    for name, p in variants.items():
        w = word(p)
        out[name] = {"d": svg_d(w), "w": w.bounds[2], "pts": count_points(w)}
    json.dump(out, open("hco_v1.json", "w"))
    for k, v in out.items(): print(k, round(v["w"]), v["pts"])
