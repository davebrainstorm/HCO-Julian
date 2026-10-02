"""Round 3 master artwork (pixel HCO): symbol (gap 0.1 module), lockups, mono versions,
pixel-perfect favicons (no gap at pixel sizes). All dimensions are whole modules or letter-pixels."""
import numpy as np, sys
from PIL import Image
from mark import lockup, symbol_rects, wordmark, descriptor, desc_baseline, svg, M, CAP, HEIGHTS
from palette import E, BASALT, CHALK, LICHEN, FLAG, hex2rgb
sys.path.insert(0, "../geometry"); from glyphs import svg_d
GAP = 0.10
def save(n, b, W, H): open(f"marks/{n}.svg", "w").write(svg(b, W, H))

w = wordmark(); ww = w.bounds[2]                     # 3000 = 15M
d, dx, bb, dcap = descriptor(ww); yb = desc_baseline(bb)
for nm, mono, ink in (("colour", None, CHALK), ("basalt", BASALT, BASALT), ("chalk", CHALK, CHALK)):
    save(f"symbol-{nm}", symbol_rects(GAP, mono=mono), 8 * M, 5 * M)
    b, W, H = lockup(GAP, mono=mono, ink=ink, desc=True); save(f"primary-{nm}", b, W, H)
    b, W, H = lockup(GAP, mono=mono, ink=ink, desc=False); save(f"compact-{nm}", b, W, H)
    save(f"wordmark-{nm}", f'<path d="{svg_d(w, cap=CAP)}" fill="{ink}"/>', ww, CAP)
    save(f"descriptor-{nm}", f'<g transform="translate({dx:.2f},{-bb[1]:.2f})"><path d="{d}" fill="{ink}"/></g>', ww, bb[3] - bb[1])
    top = 5 * M + M                                    # stacked: symbol, 1M, wordmark, descriptor
    body = symbol_rects(GAP, mono=mono, x0=(ww - 8 * M) / 2) + f'<path transform="translate(0,{top})" d="{svg_d(w, cap=CAP)}" fill="{ink}"/>' + \
           f'<g transform="translate({dx:.2f},{top + yb:.2f})"><path d="{d}" fill="{ink}"/></g>'
    save(f"stacked-{nm}", body, ww, top + yb + bb[3])

def favicon(px, cell, gap_px=0, bg=BASALT):
    im = Image.new("RGB", (px, px), tuple(int(v * 255) for v in hex2rgb(bg))); P = im.load()
    ox = (px - 8 * cell) // 2; oy = (px - 5 * cell) // 2
    for i, h in enumerate(HEIGHTS):
        c = tuple(int(v * 255) for v in hex2rgb(E[h]))
        for y in range(oy + (4 - h) * cell + gap_px, oy + (5 - h) * cell):
            for x in range(ox + i * cell + gap_px, ox + (i + 1) * cell): P[x, y] = c
    return im
for px, cell, g in ((16, 2, 0), (24, 3, 0), (32, 3, 0), (48, 6, 1), (180, 20, 2), (512, 56, 6)):
    im = favicon(px, cell, g); im.save(f"marks/favicon-{px}.png")
    if px <= 48: im.resize((px * 8, px * 8), Image.NEAREST).save(f"marks/favicon-{px}-x8.png")
print("wordmark", ww, "desc cap", round(-bb[1]), "baseline", round(yb), "bottom", round(yb + bb[3]))
