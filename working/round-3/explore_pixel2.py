import cairosvg, json, numpy as np, sys
from pixel import wordmark, CAP, M, svg_d
from palette import BASALT, CHALK, E, LICHEN, FLAG, mix
from mark import symbol_rects
sec = json.load(open("assets/section.json")); prof = np.array(sec["profile"])
def ridge16(thick=2):
    lv = np.round(prof.reshape(16, 6).mean(1) * 8).astype(int)       # 16 half-module columns, 0…8
    cells = []
    for i, l in enumerate(lv):
        lo = l; hi = l + thick - 1
        for nb in (i - 1, i + 1):                                     # keep the stroke connected
            if 0 <= nb < 16 and lv[nb] + thick - 1 < lo - 0: lo = min(lo, lv[nb] + thick - 1 + 1) if False else min(lo, lv[nb] + thick)
        for r in range(lo, hi + 1): cells.append((i, r))
    return lv, cells
def ridge_svg(x0, y0, p=100, gap=0.0, colour=True):
    lv, cells = ridge16(); o = []
    for i, r in cells:
        t = min(4, r // 2); fill = E[t] if colour else CHALK
        o.append(f'<rect x="{x0 + i*p + gap/2:.1f}" y="{y0 + CAP - (r+1)*p + gap/2:.1f}" width="{p-gap:.1f}" height="{p-gap:.1f}" fill="{fill}"/>')
    return "".join(o), lv
rows = []; y = 0
tests = [
 ("A1 cells · gaps 1/1 · aperture 300–700", "cells", dict(gaps=(1, 1))),
 ("A2 cells · gaps 2/1", "cells", dict(gaps=(2, 1))),
 ("A3 cells · gaps 1/1 · aperture 400–700", "cells", dict(gaps=(1, 1), ap=(400, 700))),
 ("A4 cells · gaps 1/1 · aperture 400–600", "cells", dict(gaps=(1, 1), ap=(400, 600))),
 ("R1 pixel ridgeline · 16 cols · 2-px stroke", "ridge", dict(gaps=(1, 1))),
 ("R2 pixel ridgeline · gapped pixels", "ridgeg", dict(gaps=(1, 1))),
]
for name, sk, kw in tests:
    path, W, info = wordmark(p=100, wH=8, wC=9, wO=10, c=2, **kw)
    if sk == "cells": sym = symbol_rects(0.10, 0, y)
    else: sym, lv = ridge_svg(0, y, gap=0 if sk == "ridge" else 10)
    rows.append(f'<g>{sym}<path transform="translate({9*M},{y})" d="{svg_d(path, cap=CAP)}" fill="{CHALK}"/>'
                f'<text x="{9*M + W + 300}" y="{y + 560}" font-family="DejaVu Sans" font-size="130" fill="#959F9A">{name}</text></g>')
    y += 1500
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 9600 {y + 100}"><rect x="-300" y="-300" width="9600" height="{y+400}" fill="{BASALT}"/>{"".join(rows)}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="explore/pixel-wordmarks-2.png", output_width=1800)
print(ridge16()[0])
