"""Round 3 imagery from the single illustrative dataset (seed 11)."""
import numpy as np, json, sys
from PIL import Image, ImageDraw
sys.path.insert(0, "../round-2")
from terrain import hillshade
from voxel import ramp_colour, SEC, TARGET, rgb, shade
from palette import E as RAMP, BASALT, MOSS, CHALK, FLAG, mix

Ed = np.load("../round-2/assets/dem1920-11.npy"); H, W = Ed.shape
S = hillshade(Ed, z=230 * 1920 / 1024)
R = np.argsort(np.argsort(Ed.ravel())).reshape(Ed.shape) / Ed.size        # elevation percentile
from palette import hex2rgb
def frame_colour(t):
    """Full-frame ramp by percentile: Basalt-dominant, signal colours only on the top few percent."""
    stops = [(0.00, BASALT), (0.42, mix(BASALT, MOSS, 0.35)), (0.72, MOSS), (0.88, RAMP[0]), (0.945, RAMP[1]), (0.972, RAMP[2]), (0.988, RAMP[3]), (0.997, RAMP[4])]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b: return rgb(mix(ca, cb, max(0, min(1, (t - a) / (b - a)))))
    return rgb(RAMP[4])

def pixel_map(x0, y0, w, h, cells_x, out, cell_px=None, gap=1, lift=0.0, src=R, colour=None, bg=BASALT):
    """Top-down pixel heightmap: block-mean elevation per cell, ramp colour lit by relief."""
    k = w // cells_x; cy = h // k
    e = src[y0:y0 + cy * k, x0:x0 + cells_x * k].reshape(cy, k, cells_x, k).mean((1, 3))
    s = S[y0:y0 + cy * k, x0:x0 + cells_x * k].reshape(cy, k, cells_x, k).mean((1, 3))
    cp = cell_px or k
    colour = colour or frame_colour
    img = Image.new("RGB", (cells_x * cp, cy * cp), rgb(bg)); d = ImageDraw.Draw(img)
    for j in range(cy):
        for i in range(cells_x):
            t = min(1, e[j, i] + lift); c = colour(t); k2 = 0.70 + 0.50 * s[j, i]
            if t > 0.97: k2 = 0.90 + 0.14 * s[j, i]
            d.rectangle([i * cp, j * cp, (i + 1) * cp - 1 - gap, (j + 1) * cp - 1 - gap], fill=shade(c, k2))
    img.save(out); return e

if __name__ == "__main__":
    # A · full-frame pixel heightmap for identity studies (1920×1200, 16 px cells)
    pixel_map(0, 0, 1920, 1200, 120, "assets/bg-pixel.png", cell_px=16, gap=1)
    # report map tile: the block-model patch seen from above, 24 × 24 cells
    cx = SEC["x0"] + SEC["L"] // 2
    patch = Ed[SEC["y"] - 96:SEC["y"] + 96, cx - 96:cx + 96]; loc = np.zeros_like(Ed)
    loc[SEC["y"] - 96:SEC["y"] + 96, cx - 96:cx + 96] = (patch - patch.min()) / (patch.max() - patch.min())
    e = pixel_map(cx - 96, SEC["y"] - 96, 192, 192, 24, "assets/map-tile.png", cell_px=40, gap=3, src=loc, colour=ramp_colour)
    json.dump(np.round(e, 3).tolist(), open("assets/map-tile.json", "w"))
    # B · dot matrix
    img = Image.new("RGB", (3840, 2400), rgb(BASALT)); d = ImageDraw.Draw(img); c = 28
    for y in range(0, 2400, c):
        for x in range(0, 3840, c):
            t = float(R[y // 2:(y + c) // 2, x // 2:(x + c) // 2].mean()); s = float(S[y // 2:(y + c) // 2, x // 2:(x + c) // 2].mean())
            r = c * (0.06 + 0.40 * max(0, (t - 0.35) / 0.65) ** 1.6)
            col = frame_colour(min(1, t + 0.01 * s)) if t > 0.45 else rgb(mix(BASALT, MOSS, 0.85))
            d.ellipse([x + c / 2 - r, y + c / 2 - r, x + c / 2 + r, y + c / 2 + r], fill=col)
    img.resize((1920, 1200), Image.LANCZOS).save("assets/bg-dots.png")
    # section profile (continuous) + the eight samples
    row = Ed[SEC["y"], SEC["x0"]:SEC["x0"] + SEC["L"]]
    lo, hi = row.min(), row.max()
    json.dump({"profile": np.round((row - lo) / (hi - lo), 4).tolist(),
               "samples": np.round((row.reshape(8, -1).mean(1) - lo) / (hi - lo), 4).tolist(), "levels": TARGET}, open("assets/section.json", "w"), indent=0)
    print("ok")
