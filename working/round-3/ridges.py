"""Pixel ridgelines: stacked terrain profiles drawn with the wordmark's pen
(stroke = 2 pixels, 1-pixel stairs), nearer lines occlude farther ones.
Same illustrative dataset (seed 11). Not real elevation data."""
import numpy as np
from PIL import Image, ImageDraw
from assets import Ed, R, frame_colour, rgb
from palette import BASALT, MOSS, E as RAMP, mix
def ridges(out, W=1920, H=1200, cell=8, n=26, y0=180, y1=1500, amp=0.36, x0=0, xw=1920, gap=0, rows=None, fade=0.55, stroke=2, ramp=frame_colour, b0=0.30, b1=1.04):
    gw, gh = W // cell, H // cell
    img = Image.new("RGB", (W, H), rgb(BASALT)); d = ImageDraw.Draw(img)
    Hd, Wd = Ed.shape
    rows = rows if rows is not None else np.linspace(y0, min(y1, Hd - 1), n).astype(int)
    base_y = np.linspace(gh * b0, gh * b1, len(rows))                  # baselines in grid px, back → front
    xs = np.linspace(x0, x0 + xw - 1, gw).astype(int)
    lo, hi = Ed.min(), Ed.max()
    for k, (r, by) in enumerate(zip(rows, base_y)):
        prof = Ed[r, xs]; t = R[r, xs]
        h = (prof - lo) / (hi - lo) * gh * amp
        top = np.round(by - h).astype(int)
        depth = k / max(1, len(rows) - 1)                                    # 0 back … 1 front
        for i in range(gw):
            # occlusion: clear below the line down to the frame
            if (top[i] + stroke) * cell < H: d.rectangle([i * cell, (top[i] + stroke) * cell, (i + 1) * cell - 1, H], fill=rgb(BASALT))
        for i in range(gw):
            a = top[i]; lo_ = a + stroke - 1
            for nb in (i - 1, i + 1):                                       # keep the stroke continuous
                if 0 <= nb < gw and top[nb] > lo_: lo_ = max(lo_, top[nb])
            c = ramp(float(t[i])); c = tuple(int(v) for v in np.array(c) * (fade + (1 - fade) * depth) + np.array(rgb(BASALT)) * (1 - fade) * (1 - depth))
            for j in range(a, lo_ + 1):
                d.rectangle([i * cell + gap, j * cell + gap, (i + 1) * cell - 1 - gap, (j + 1) * cell - 1 - gap], fill=c)
    img.save(out); return img
if __name__ == "__main__":
    ridges("assets/bg-ridges.png", cell=12, n=18, amp=0.40, b0=0.42, b1=1.06)
    ridges("assets/bg-ridges-gap.png", cell=12, n=18, amp=0.40, b0=0.42, b1=1.06, gap=1)
    ridges("assets/ridges-tall.png", W=1200, H=1680, cell=12, n=20, x0=980, xw=940, amp=0.26, b0=0.40, b1=1.04)
    print("ok")
