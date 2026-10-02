"""Digitised-mountain backgrounds for the identity studies (1920×1200).
Procedural terrain — illustrative, not real elevation data, no location implied."""
import numpy as np
from PIL import Image, ImageDraw
from terrain import massif, hillshade

import os
LICHEN = tuple(int(os.environ.get("LICHEN", "C9D36E")[i:i+2], 16) for i in (0, 2, 4))
PAL = dict(basalt=(14, 36, 35), moss=(46, 75, 67), sage=(114, 144, 124), lichen=LICHEN, chalk=(244, 245, 239))
W, H = 1920, 1200

def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def ramp(e):
    """Elevation → palette, low to high: Basalt → Moss → Sage → Lichen → Chalk."""
    stops = [(0.00, PAL["basalt"]), (0.45, PAL["basalt"]), (0.75, PAL["moss"]), (0.935, PAL["sage"]), (0.99, PAL["lichen"]), (0.9988, PAL["chalk"])]
    for (e0, c0), (e1, c1) in zip(stops, stops[1:]):
        if e <= e1: return lerp(c0, c1, (e - e0) / max(e1 - e0, 1e-6))
    return PAL["chalk"]

def terrain(seed=5):
    E = massif(H, W, seed=seed, zoom=W / 1024, layout="right")
    # colour by elevation percentile so the ramp spans the landform
    r = np.argsort(np.argsort(E.ravel())).reshape(E.shape) / E.size
    return r, hillshade(E, z=230 * W / 1024)

def mode_pixel(E, S, cell=16, gap=1):
    img = Image.new("RGB", (W, H), PAL["basalt"]); d = ImageDraw.Draw(img)
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            e = float(E[y:y+cell, x:x+cell].mean()); s = float(S[y:y+cell, x:x+cell].mean())
            c = ramp(e); k = 0.55 + 0.75 * s
            col = tuple(int(min(255, max(0, v * k))) for v in c)
            if e > 0.985: col = tuple(int(min(255, v * (0.82 + 0.22 * s))) for v in ramp(e))   # summits keep their colour, lightly shaded
            d.rectangle([x, y, x + cell - 1 - gap, y + cell - 1 - gap], fill=col)
    return img

def mode_dots(E, S, cell=14):
    img = Image.new("RGB", (W * 2, H * 2), PAL["basalt"]); d = ImageDraw.Draw(img)
    c2 = cell * 2
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            e = float(E[y:y+cell, x:x+cell].mean()); s = float(S[y:y+cell, x:x+cell].mean())
            r = c2 * (0.08 + 0.40 * max(0, (e - 0.25) / 0.75) ** 1.1)
            col = ramp(min(1, e * 0.92 + 0.12 * s))
            if e < 0.45: col = lerp(PAL["basalt"], PAL["moss"], 0.9)
            cx, cy = x * 2 + c2 / 2, y * 2 + c2 / 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(int(v) for v in col))
    return img.resize((W, H), Image.LANCZOS)

def mode_hillshade(E, S, cell=6, tones=6):
    small = lambda A: np.asarray(Image.fromarray(A.astype(np.float32), mode="F").resize((W // cell, H // cell), Image.BOX))
    e = small(E); s = small(S)
    base = [lerp(PAL["basalt"], PAL["moss"], t) for t in np.linspace(0, 1, tones - 1)] + [lerp(PAL["moss"], PAL["sage"], 0.45)]
    q = np.clip((s * (0.35 + 0.75 * e) * tones).astype(int), 0, tones - 1)
    rgb = np.zeros(e.shape + (3,), np.uint8)
    for k in range(tones): rgb[q == k] = base[k]
    return Image.fromarray(rgb).resize((W, H), Image.NEAREST)

if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    E, S = terrain(seed)
    np.save(f"assets/dem1920-{seed}.npy", E.astype(np.float32))
    mode_pixel(E, S).save(f"assets/bg-A-pixel-{seed}.png")
    mode_dots(E, S).save(f"assets/bg-B-dots-{seed}.png")
    mode_hillshade(E, S).save(f"assets/bg-C-hillshade-{seed}.png")
    print("ok", seed, float(E.mean()))
