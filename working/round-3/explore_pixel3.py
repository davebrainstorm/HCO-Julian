import cairosvg
from pixel import wordmark, number, FINAL, CAP, M, svg_d
from palette import BASALT, CHALK, E, LICHEN, FLAG
from mark import symbol_rects
path, W, info = wordmark(**FINAL)
n1, w1 = number("0123456789")
n2, w2 = number("01 24 2026")
y2 = 1600; y3 = 3200
body = (symbol_rects(0.10, 0, 0) + f'<path transform="translate({9*M},0)" d="{svg_d(path, cap=CAP)}" fill="{CHALK}"/>'
        f'<path transform="translate(0,{y2})" d="{svg_d(n1, cap=CAP)}" fill="{CHALK}"/>'
        f'<path transform="translate(0,{y3})" d="{svg_d(n2, cap=CAP)}" fill="{LICHEN}"/>')
grid = "".join(f'<line x1="{x}" y1="-100" x2="{x}" y2="1100" stroke="#EC5D2F" stroke-opacity=".35" stroke-width="6"/>' for x in range(9*M, 9*M + 3001, 100))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 {max(w1, 24*M) + 600} 4900"><rect x="-300" y="-300" width="99999" height="99999" fill="{BASALT}"/>{body}{grid}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="explore/pixel-final.png", output_width=1800)
print("wordmark width", W, "units =", W / M, "M")
