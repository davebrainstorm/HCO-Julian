"""Evidence and principle diagrams for the v2 logo brief.
All terrain here is procedural (seeded) and labelled illustrative: it is not
real elevation data and implies no location."""
import numpy as np, io, math
from PIL import Image
import cairosvg

A = "assets/"
PAL = dict(basalt="#0E2423", moss="#2E4B43", sage="#6F8E7A", lichen="#D6E65D", chalk="#F4F5EF", flag="#EC5D2F")
RAMP = [PAL["moss"], PAL["sage"], PAL["lichen"], PAL["chalk"]]

# ------------------------------------------------------------- 1. reference at real sizes
ref = Image.open("refs/ref1-hco-identity-study-01.webp").convert("RGB").crop((146, 399, 485, 671))
for px in (16, 24, 32, 48):
    w = px; h = round(px * ref.height / ref.width)
    small = ref.resize((w, h), Image.LANCZOS)
    small.save(f"{A}ref1-symbol-{px}.png")
    small.resize((w * 8, h * 8), Image.NEAREST).save(f"{A}ref1-symbol-{px}-x8.png")
ref.save(f"{A}ref1-symbol-crop.png")

# ------------------------------------------------------------- 2. procedural terrain
rng = np.random.default_rng(7)
def value_noise(h, w, cells):
    g = rng.random((cells + 1, cells + 1))
    ys = np.linspace(0, cells, h, endpoint=False); xs = np.linspace(0, cells, w, endpoint=False)
    y0 = ys.astype(int); x0 = xs.astype(int); ty = ys - y0; tx = xs - x0
    ty = ty * ty * (3 - 2 * ty); tx = tx * tx * (3 - 2 * tx)
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    top = a + (b - a) * tx; bot = c + (d - c) * tx
    return top + (bot - top) * ty[:, None]
H, W = 300, 480
yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
ridge = np.exp(-((xx * 0.9 + yy * 0.45 - 0.82) ** 2) / 0.020)          # a diagonal range
peak = np.exp(-(((xx - 0.63) ** 2) / 0.010 + ((yy - 0.38) ** 2) / 0.020))  # one dominant summit, off-centre
noise = sum(value_noise(H, W, c) * (0.5 ** i) for i, c in enumerate([4, 9, 19, 41, 83]))
noise = (noise - noise.min()) / (noise.max() - noise.min())
Z = 0.55 * ridge + 0.75 * peak + 0.35 * noise * (0.4 + ridge)
Z = (Z - Z.min()) / (Z.max() - Z.min())
np.save(f"{A}terrain.npy", Z)

def quant(v, n): return np.clip((v * n).astype(int), 0, n - 1)

# ------------------------------------------------------------- 3. profile sampling principle
prof = Z.max(axis=0)                         # silhouette seen from the south
prof = (prof - prof.min()) / (prof.max() - prof.min())
def profile_svg(cols, rows, cell=None, line=False, w=300, h=150, fill=PAL["basalt"]):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">']
    if line:
        xs = np.linspace(0, w, len(prof)); pts = " ".join(f"{x:.1f},{h - v * h * 0.92:.1f}" for x, v in zip(xs, prof))
        out.append(f'<polygon points="0,{h} {pts} {w},{h}" fill="{fill}"/>')
    else:
        bins = np.array_split(prof, cols); cw = w / cols; rh = h / rows
        for i, b in enumerate(bins):
            lv = int(round(b.mean() * rows))
            for r in range(lv):
                out.append(f'<rect x="{i*cw:.2f}" y="{h-(r+1)*rh:.2f}" width="{cw+.05:.2f}" height="{rh+.05:.2f}" fill="{fill}"/>')
    out.append("</svg>"); return "".join(out)
open(f"{A}profile-continuous.svg", "w").write(profile_svg(0, 0, line=True))
sec = Z[int(0.40 * H), :] * 0.75 + Z[int(0.40 * H) - 25, :] * 0.25   # one section through the summit
sec = np.convolve(sec, np.ones(9) / 9, mode="same")
sec = (sec - sec.min()) / (sec.max() - sec.min())
_prof = prof
prof = sec
open(f"{A}section-continuous.svg", "w").write(profile_svg(0, 0, line=True))
open(f"{A}section-8.svg", "w").write(profile_svg(8, 5, w=300, h=187.5))
prof = _prof
open(f"{A}profile-32.svg", "w").write(profile_svg(32, 16))
open(f"{A}profile-16.svg", "w").write(profile_svg(16, 8))
open(f"{A}profile-8.svg", "w").write(profile_svg(8, 5, w=300, h=187.5))

# ------------------------------------------------------------- 4. plan raster principle (top-down)
def raster_svg(n_x, n_y, w=300, h=None, ramp=RAMP, gap=0.0, bg=PAL["basalt"]):
    h = h or w * n_y / n_x
    small = Image.fromarray((Z * 255).astype(np.uint8)).resize((n_x, n_y), Image.BOX)
    v = np.asarray(small) / 255.0
    q = quant(v, len(ramp) + 1)              # band 0 = background (lowest ground)
    cw, ch = w / n_x, h / n_y
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h:.2f}"><rect width="{w}" height="{h:.2f}" fill="{bg}"/>']
    for j in range(n_y):
        for i in range(n_x):
            k = q[j, i]
            if k == 0: continue
            out.append(f'<rect x="{i*cw+gap:.2f}" y="{j*ch+gap:.2f}" width="{cw-2*gap+.05:.2f}" height="{ch-2*gap+.05:.2f}" fill="{ramp[k-1]}"/>')
    out.append("</svg>"); return "".join(out)
open(f"{A}raster-96.svg", "w").write(raster_svg(96, 60))
open(f"{A}raster-24.svg", "w").write(raster_svg(24, 15))
open(f"{A}raster-8.svg", "w").write(raster_svg(8, 5))

# ------------------------------------------------------------- 5. background render modes (16:10)
BW, BH = 480, 300
open(f"{A}bg-pixel.svg", "w").write(raster_svg(64, 40, w=BW, h=BH, gap=0.35))
# dot matrix: dot radius = elevation
small = np.asarray(Image.fromarray((Z * 255).astype(np.uint8)).resize((60, 38), Image.BOX)) / 255.0
cw = BW / 60; ch = BH / 38
dots = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BW} {BH}"><rect width="{BW}" height="{BH}" fill="{PAL["basalt"]}"/>']
for j in range(38):
    for i in range(60):
        v = small[j, i]
        r = cw * (0.10 + 0.36 * v ** 0.9)
        col = RAMP[min(3, int(v * 4))] if v > 0.12 else PAL["moss"]
        dots.append(f'<circle cx="{(i+.5)*cw:.2f}" cy="{(j+.5)*ch:.2f}" r="{r:.2f}" fill="{col}"/>')
dots.append("</svg>"); open(f"{A}bg-dots.svg", "w").write("".join(dots))
# quantised hillshade: light from north-west, posterised to 5 tones of the field colour
gy, gx = np.gradient(Z * 60)
az, alt = math.radians(315), math.radians(40)
slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
shade = (shade - shade.min()) / (shade.max() - shade.min())
tones = [(14, 36, 35), (22, 50, 47), (36, 68, 61), (66, 98, 86), (120, 146, 124)]
qs = quant(shade, len(tones))
img = np.zeros((H, W, 3), np.uint8)
for k, t in enumerate(tones): img[qs == k] = t
hs = Image.fromarray(img).resize((96, 60), Image.BOX).resize((BW * 2, BH * 2), Image.NEAREST)
hs.save(f"{A}bg-hillshade.png")
print("assets written")
