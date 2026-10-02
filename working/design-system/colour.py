"""Groundwork colour maths: OKLab/OKLCH, gamut mapping, WCAG contrast, CVD simulation (Machado et al. 2009)."""
import math, sys
sys.path.insert(0, "../round-3")
from palette import to_oklab, from_oklab, hex2rgb, rgb2hex, mix, contrast, lum, BASALT, CHALK, MOSS, SAGE, LICHEN, FLAG, E

def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def oklab_to_lin(L, a, b):
    l = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    return (4.0767416621*l - 3.3077115913*m + 0.2309699292*s,
            -1.2684380046*l + 2.6097574011*m - 0.3413193965*s,
            -0.0041960863*l - 0.7034186147*m + 1.7076147010*s)
def in_gamut(L, a, b, eps=1e-4): return all(-eps <= v <= 1 + eps for v in oklab_to_lin(L, a, b))
def oklch(L, C, h):
    """OKLCH → hex, reducing chroma until the colour fits sRGB (hue and lightness preserved)."""
    hr = math.radians(h)
    while C > 0 and not in_gamut(L, C * math.cos(hr), C * math.sin(hr)): C -= 0.002
    return from_oklab(L, C * math.cos(hr), C * math.sin(hr))
def lch(hx):
    L, a, b = to_oklab(hx); return L, math.hypot(a, b), (math.degrees(math.atan2(b, a)) + 360) % 360

M = {"protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
     "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
     "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}
def simulate(hx, kind):
    r, g, b = (_lin(c) for c in hex2rgb(hx))
    if kind == "greyscale":
        y = 0.2126*r + 0.7152*g + 0.0722*b; return rgb2hex((_gam(y),) * 3)
    m = M[kind]; out = [sum(m[i][j] * v for j, v in enumerate((r, g, b))) for i in range(3)]
    return rgb2hex(tuple(_gam(max(0, min(1, v))) for v in out))
def de(h1, h2):
    """ΔE in OKLab (×100)."""
    a, b = to_oklab(h1), to_oklab(h2); return 100 * math.dist(a, b)
