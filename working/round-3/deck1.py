"""Boards 01–09: cover, introduction, origin, section, construction, numerals, family."""
import json, numpy as np
from base import *
from mark import M as MU, CAP as CU
from pixel import wordmark as pwm, FINAL, DIGITS
SEC = json.load(open("assets/section.json"))
INFO = dict(ox=1800, oy=675, a=16.125, b=8.0625, j0=48, i0=24, i1=72)      # voxel.py render geometry (image px)

def b01(D):
    lk = 720; k = lk / 4800; top = 872 - 1000 * k                            # wordmark baseline on 872
    body = (img("assets/bg-ridges.png", 0, 0, 1600, 1000)
        + at(X(0), Y(0), '<div class="lab ac">Identity system</div><div class="lab" style="margin-top:8px;color:%s">Round 3 — for review · October 2026</div>'
             '<div class="lab mu" style="margin-top:8px">Working draft · not for release</div>' % CHALK, w=WD(4))
        + mkw("primary-colour", lk, X(0), top))
    D.add(1, body, "Cover", "dk", chrome=False)

def b02(D):
    contents = [("Introduction", 2), ("Origin", 3), ("Symbol", 5), ("Wordmark", 6), ("Signature", 7), ("Numerals", 8), ("Family and use", 9),
                ("Colour", 12), ("Typography", 14), ("Graphic language", 16), ("Imagery", 17), ("Applications", 18), ("Decisions", 24)]
    rows = "".join(f'<div class="rule" style="display:flex;padding:7px 0 8px"><span class="s mu num" style="width:{COLW + GUT}px">{i + 1:02d}</span><span class="s" style="flex:1">{e(t)}</span><span class="s mu num">p. {p:02d}</span></div>' for i, (t, p) in enumerate(contents))
    body = (head("Introduction", "", n="01")
        + at(X(0), Y(0) + 56, '<div class="d1">The mountain,<br>measured.</div>', w=WD(8))
        + para(0, Y(2) + 40, 6, "HCO helps farmers, ranchers and agricultural businesses understand their land and their operation. "
               "The identity works the way the work does: observe first, then report clearly. The symbol is a measured section of terrain. "
               "The letters are drawn on the same pixel grid. The colours report elevation.", "bl")
        + at(X(8), Y(0), f'<div class="lab" style="margin-bottom:16px">Contents</div>{rows}', w=WD(4))
        + "".join(at(X(c), Y(4) + 48, f'<div class="rule" style="padding-top:16px"><svg width="40" height="20" style="display:block;overflow:visible">{pnum(n, 0, 0, 20, BASALT)}</svg>'
                     f'<div class="h3" style="margin-top:16px">{h}</div><p class="s mu" style="margin-top:8px">{t}</p></div>', w=WD(4) - 24 if c < 8 else WD(4))
                     for c, n, h, t in ((0, "01", "Measured, not drawn", "The symbol is eight samples of a real reading of the terrain model, not a picture of a mountain."),
                                        (4, "02", "One module, one pen", "A sample, a letter stroke and the layout unit are the same size: 1M. Letters are drawn in half-module pixels."),
                                        (8, "03", "Colour is data", "Colour encodes elevation or status. It is never decoration, and it lives on the dark ground."))))
    D.add(2, body, "Introduction")

def b03(D):
    sc = 0.46; L = 446 - 1010 * sc; T = 113 - 150 * sc
    ox, oy, a, b, j0 = INFO["ox"], INFO["oy"], INFO["a"], INFO["b"], INFO["j0"]
    def P(i): return (L + (ox + (i - j0) * a - a) * sc, T + (oy + (i + j0) * b) * sc)
    o = []
    for s in range(9):
        x, y = P(24 + 6 * s); o.append(ln(x, y + 10, x, y + 26, LICHEN, 1))
    for s in range(8):
        x1, y1 = P(24 + 6 * s); x2, y2 = P(30 + 6 * s); xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        o.append(tx(xm + 4, ym + 34, f"S{s + 1}", LICHEN, 11, "middle", rot=26.57))
    xa, ya = P(24); xb, yb = P(72)
    o.append(ln(xa, ya + 18, xb, yb + 18, LICHEN, 1))
    o.append(tx(xb + 16, yb + 30, "Section A–A · 8 samples", CHALK, 11, rot=26.57))
    steps = [("Terrain", "An illustrative model, 96 × 96 samples."), ("Section", "One cut, line A–A, across the summit."),
             ("Samples", "The surface averaged into eight intervals."), ("Symbol", "Each mean rounded to whole modules: 0 1 1 2 3 4 3 2.")]
    body = (img("assets/voxel.png", L, T, 3600 * sc, 2250 * sc)
        + svgl("".join(o))
        + head("Origin", "Every mark begins<br>as a measurement.", n="02", dark=True, cs=4)
        + para(0, Y(2), 3, "We cut a section through the terrain, averaged the surface into eight samples and rounded each to a whole module. "
               "The result is the symbol. It is not a drawing of a mountain; it is a reading of one.", "b mu")
        + notes(0, Y(3) + 72, 3, steps, dark=True)
        + at(X(0), 896, '<p class="cap mu">Procedural terrain for illustration. No real location is depicted or implied.</p>', w=WD(3)))
    D.add(3, body, "Origin", "dk")

def b04(D):
    prof = np.array(SEC["profile"]); smp = np.array(SEC["samples"]); lv = SEC["levels"]
    x0, x1 = X(4), X(12) - GUT; base = 616; u = 72
    def yv(v): return base - (v * 4 + 0.5) * u
    o = []
    for h in range(5):                                                       # level bands
        o.append(rect(x0, base - (h + 1) * u, x1 - x0, u, CHALK if h % 2 == 0 else "none", op=.035))
        o.append(tx(x1 + 12, base - (h + .5) * u + 4, f"L{h}", INK2, 11))
    for s in range(9):
        x = X(4 + s) - GUT / 2 if 0 < s < 8 else (x0 if s == 0 else x1)
        o.append(ln(x, base - 5 * u - 16, x, base + 8, CHALK, 1, "2 4", .35))
    for s in range(8):
        h = lv[s]; xs = X(4 + s)
        o.append(rect(xs, base - (h + 1) * u + 6, COLW, u - 12, E[h], op=.9))
    pts = " ".join(f"{x0 + (x1 - x0) * i / 95:.1f},{yv(v):.1f}" for i, v in enumerate(prof))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{CHALK}" stroke-width="2" stroke-linejoin="round"/>')
    for s in range(8):
        y = yv(smp[s]); xs = X(4 + s)
        h = lv[s]; o.append(ln(xs, y, xs + COLW, y, FLAG, 3)); o.append(tx(xs + COLW / 2, base - (h + 1) * u - 4, f"{smp[s] * 4:.2f} → {h}", INK2, 11, "middle"))
    o.append(tx(x0, base - 5 * u - 28, "Section A–A · continuous surface", CHALK, 11))
    o.append(tx(x1, base - 5 * u - 28, "Mean per sample → rounded to level", FLAG, 11, "end"))
    rows = [("Sample", [f"S{s + 1}" for s in range(8)], "lab"), ("Mean, normalised", [f"{v:.3f}" for v in smp], "s num"),
            ("× 4 levels", [f"{v * 4:.2f}" for v in smp], "s num"), ("Level", [str(v) for v in lv], "h3 num"), ("Ramp step", [f"E{v}" for v in lv], "lab")]
    tbl = []
    for i, (name, vals, cls) in enumerate(rows):
        y = Y(4) + 8 + i * 40
        tbl.append(at(X(0), y, f'<div class="rule" style="padding-top:8px" ></div>', w=WD(12)))
        tbl.append(at(X(0), y + 8, f'<div class="lab mu">{name}</div>', w=WD(3)))
        for s, v in enumerate(vals): tbl.append(at(X(4 + s), y + 8, f'<div class="{cls}" style="{"color:" + LICHEN if cls == "h3 num" else ""}">{v}</div>', w=COLW))
    sw = "".join(at(X(4 + s), Y(4) + 8 + 5 * 40 + 8, "", w=COLW, h=8, style=f"background:{E[v]}") for s, v in enumerate(lv))
    m = 28; body = (head("From section to symbol", "Read, average, round.", n="02", dark=True)
        + para(0, Y(1) + 40, 3, "The continuous surface (white) is averaged over eight equal intervals (orange). "
               "Each mean is scaled to five levels and rounded. Nothing is adjusted by eye.", "b mu")
        + svgl(sym(X(0), Y(4) - 5 * m - 40, m) + tx(X(0), Y(4) - 16, "Result · 8 × 5 modules", INK2, 11))
        + svgl("".join(o)) + "".join(tbl) + sw)
    D.add(4, body, "Origin", "dk")

def b05(D):
    m = 80; x0, y0 = X(4), 232; o = []
    for i in range(9): o.append(ln(x0 + i * m, y0, x0 + i * m, y0 + 5 * m, STONE, 1, None, .35))
    for j in range(6): o.append(ln(x0, y0 + j * m, x0 + 8 * m, y0 + j * m, STONE, 1, None, .35))
    o.append(sym(x0, y0, m, mono=BASALT))
    for i in range(8): o.append(tx(x0 + i * m + m / 2, y0 - 12, f"S{i + 1}", STONE, 11, "middle"))
    for h in range(5): o.append(tx(x0 - 16, y0 + (4 - h) * m + m / 2 + 4, f"L{h}", STONE, 11, "end"))
    o.append(hdim(x0, x0 + 8 * m, y0 - 48, "8M = 1600 u", ext=y0 - 24))
    o.append(vdim(x0 + 8 * m + 40, y0, y0 + 5 * m, "5M = 1000 u", left=False))
    o.append(hdim(x0, x0 + m, y0 + 5 * m + 32, "1M = 200 u", above=False, ext=y0 + 5 * m + 4))
    gx = x0 + 2 * m; gy = y0 + 3 * m
    o.append(ln(gx, gy + m / 2, x0 + m, y0 + 1.5 * m + 8, FLAG, 1)); o.append(f'<circle cx="{gx}" cy="{gy + m / 2}" r="5" fill="none" stroke="{FLAG}"/>')
    o.append(tx(x0 + 12, y0 + 1.5 * m, "Gap 0.1M = 20 u", BASALT, 11))
    o.append(ln(x0 - 32, y0 + 5 * m, x0 + 8 * m + 72, y0 + 5 * m, FLAG, 1, "6 4"))
    o.append(tx(x0 + 8 * m + 72, y0 + 5 * m + 18, "Baseline", BASALT, 11, "end"))
    keys = []
    for h in range(5):
        y = y0 + (4 - h) * m + 4
        keys.append(at(X(10), y, f'<div style="display:flex;gap:16px;align-items:flex-start"><div style="width:40px;height:{m - 8}px;background:{E[h]};outline:1px solid rgba(14,36,35,.18);outline-offset:-1px"></div>'
                    f'<div><div class="lab">E{h} · L{h}</div><div class="cap mu num" style="margin-top:4px">{E[h]}<br>{contrast(E[h], BASALT):.2f}:1 on Basalt</div></div></div>', w=WD(2)))
    body = (head("Symbol", "Ridgeline. Eight samples, one grid.", n="03")
        + para(0, Y(2) + 24, 3, "One cell per sample, standing on the baseline at its measured level. Colour follows level through the elevation ramp, E0 low to E4 summit.", "b mu")
        + svgl("".join(o)) + "".join(keys)
        + notes(3, Y(5) - 16, 3, [("Fixed sequence", "0 1 1 2 3 4 3 2. The samples are data and are never redrawn or reordered.")])
        + notes(6, Y(5) - 16, 3, start=2, items=[("Square cells", "Cells are square, unrounded and unoutlined. The 0.1M gap closes to zero at pixel sizes.")])
        + notes(9, Y(5) - 16, 3, start=3, items=[("Colour on dark", "The full-colour symbol sits on Basalt or Moss only. On light grounds use the one-colour version.")]))
    D.add(5, body, "Symbol")

def b06(D):
    p = 32; m = 2 * p; x0, y0 = X(3), 312; o = []
    path, W, info = pwm(**FINAL)
    for i in range(31): o.append(ln(x0 + i * p, y0 - 8, x0 + i * p, y0 + 10 * p + 8, STONE, 1, None, .22 if i % 2 else .45))
    for j in range(11): o.append(ln(x0 - 8, y0 + j * p, x0 + 30 * p + 8, y0 + j * p, STONE, 1, None, .22 if j % 2 else .45))
    o.append(wm(x0, y0, 10 * p, BASALT))
    xs = [x0, x0 + 8 * p, x0 + 10 * p, x0 + 19 * p, x0 + 20 * p, x0 + 30 * p]
    labs = ["H · 4M", "1M", "C · 4.5M", "0.5", "O · 5M"]
    for (a, b), l in zip(zip(xs, xs[1:]), labs): o.append(hdim(a, b, y0 - 40, l, ext=y0 - 16))
    o.append(hdim(x0, x0 + 30 * p, y0 - 88, "15M = 3000 u = 30 letter-pixels", ext=y0 - 64))
    o.append(vdim(x0 + 30 * p + 40, y0, y0 + 10 * p, "Cap 5M = 10 px", left=False))
    hy = y0 + 4 * p
    o.append(ln(x0 - 24, hy, x0 + 30 * p + 24, hy, FLAG, 1.5)); o.append(tx(x0 - 32, hy + 4, "Horizon 0.6", FLAG, 11, "end"))
    o.append(hdim(x0, x0 + 2 * p, y0 + 10 * p + 32, "Stroke 1M = 2 px", above=False, ext=y0 + 10 * p + 4))
    cx, cy = x0 + 20 * p + p, y0 + p
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{1.6 * p}" fill="none" stroke="{FLAG}" stroke-width="1.5"/>')
    o.append(ln(cx + 1.13 * p, cy + 1.13 * p, x0 + 23 * p + 4, y0 + 3 * p + 4, FLAG, 1)); o.append(tx(x0 + 23 * p + 8, y0 + 3 * p + 18, "Stair = 1 px at 45°", BASALT, 11))
    body = (head("Wordmark", "HCO, drawn in pixels.", n="04")
        + para(0, Y(1) + 56, 3, "A custom wordmark on a grid of half-module pixels. Stems are two pixels, curves step in single pixels, and the crossbar sits high: the horizon seen from high ground.", "b mu")
        + svgl("".join(o))
        + notes(3, Y(4) + 72, 3, [("One pen", "Every stroke is 2 px = 1M, the width of one sample in the symbol.")])
        + notes(6, Y(4) + 72, 3, start=2, items=[("One horizon", "The crossbar and the C’s upper jaw end on one line, 0.6 of the cap height above the baseline.")])
        + notes(9, Y(4) + 72, 3, start=3, items=[("No overshoot", "Pixels do not overshoot: H, C and O share one cap line and one baseline. Spacing is 2 px and 1 px.")]))
    D.add(6, body, "Wordmark")

def b07(D):
    m = 36; bx, by = X(3), Y(1); x0, y0 = bx + 2 * m, by + 2 * m; o = []
    _, _, Wl, Hl = vb("primary-basalt"); k = m / 200; lw, lh = Wl * k, Hl * k
    o.append(rect(bx, by, lw + 4 * m, lh + 4 * m, "none", FLAG, 1, "6 4"))
    for cx_, cy_ in ((bx, by), (bx + lw + 2 * m, by), (bx, by + lh + 2 * m), (bx + lw + 2 * m, by + lh + 2 * m)):
        o.append(rect(cx_, cy_, 2 * m, 2 * m, FLAG, op=.10)); o.append(rect(cx_, cy_, 2 * m, 2 * m, "none", FLAG, 1))
    o.append(tx(bx + m, by + m + 4, "2M", FLAG, 11, "middle"))
    xs = [x0, x0 + 8 * m, x0 + 9 * m, x0 + 24 * m]
    for (a, b), l in zip(zip(xs, xs[1:]), ["Symbol 8M", "1M", "Wordmark 15M"]): o.append(hdim(a, b, by - 24, l, ext=by - 4))
    o.append(vdim(bx + lw + 4 * m + 32, y0, y0 + 5 * m, "5M", left=False))
    dy = y0 + (1000 + 100) * k; o.append(ln(x0 + 9 * m - 8, y0 + 5 * m, x0 + 24 * m + 8, y0 + 5 * m, FLAG, 1, "3 3")); o.append(ln(x0 + 9 * m - 8, dy, x0 + 24 * m + 8, dy, FLAG, 1, "3 3"))
    o.append(tx(x0 + 24 * m + 16, dy - 2, "0.5M", FLAG, 11))
    for xx in (x0 + 9 * m, x0 + 24 * m): o.append(ln(xx, dy, xx, by + lh + 4 * m + 24, FLAG, 1, None, .5))
    o.append(hdim(x0 + 9 * m, x0 + 24 * m, by + lh + 4 * m + 24, "Descriptor ink = HCO ink = 15M", above=False))
    body = (head("Signature", "Symbol and wordmark, 24&nbsp;×&nbsp;5&nbsp;modules.", n="05")
        + para(0, Y(2) + 24, 3, "The symbol and HCO share cap line and baseline, one module apart. The descriptor is fitted to the ink width of HCO and hangs one letter-pixel below it.", "b mu")
        + mkw("primary-basalt", lw, x0, y0) + svgl("".join(o))
        + notes(3, Y(4) + 72, 3, [("Clear space", "2M on every side, measured from the ink. Nothing enters it: not text, not edges, not imagery detail.")])
        + notes(6, Y(4) + 72, 3, start=2, items=[("Descriptor", "High Country Observations, tracked uppercase, outlined. It is part of the artwork, never retyped.")])
        + notes(9, Y(4) + 72, 3, start=3, items=[("Name check", "“Group” or “Consulting” is not shown until the client confirms the trading name.")]))
    D.add(7, body, "Signature")

def b08(D):
    h = 120; o = [pnum("0123456789", X(3), Y(1) + 16, h, CHALK)]
    g = DIGITS["3"]; gx, gy, q = X(3), Y(3) + 48, 24
    for j in range(10):
        for i in range(8):
            o.append(rect(gx + i * q, gy + j * q, q - 1, q - 1, LICHEN if g[j, i] else CHALK, op=1 if g[j, i] else .05))
    o.append(tx(gx, gy + 10 * q + 32, "Construction · 8 × 10 px · tabular", INK2, 11))
    ex = []
    for c, lab, art in ((6, "Section number", pnum("07", X(6), gy + 40, 80, LICHEN)),
                        (8, "Observation marker", rect(X(8), gy + 40, 104, 80, FLAG) + pnum("03", X(8) + 24, gy + 60, 40, BASALT)),
                        (10, "Key figure", pnum("2026", X(10), gy + 40, 40, CHALK))):
        o.append(art); ex.append(at(X(c), gy, f'<div class="rule" style="padding-top:8px"><div class="lab mu">{lab}</div></div>', w=WD(2)))
    body = (head("Numerals", "Figures from the same pen.", n="06", dark=True)
        + para(0, Y(1) + 56, 3, "Ten bespoke pixel figures for the numbers that matter: sections, observations and key data. They are tabular, so columns align. Never use them for running text.", "b mu")
        + svgl("".join(o)) + "".join(ex))
    D.add(8, body, "Numerals", "dk")

def tile(c, r, cs, rs, bg, inner, label, lab_col=INK2):
    return box(c, r, cs, rs, inner + f'<div class="lab abs" style="left:24px;top:20px;color:{lab_col}">{label}</div>', f"background:{bg}")
def centre(name, c, r, cs, rs, w):
    _, _, W, H = vb(name); h = w * H / W
    return at(X(c) + (WD(cs) - w) / 2, Y(r) + (HT(rs) - h) / 2, mk(name, w=w, h=h), w=w, h=h)
def b09(D):
    body = (head("Family", "One signature, five configurations.", cs=6, n="07")
        + tile(0, 1, 8, 3, BASALT, "", "Primary") + centre("primary-colour", 0, 1, 8, 3, 624)
        + tile(8, 1, 4, 3, BASALT, "", "Symbol") + centre("symbol-colour", 8, 1, 4, 3, 224)
        + tile(0, 4, 4, 2, mix(BASALT, MOSS, .55), "", "Stacked") + centre("stacked-colour", 0, 4, 4, 2, 150)
        + tile(4, 4, 4, 2, "#E6E8E2", "", "Compact · one colour", STONE) + centre("compact-basalt", 4, 4, 4, 2, 312)
        + tile(8, 4, 4, 2, LICHEN, "", "Wordmark · one colour", BASALT) + centre("wordmark-basalt", 8, 4, 4, 2, 216))
    D.add(9, body, "Family")
