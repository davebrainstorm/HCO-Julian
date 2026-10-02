"""Procedural mountain terrain for HCO Round 2: spectral (1/f^β) fractal surfaces,
ridged and domain-warped, plus hillshade. Illustrative only — not real elevation
data, no location implied."""
import numpy as np, math

def spectral(h, w, beta, rng, kmax=None, aniso=1.0, angle=0.0):
    ky = np.fft.fftfreq(h)[:, None]; kx = np.fft.rfftfreq(w)[None, :]
    ca, sa = math.cos(angle), math.sin(angle)
    ku = kx * ca + ky * sa; kv = -kx * sa + ky * ca           # rotate, then stretch: elongated landforms
    k = np.sqrt(ku ** 2 + (aniso * kv) ** 2); k[0, 0] = 1
    amp = k ** (-beta / 2); amp[0, 0] = 0
    if kmax: amp *= np.exp(-(k / kmax) ** 4)          # band-limit: no pixel-scale noise
    ph = rng.uniform(0, 2 * np.pi, amp.shape)
    f = np.fft.irfft2(amp * np.exp(1j * ph), s=(h, w))
    return (f - f.mean()) / f.std()

def warp(field, dx, dy):
    h, w = field.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    xs = np.clip(xx + dx, 0, w - 1); ys = np.clip(yy + dy, 0, h - 1)
    x0 = xs.astype(int); y0 = ys.astype(int); x1 = np.clip(x0 + 1, 0, w - 1); y1 = np.clip(y0 + 1, 0, h - 1)
    fx = xs - x0; fy = ys - y0
    return (field[y0, x0] * (1 - fx) * (1 - fy) + field[y0, x1] * fx * (1 - fy) +
            field[y1, x0] * (1 - fx) * fy + field[y1, x1] * fx * fy)

def massif(h=640, w=1024, seed=11, zoom=1.0, layout='band'):
    rng = np.random.default_rng(seed)
    ang = math.radians(-36)                                   # ranges trend SW→NE
    base = spectral(h, w, 3.6, rng)
    ranges = spectral(h, w, 3.0, rng, kmax=0.03 / zoom, aniso=2.2, angle=ang)
    detail = spectral(h, w, 2.6, rng, kmax=0.09 / zoom)
    wx = spectral(h, w, 3.4, rng) * 20 * zoom; wy = spectral(h, w, 3.4, rng) * 20 * zoom
    crest = np.clip(1 - np.abs(warp(ranges, wx, wy)) / 2.2, 0, 1) ** 1.6     # broad, linear crests
    yy, xx = np.mgrid[0:h, 0:w] / np.array([h, w])[:, None, None]
    band = np.exp(-((xx * 0.8 + yy * 0.6 - 0.98) ** 2) / 0.07)
    if layout == "right":
        t = np.clip((xx - 0.30) / 0.45, 0, 1); t = t * t * (3 - 2 * t)
        band = np.clip(0.25 * band + t * (0.65 + 0.35 * np.exp(-((yy - 0.42) ** 2) / 0.18)), 0, 1)
    b = (base - base.min()) / (base.max() - base.min())
    d = (detail - detail.min()) / (detail.max() - detail.min())
    E = 0.30 * b + 0.75 * band * (0.35 + 0.65 * crest) + 0.10 * d * (0.2 + band)
    E = (E - E.min()) / (E.max() - E.min())
    return E ** 1.3

def hillshade(E, z=160.0, az=315, alt=42):
    gy, gx = np.gradient(E * z / max(E.shape) * 640)
    a, al = math.radians(az), math.radians(alt)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    s = np.sin(al) * np.cos(slope) + np.cos(al) * np.sin(slope) * np.cos(a - aspect)
    return np.clip(s, 0, 1)
if __name__ == "__main__":
    from PIL import Image
    seeds = (5, 11, 23, 37)
    for seed in seeds:
        E = massif(seed=seed); H = hillshade(E)
        np.save(f"assets/dem-{seed}.npy", E.astype(np.float32))
        rgb = np.dstack([H * 0.55 + E * 0.45] * 3)
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((512, 320), Image.LANCZOS).save(f"explore/dem-{seed}.png")
    sh = Image.new("RGB", (1044, 660), "white")
    for i, s in enumerate(seeds): sh.paste(Image.open(f"explore/dem-{s}.png"), ((i % 2) * 522, (i // 2) * 330))
    sh.save("explore/dem-sheet.png"); print("ok")
