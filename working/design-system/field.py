"""Illustrative property dataset for Groundwork maps (procedural; not a real place, not survey data).
128 × 80 cells at 8 m = 65.5 ha. Layers: relative elevation, vegetation index (NDVI-like), red-edge index (NDRE-like), land class.
Also exports ridge profiles for the hero canvas. Run: python3 field.py"""
import json, math, sys, os
import numpy as np
sys.path.insert(0, "../round-2")
from terrain import spectral
rng = np.random.default_rng(7)
W, H, CELL = 128, 80, 8
Ed = np.load("../round-2/assets/dem1920-11.npy")

# relative elevation: a gentle lowland window of the seed-11 terrain, pooled 4 px → 1 cell
y0, x0 = 860, 180
win = Ed[y0:y0 + H * 4, x0:x0 + W * 4].reshape(H, 4, W, 4).mean((1, 3))
elev = (win - win.min()) / (win.max() - win.min())
ELEV_RANGE_M = 38                                     # relative relief shown in the legend

def noise(beta=2.2, kmax=None, seed=1):
    r = np.random.default_rng(seed); n = spectral(H, W, beta, r, kmax=kmax); return (n - n.mean()) / n.std()
YY, XX = np.mgrid[0:H, 0:W]
cls = np.full((H, W), "p")                             # p pasture/fallow, f crop, t track, w water, b structure
ndvi = 0.42 + 0.05 * noise(2.6, seed=2)
blocks = [dict(id="A", name="North paddock", crop="Cereal", x0=2, y0=2, x1=60, y1=37, base=0.74),
          dict(id="B", name="North-east block", crop="Cereal", x0=66, y0=2, x1=125, y1=37, base=0.66),
          dict(id="C", name="South flats", crop="Cereal", x0=2, y0=43, x1=60, y1=77, base=0.70)]
pivot = dict(id="D", name="Pivot 1", crop="Forage", cx=95.5, cy=60.5, r=16.5)
for b in blocks:
    m = (XX >= b["x0"]) & (XX <= b["x1"]) & (YY >= b["y0"]) & (YY <= b["y1"])
    cls[m] = "f"; ndvi[m] = b["base"] + 0.035 * noise(2.4, seed=hash(b["id"]) % 97)[m] + 0.012 * ((XX[m] % 2) - 0.5)
rr = np.hypot(XX - pivot["cx"], YY - pivot["cy"]); ang = (np.degrees(np.arctan2(YY - pivot["cy"], XX - pivot["cx"])) + 360) % 360
pm = rr <= pivot["r"]; cls[pm] = "f"; ndvi[pm] = 0.80 + 0.03 * noise(2.8, seed=11)[pm] - 0.004 * (rr[pm] % 3 < 1)
# problem areas (the observations)
wet = np.exp(-(((XX - 33) / 8.5) ** 2 + ((YY - 63) / 4.5) ** 2)); ndvi -= 0.42 * wet * (cls == "f")                      # 01 standing water
patch = np.clip(noise(2.0, seed=5), 0, None) * ((XX > 92) & (YY < 24)) * (cls == "f"); ndvi -= 0.20 * np.clip(patch, 0, 1.6)  # 02 uneven growth
arc = pm & (rr > pivot["r"] - 4) & (ang > 298) & (ang < 352); ndvi[arc] -= 0.24 + 0.05 * noise(2.5, seed=8)[arc]        # 04 dry arc on the outer span
# tracks, creek, dam, structures
cls[39:41, :] = "t"; cls[:, 62:64] = "t"
creek = np.zeros((H, W), bool)
for x in range(0, 61):
    yc = 70 + 4.5 * math.sin(x / 8.0) - x * 0.08; creek[int(round(yc)):int(round(yc)) + 2, x] = True
cls[creek] = "w"
dam = (np.abs(XX - 16.5) + np.abs(YY - 52.5) <= 4.5) & (np.maximum(np.abs(XX - 16.5), np.abs(YY - 52.5)) <= 3.5); cls[dam] = "w"
for (bx0, by0, bx1, by1) in ((66, 42, 72, 45), (74, 42, 77, 44), (66, 47, 69, 49)): cls[by0:by1 + 1, bx0:bx1 + 1] = "b"
ndvi[cls == "t"] = 0.12 + 0.02 * noise(3, seed=3)[cls == "t"]; ndvi[cls == "b"] = 0.06; ndvi[cls == "w"] = -0.08
ndvi = np.clip(ndvi, -0.1, 0.92)
ndre = np.clip(0.08 + 0.58 * (ndvi - 0.1) + 0.02 * noise(2.8, seed=9) - 0.06 * np.clip(patch, 0, 1.6), -0.1, 0.7)   # red edge shows the NE patch earlier
ndre[cls == "w"] = -0.05

obs = [dict(n="01", title="Standing water after rain", block="South flats", x=33, y=62, priority=1, kind="Drainage",
            text="Low vigour where water sits after rain. Check the drainage line before the next irrigation cycle."),
       dict(n="02", title="Uneven growth on the upper slope", block="North-east block", x=108, y=12, priority=2, kind="Crop health",
            text="Patchy canopy, clearer in the red-edge layer. Scout on foot to confirm the cause."),
       dict(n="03", title="Gap in the fence line", block="North-east block", x=125, y=20, priority=2, kind="Infrastructure",
            text="At the eastern gate. Repair before stock are moved."),
       dict(n="04", title="Dry arc on the outer span", block="Pivot 1", x=106, y=49, priority=1, kind="Irrigation",
            text="A consistent low-vigour arc on the last span. Check nozzles and pressure on that section.")]
flights = [dict(n="01", date="2026-08-12", area_ha=65.5, images=1218, status="Processed"),
           dict(n="02", date="2026-08-26", area_ha=65.5, images=1204, status="Processed"),
           dict(n="03", date="2026-09-09", area_ha=65.5, images=1231, status="Processed"),
           dict(n="04", date="2026-09-23", area_ha=65.5, images=1226, status="Processing")]
# block statistics (mean index per block per flight: illustrative trend)
def bmask(b): return (XX >= b["x0"]) & (XX <= b["x1"]) & (YY >= b["y0"]) & (YY <= b["y1"]) & (cls == "f")
stats = []
for b in blocks + [pivot]:
    m = pm if b["id"] == "D" else bmask(b)
    mean = float(ndvi[m].mean()); area = float(m.sum() * CELL * CELL / 1e4)
    trend = [round(mean - 0.09 + 0.03 * k + (0.01 if b["id"] == "A" else -0.012 * (k == 3) if b["id"] in "BD" else 0), 3) for k in range(4)]
    stats.append(dict(id=b["id"], name=b["name"], crop=b["crop"], area_ha=round(area, 1), ndvi=round(mean, 3), low_pct=round(100 * float((ndvi[m] < 0.5).mean()), 1), trend=trend))

def enc(a, lo, hi):           # 0…63 → base64url alphabet, one char per cell
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    q = np.clip(np.round((a - lo) / (hi - lo) * 63), 0, 63).astype(int)
    return "".join(al[v] for v in q.ravel())
data = dict(w=W, h=H, cell_m=CELL, elev=enc(elev, 0, 1), elev_range_m=ELEV_RANGE_M, ndvi=enc(ndvi, -0.1, 0.9), ndre=enc(ndre, -0.1, 0.7),
            ndvi_range=[-0.1, 0.9], ndre_range=[-0.1, 0.7], cls="".join(cls.ravel()),
            blocks=[{k: b[k] for k in ("id", "name", "crop", "x0", "y0", "x1", "y1")} for b in blocks], pivot=pivot, observations=obs, flights=flights, stats=stats,
            note="Illustrative data. Procedural terrain and vegetation; not a real property, not survey data.")
os.makedirs("../../review/hco/assets/data", exist_ok=True)
json.dump(data, open("../../review/hco/assets/data/field.json", "w"), separators=(",", ":"))
open("../../review/hco/assets/data/field.js", "w").write("/* Illustrative data, procedural. Not a real property; not survey data. */\nwindow.GW_FIELD=" + json.dumps(data, separators=(",", ":")) + ";\n")

# hero ridgelines: 20 profiles × 240 samples from the massif
R = np.argsort(np.argsort(Ed.ravel())).reshape(Ed.shape) / Ed.size
rows = np.linspace(200, 1180, 20).astype(int); xs = np.linspace(0, 1919, 240).astype(int)
lo, hi = Ed.min(), Ed.max()
ridge = dict(n=20, m=240, h=[enc((Ed[r, xs] - lo) / (hi - lo), 0, 1) for r in rows], t=[enc(R[r, xs], 0, 1) for r in rows])
json.dump(ridge, open("../../review/hco/assets/data/ridges.json", "w"), separators=(",", ":"))
open("../../review/hco/assets/data/ridges.js", "w").write("window.GW_RIDGES=" + json.dumps(ridge, separators=(",", ":")) + ";\n")

# QA render
from PIL import Image
sys.path.insert(0, "."); from tokens import VIGOUR, TERRAIN, MAP
def ramp(cols, t): t = min(max(t, 0), 1) * (len(cols) - 1); i = int(t); i2 = min(i + 1, len(cols) - 1); f = t - i
from colour import mix, hex2rgb
def col(cols, t):
    t = min(max(t, 0), 1) * (len(cols) - 1); i = int(t); i2 = min(i + 1, len(cols) - 1); return mix(cols[i], cols[i2], t - i)
img = Image.new("RGB", (W * 6 * 2 + 12, H * 6), (8, 24, 23)); P = img.load()
for y in range(H):
    for x in range(W):
        c1 = MAP["water"] if cls[y, x] == "w" else MAP["structure"] if cls[y, x] == "b" else col(VIGOUR, (ndvi[y, x] - 0.05) / 0.85)
        c2 = MAP["water"] if cls[y, x] == "w" else col(TERRAIN, elev[y, x])
        for k, c in ((0, c1), (1, c2)):
            rgb = tuple(int(v * 255) for v in hex2rgb(c))
            for dy in range(5):
                for dx in range(5): P[k * (W * 6 + 12) + x * 6 + dx, y * 6 + dy] = rgb
img.save("build/field-qa.png")
print("stats", stats); print("json kB", os.path.getsize("../../review/hco/assets/data/field.json") // 1024, "ridges kB", os.path.getsize("../../review/hco/assets/data/ridges.json") // 1024)
