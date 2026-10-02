"""HCO colour system (Round 3). Core colours + a five-step elevation ramp
interpolated in OKLab so each step is perceptually even."""
import math

def _srgb_to_lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _lin_to_srgb(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def hex2rgb(h): return tuple(int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
def rgb2hex(r): return "#%02X%02X%02X" % tuple(max(0, min(255, round(v * 255))) for v in r)
def to_oklab(h):
    r, g, b = (_srgb_to_lin(c) for c in hex2rgb(h))
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l, m, s = (math.copysign(abs(v) ** (1/3), v) for v in (l, m, s))
    return (0.2104542553*l + 0.7936177850*m - 0.0040720468*s,
            1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
            0.0259040371*l + 0.7827717662*m - 0.8086757660*s)
def from_oklab(L, a, b):
    l = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    r = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bb = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    return rgb2hex(tuple(_lin_to_srgb(max(0, v)) for v in (r, g, bb)))
def mix(a, b, t):
    A, B = to_oklab(a), to_oklab(b)
    return from_oklab(*(A[i] + (B[i] - A[i]) * t for i in range(3)))

BASALT, CHALK, LICHEN, FLAG = "#0E2423", "#F4F5EF", "#C9D36E", "#EC5D2F"
MOSS, SAGE = "#2E4B43", "#72907C"
# elevation ramp: E0 low … E4 summit
E = [mix(MOSS, SAGE, 0.64), SAGE, mix(SAGE, LICHEN, 0.5), LICHEN, CHALK]
STONE = mix(BASALT, CHALK, 0.40)          # secondary text on light grounds (≥ 4.5:1 on Chalk)
INK2 = mix(BASALT, CHALK, 0.62)           # secondary text on Basalt (≥ 4.5:1)

def lum(h):
    r, g, b = (_srgb_to_lin(c) for c in hex2rgb(h)); return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + 0.05) / (y + 0.05)

if __name__ == "__main__":
    print("ramp", E)
    for i, c in enumerate(E): print(f"E{i} {c} on Basalt {contrast(c, BASALT):.2f}")
    print("STONE", STONE, f"{contrast(STONE, CHALK):.2f} on Chalk", "INK2", INK2, f"{contrast(INK2, BASALT):.2f} on Basalt")
