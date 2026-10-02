"""Final Round-2 artwork: three symbol studies, lockups, one-colour and reversed
versions, and pixel-perfect favicons. All outlined vectors (no fonts, no rasters)."""
import json, numpy as np, cairosvg, io
from PIL import Image
from designs import ALL, parse
from lockup import lockup, stacked, svg, symbol_paths, PAL, M
from wordmark import word, CAP
import sys; sys.path.insert(0, "../geometry")
from glyphs import svg_d

S = {"S1": np.where(np.array(ALL["S2h"]) == 9, 0, np.array(ALL["S2h"])).tolist(),   # Massif
     "S2": ALL["S2h"],                                                                 # Observation (one flagged cell)
     "S3": ALL["S3e"]}                                                                 # Ridgeline
NAMES = {"S1": "Massif", "S2": "Observation", "S3": "Ridgeline"}
ALL.update({"S1": S["S1"], "S2": S["S2"], "S3": S["S3"]})
json.dump({k: {"name": NAMES[k], "cells": v} for k, v in S.items()}, open("marks/symbols.json", "w"), indent=1)

def save(name, body, W, H, pad=0, bg=None):
    open(f"marks/{name}.svg", "w").write(svg(body, W, H, pad=pad, bg=bg))

for k, q in S.items():
    q = np.array(q); R, C = q.shape
    save(f"{k}-symbol-colour", symbol_paths(q), C * M, R * M)
    save(f"{k}-symbol-basalt", symbol_paths(q, mono=PAL["basalt"]), C * M, R * M)
    save(f"{k}-symbol-chalk", symbol_paths(q, mono=PAL["chalk"]), C * M, R * M)
    for d in ("below", "none"):
        b, W, H = lockup(k, "W1", d if d != "none" else None); save(f"{k}-lockup-{d}-colour", b, W, H)
        b, W, H = lockup(k, "W1", d if d != "none" else None, mono=PAL["basalt"]); save(f"{k}-lockup-{d}-basalt", b, W, H)
        b, W, H = lockup(k, "W1", d if d != "none" else None, mono=PAL["chalk"]); save(f"{k}-lockup-{d}-chalk", b, W, H)
    # pixel-perfect favicons on a Basalt tile: integer cell sizes only
    for px, cell in ((16, 2), (24, 3), (32, 3), (180, 18), (512, 48)):
        im = Image.new("RGB", (px, px), PAL["basalt"]); pix = im.load()
        ox = (px - C * cell) // 2; oy = (px - R * cell) // 2
        cols = {1: PAL["sage"], 2: PAL["lichen"], 3: PAL["chalk"], 9: PAL["flag"]}
        for r in range(R):
            for c in range(C):
                if q[r, c]:
                    rgb = tuple(int(cols[q[r, c]][i:i+2], 16) for i in (1, 3, 5))
                    for y in range(oy + r * cell, oy + (r + 1) * cell):
                        for x in range(ox + c * cell, ox + (c + 1) * cell): pix[x, y] = rgb
        im.save(f"marks/{k}-favicon-{px}.png")
        if px <= 32: im.resize((px * 6, px * 6), Image.NEAREST).save(f"marks/{k}-favicon-{px}-x6.png")
# stacked signature (recommended study)
for mono, nm in ((None, "colour"), (PAL["basalt"], "basalt"), (PAL["chalk"], "chalk")):
    b, W, H = stacked("S3", mono=mono); save(f"S3-stacked-{nm}", b, W, H)
# wordmarks alone
for k in ("W1", "W2"):
    w = word(k); open(f"marks/{k}-chalk.svg", "w").write(svg(f'<path d="{svg_d(w, cap=CAP)}" fill="{PAL["chalk"]}"/>', w.bounds[2], CAP + 14))
    open(f"marks/{k}-basalt.svg", "w").write(svg(f'<path d="{svg_d(w, cap=CAP)}" fill="{PAL["basalt"]}"/>', w.bounds[2], CAP + 14))
print("marks written")
