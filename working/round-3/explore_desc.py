import cairosvg, sys
sys.path.insert(0, "../geometry")
from textpath import shape
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
from mark import lockup, symbol_rects, wordmark, M, CAP
from glyphs import svg_d
from palette import BASALT, CHALK
def fit(font, text, ww, tracking=0.0):
    def ink(fs):
        d, dw, _, cap = shape(font, text, fs, tracking=tracking); bp = BoundsPen(None); parse_path(d, bp); return d, bp.bounds, cap
    _, b, _ = ink(100); fs = 100 * ww / (b[2] - b[0]); d, b, cap = ink(fs); return d, -b[0], b, cap, fs
w = wordmark(); out = []; y = 0
for name, font, text, tr, base in (
    ("D1", "../fonts-static/InstrumentSans-Medium.ttf", "High Country Observations", 0.0, 1.5),
    ("D2", "../fonts-static/InstrumentSans-CondSemiBold.ttf", "HIGH COUNTRY OBSERVATIONS", 0.10, 1.25),
    ("D3", "../fonts-static/InstrumentSans-Medium.ttf", "HIGH COUNTRY OBSERVATIONS", 0.04, 1.25)):
    d, dx, b, cap, fs = fit(font, text, 3000, tr)
    print(name, "cap", round(cap), "units =", round(cap / M, 2), "M; desc bottom", round(b[3]))
    out.append(symbol_rects(0.1, 0, y) + f'<path transform="translate({9*M},{y})" d="{svg_d(w, cap=CAP)}" fill="{CHALK}"/>'
               f'<g transform="translate({9*M + dx:.1f},{y + CAP + base * M})"><path d="{d}" fill="{CHALK}"/></g>')
    y += 1900
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 5400 {y + 200}"><rect x="-300" y="-300" width="99999" height="99999" fill="{BASALT}"/>{"".join(out)}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="explore/desc-test.png", output_width=1400)
cairosvg.svg2png(bytestring=svg.encode(), write_to="explore/desc-test-small.png", output_width=300)
