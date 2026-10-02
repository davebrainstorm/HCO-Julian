import cairosvg, sys
from pixel import wordmark, CAP, M, svg_d
from palette import BASALT, CHALK, E, LICHEN
sys.path.insert(0, "../geometry")
from mark import symbol_rects
V = [
 ("A  p=M/2 · 2-stair corners · gaps 1/1", dict(p=100, wH=8, wC=9, wO=10, c=2, gaps=(1, 1))),
 ("B  p=M/2 · 1-stair corners · gaps 1/1", dict(p=100, wH=8, wC=9, wO=10, c=1, gaps=(1, 1))),
 ("C  p=M/2 · 3-stair corners · gaps 2/1", dict(p=100, wH=8, wC=9, wO=10, c=3, gaps=(2, 1))),
 ("D  p=M/3 · 3-stair · gaps 2/2", dict(p=200/3, wH=12, wC=13, wO=14, c=3, gaps=(2, 2))),
 ("E  p=M/3 · 4-stair · gaps 2/1", dict(p=200/3, wH=12, wC=13, wO=15, c=4, gaps=(2, 1))),
 ("F  p=M/4 · 5-stair · gaps 3/2", dict(p=50, wH=16, wC=17, wO=19, c=5, gaps=(3, 2))),
]
rows = []; y = 0
for name, kw in V:
    path, W, info = wordmark(**kw)
    sym = symbol_rects(0.10, 0, y, mono=None)
    rows.append(f'<g>{sym}<path transform="translate({9*M},{y})" d="{svg_d(path, cap=CAP)}" fill="{CHALK}"/>'
                f'<text x="{9*M + W + 300}" y="{y + 560}" font-family="DejaVu Sans" font-size="130" fill="#959F9A">{name}</text></g>')
    y += 1500
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 9200 {y + 100}"><rect x="-300" y="-300" width="9200" height="{y+400}" fill="{BASALT}"/>{"".join(rows)}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="explore/pixel-wordmarks.png", output_width=1800)
print("ok")
