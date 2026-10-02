"""Isometric block model of the terrain, cut along the measured section.
Procedural terrain — illustrative, not real elevation data."""
import numpy as np, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, "../round-2")
from terrain import hillshade
from palette import E as RAMP, BASALT, MOSS, CHALK, LICHEN, hex2rgb, mix

SEC = dict(L=96, y=224, x0=1560)            # the section whose 8 samples are the logo
TARGET = [0, 1, 1, 2, 3, 4, 3, 2]

def rgb(h): return tuple(int(v * 255) for v in hex2rgb(h))
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c)

def ramp_colour(t):
    """Elevation t∈[0,1] → colour: low ground in Basalt/Moss, then E0…E4."""
    stops = [(0.00, mix(BASALT, MOSS, 0.55)), (0.30, MOSS), (0.50, RAMP[0]), (0.66, RAMP[1]), (0.80, RAMP[2]), (0.91, RAMP[3]), (0.985, RAMP[4])]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            u = (t - a) / (b - a); return rgb(mix(ca, cb, max(0, min(1, u))))
    return rgb(RAMP[4])

def render(N=96, span=192, cut=True, out="assets/voxel.png", W=3600, Hh=2250, zscale=None, base=None, hi_samples=True, bg=BASALT, ss=2, oyf=0.30, scale=0.86):
    Ed = np.load("../round-2/assets/dem1920-11.npy")
    cx = SEC["x0"] + SEC["L"] // 2; cy = SEC["y"]
    x0, y0 = cx - span // 2, cy - span // 2
    patch = Ed[y0:y0 + span, x0:x0 + span]
    k = span // N
    G = patch[:N * k, :N * k].reshape(N, k, N, k).mean((1, 3))
    S = hillshade(patch, z=230 * 1920 / 1024)[:N * k, :N * k].reshape(N, k, N, k).mean((1, 3))
    lo, hi = G.min(), G.max(); T = (G - lo) / (hi - lo)
    j0 = (SEC["y"] - y0) // k
    i0 = (SEC["x0"] - x0) // k; i1 = i0 + SEC["L"] // k
    W2, H2 = W * ss, Hh * ss
    img = Image.new("RGB", (W2, H2), rgb(bg)); d = ImageDraw.Draw(img)
    cw = W * scale / N * ss; a = cw / 2; b = cw / 4
    zs = (zscale or Hh * 0.34) * ss; bz = (base or Hh * 0.045) * ss
    ox = W2 / 2; oy = H2 * oyf
    jmax = j0 if cut else N - 1
    sample_of = {}
    for s_ in range(8):
        for i in range(i0 + s_ * (i1 - i0) // 8, i0 + (s_ + 1) * (i1 - i0) // 8): sample_of[i] = s_
    wall_l = rgb(mix(MOSS, BASALT, 0.35)); wall_r = rgb(mix(MOSS, BASALT, 0.62))
    poche = rgb(mix(MOSS, BASALT, 0.15))
    cells = sorted(((i, j) for j in range(jmax + 1) for i in range(N)), key=lambda c: c[0] + c[1])
    for i, j in cells:
        t = T[j, i]; z = bz + t * zs
        sx = ox + (i - j) * a; sy = oy + (i + j) * b - z
        lit = 0.68 + 0.6 * S[j, i]
        top = ramp_colour(t); topc = shade(top, lit)
        left = [(sx - a, sy), (sx, sy + b), (sx, sy + b + z), (sx - a, sy + z)]
        right = [(sx, sy + b), (sx + a, sy), (sx + a, sy + z), (sx, sy + b + z)]
        topf = [(sx, sy - b), (sx + a, sy), (sx, sy + b), (sx - a, sy)]
        front_edge = (j == jmax); right_edge = (i == N - 1)
        # left face (+j side): perimeter wall, section poché, or interior relief
        if front_edge and cut:
            d.polygon(left, fill=poche)
            if hi_samples and i in sample_of:                          # the measured band along the section
                band = 4.0 * b
                d.polygon([(sx - a, sy), (sx, sy + b), (sx, sy + b + band), (sx - a, sy + band)], fill=rgb(RAMP[TARGET[sample_of[i]]]))
        elif front_edge:
            d.polygon(left, fill=wall_l)
        else:
            d.polygon(left, fill=shade(top, 0.52 * lit))
        d.polygon(right, fill=wall_r if right_edge else shade(top, 0.36 * lit))
        d.polygon(topf, fill=topc)
    img = img.resize((W, Hh), Image.LANCZOS)
    img.save(out)
    return dict(j0=int(j0), i0=int(i0), i1=int(i1), N=N, cw=cw / ss, a=a / ss, b=b / ss, ox=ox / ss, oy=oy / ss, zs=zs / ss, bz=bz / ss)

if __name__ == "__main__":
    info = render(); print(info)
    render(cut=False, out="assets/voxel-whole.png")
