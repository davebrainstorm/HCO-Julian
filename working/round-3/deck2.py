"""Boards 10–17: scale, rules, colour, ramp and pairings, typography, graphic language, imagery."""
import json, numpy as np
from base import *
from pixel import DIGITS
SEC = json.load(open("assets/section.json"))

def b10(D):
    base = Y(2) + 40; o = []; items = []; ol = "outline:1px solid rgba(244,245,239,.18);outline-offset:0"
    x = X(3)
    for name, w in (("primary-colour", 200), ("compact-colour", 96)):
        _, _, W, H = vb(name); h = w * H / W
        items.append(mkw(name, w, x, base - h)); o.append(tx(x, base + 24, f"{'Primary' if 'primary' in name else 'Compact'} · {w} px", INK2, 11)); x += w + 56
    for px in (180, 48, 32, 24, 16):
        items.append(img(f"marks/favicon-{px}.png", x, base - px, px, px, style=ol, cls="pix")); o.append(tx(x, base + 24, f"{px} px", INK2, 11)); x += px + 40
    o.append(tx(X(3), Y(1) - 24 + 16, "True size", CHALK, 11))
    y2 = Y(3) + 24; x = X(3)
    o.append(tx(X(3), y2 - 16, "Enlarged × 8 · pixel-snapped favicons", CHALK, 11))
    for px in (16, 24, 32):
        s_ = px * 8; items.append(img(f"marks/favicon-{px}-x8.png", x, y2, s_, s_, style=ol, cls="pix"))
        g = "".join(ln(x + i * 8, y2, x + i * 8, y2 + s_, BASALT, 1, None, .6) for i in range(1, px)) + "".join(ln(x, y2 + j * 8, x + s_, y2 + j * 8, BASALT, 1, None, .6) for j in range(1, px))
        o.append(g); o.append(tx(x, y2 + 256 + 24, f"{px} px · cell {2 if px == 16 else 3} px · no gap", INK2, 11)); x += s_ + 48
    spec = [("Primary", "Minimum 200 px wide on screen, 45 mm in print. Below this the descriptor falls under 6 pt."),
            ("Compact", "Minimum 96 px, 20 mm. Use it when the descriptor would be illegible."),
            ("Symbol", "Minimum 16 px, 6 mm. Below 48 px use the pixel-snapped files: whole-pixel cells, no gaps.")]
    body = (head("Scale", "Sharp from 16 px upward.", n="07", dark=True) + notes(0, Y(2) + 24, 3, spec, dark=True)
        + "".join(items) + svgl("".join(o)))
    D.add(10, body, "Family and use", "dk")

def b11(D):
    W_, H_ = WD(3), 216; tiles = []
    sy = 0.30
    def symg(x, y, m, **kw): return sym(x, y, m, **kw)
    def frame(i, bg, art, cap, img_=""):
        c = 3 * (i % 4); y = Y(1) + (i // 4) * 296; x = X(c)
        mark = rect(x + 16, y + 16, 24, 24, FLAG) + ln(x + 22, y + 22, x + 34, y + 34, BASALT, 2) + ln(x + 34, y + 22, x + 22, y + 34, BASALT, 2)
        return (at(x, y, img_, w=W_, h=H_, style=f"background:{bg};overflow:hidden") + svgl(art + mark)
                + at(x, y + H_ + 16, f'<div class="rule" style="padding-top:8px"><div class="lab">{i + 1:02d}<span style="display:inline-block;width:8px"></span>Never</div><p class="s mu" style="margin-top:4px">{cap}</p></div>', w=W_))
    def pos(i): return X(3 * (i % 4)), Y(1) + (i // 4) * 296
    m = 22; out = []
    x, y = pos(0); out.append(frame(0, BASALT, sym(x + 83, y + 53, m, heights=[0, 1, 2, 3, 4, 3, 2, 1]), "redraw, smooth or reorder the samples."))
    x, y = pos(1); out.append(frame(1, CHALK, sym(x + 83, y + 53, m) + rect(x, y, W_, H_, "none", "#d9dcd5"), "use the full-colour symbol on light grounds."))
    x, y = pos(2); out.append(frame(2, BASALT, sym(x + 83, y + 53, m, rx=6, stroke=LICHEN), "round, outline, bevel or shadow the cells."))
    x, y = pos(3); out.append(frame(3, BASALT, sym(x + 83, y + 53, m, colours=[FLAG, LICHEN, FLAG, "#5B8DEF", FLAG, LICHEN, "#5B8DEF", FLAG]), "recolour cells outside the elevation ramp."))
    x, y = pos(4); _, _, Wl, Hl = vb("compact-colour"); w = 230; h = w * Hl / Wl
    out.append(frame(4, BASALT, f'<g transform="translate({x + 20},{y + 108 - h * 0.7}) scale(1.30,0.70)"><svg viewBox="0 0 {Wl} {Hl}" width="{w}" height="{h}">{re.sub(r"^<svg[^>]*>|</svg>$", "", open("marks/compact-colour.svg").read())}</svg></g>', "stretch, condense or rotate the signature."))
    x, y = pos(5); out.append(frame(5, BASALT, sym(x + 40, y + 78, 12) + f'<text x="{x + 148}" y="{y + 138}" font-family="HCO Sans" font-weight="700" font-size="72" fill="{CHALK}">HCO</text>', "retype HCO in a typeface; use the artwork."))
    x, y = pos(6); out.append(frame(6, BASALT, f'<polygon points="{x + 60},{y + 175} {x + 171},{y + 40} {x + 282},{y + 175}" fill="none" stroke="{SAGE}" stroke-width="4"/>' + sym(x + 83, y + 53, m), "add a drawn mountain, sun or horizon."))
    x, y = pos(7); out.append(frame(7, BASALT, sym(x + 83, y + 53, m), "set the mark over busy imagery without a quiet field.",
                                    f'<img src="assets/bg-pixel.png" style="position:absolute;left:-560px;top:-120px;width:960px;height:600px">'))
    body = head("Rules", "Eight things the mark never does.", cs=6, n="07") + "".join(out)
    D.add(11, body, "Family and use")

def b12(D):
    cols = [("Basalt", BASALT, 0, 4, CHALK, "Ground. Text on light."), ("Chalk", CHALK, 4, 3, BASALT, "Light ground. Text on dark."),
            ("Moss", MOSS, 7, 2, CHALK, "Secondary dark ground."), ("Sage", SAGE, 9, 1, BASALT, "Ramp E1."),
            ("Lichen", LICHEN, 10, 1, BASALT, "Signal. Ramp E3."), ("Flag", FLAG, 11, 1, BASALT, "Observations only.")]
    out = []
    for name, hx, c, n, ink, role in cols:
        r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
        out.append(box(c, 1, n, 4, f'<div class="abs" style="left:16px;top:16px;right:12px"><div class="h3" style="color:{ink}">{name}</div></div>'
                       f'<div class="abs cap num" style="left:16px;bottom:16px;color:{ink};opacity:.82">{hx}<br>{r} {g} {b}</div>', f"background:{hx};{'outline:1px solid rgba(14,36,35,.12);outline-offset:-1px' if hx == CHALK else ''}"))
        out.append(at(X(c), Y(5) + 32, f'<p class="cap mu" style="padding-right:8px">{role}</p>', w=WD(n)))
    share = [(BASALT, 55), (CHALK, 25), (MOSS, 8), (SAGE, 5), (LICHEN, 5), (FLAG, 2)]; x = X(0); bar = []
    for hx, pc in share:
        w = WD(12) * pc / 100; bar.append(at(x, Y(5), "", w=w, h=8, style=f"background:{hx};{'outline:1px solid rgba(14,36,35,.12);outline-offset:-1px' if hx == CHALK else ''}")); x += w
    body = (head("Colour", "A Basalt ground. Colour as signal.", cs=8, n="08")
        + "".join(out) + "".join(bar)
        + at(X(8), Y(0) + 8, '<p class="cap mu">The bar below the swatches shows the share of a typical layout: Basalt 55, Chalk 25, Moss 8, Sage 5, Lichen 5, Flag 2. Print values (CMYK, Pantone) are matched on press proofs at Stage 2.</p>', w=WD(4)))
    D.add(12, body, "Colour", "st")

def rating(r):
    return "AAA" if r >= 7 else "AA" if r >= 4.5 else "Large / graphics" if r >= 3 else "Not for text"
def b13(D):
    out = []
    for k in range(5):
        y = Y(1) + (4 - k) * 112; c = E[k]
        L = to_oklab(c)[0]
        out.append(at(X(0), y, f'<div style="display:flex;height:96px"><div style="width:{L * 240:.0f}px;background:{c}"></div>'
                   f'<div class="abs" style="left:256px;top:4px"><div class="lab ac">E{k}</div><div class="cap mu num" style="margin-top:4px">{c}<br>OKLab L {L:.2f}<br>{contrast(c, BASALT):.2f}:1 on Basalt</div></div></div>', w=WD(4)))
    fgs = [("Chalk", CHALK), ("Lichen", LICHEN), ("E2", E[2]), ("Sage", SAGE), ("Flag", FLAG), ("Ink 2", INK2), ("Basalt", BASALT), ("Stone", STONE)]
    bgs = [("on Basalt", BASALT, 6), ("on Moss", MOSS, 8), ("on Chalk", CHALK, 10)]
    for nm, bg, c in bgs: out.append(at(X(c), Y(1), f'<div class="lab mu">{nm}</div>', w=WD(2)))
    for i, (fn, fc) in enumerate(fgs):
        y = Y(1) + 32 + i * 64
        out.append(at(X(4), y, f'<div class="rule" style="padding-top:8px"><div class="lab">{fn}</div><div class="cap mu num">{fc}</div></div>', w=WD(2)))
        for nm, bg, c in bgs:
            r = contrast(fc, bg); same = fc == bg
            out.append(box(c, 0, 2, 1, "" if same else f'<div style="display:flex;justify-content:space-between;align-items:flex-end;height:100%;padding:8px 12px">'
                           f'<span style="font-weight:600;font-size:24px;line-height:24px;color:{fc}">Aa</span><span class="cap num" style="color:{CHALK if bg != CHALK else BASALT};text-align:right">{r:.2f}:1<br>{rating(r)}</span></div>',
                           f"top:{y}px;height:56px;background:{bg};{'outline:1px solid rgba(14,36,35,.12);outline-offset:-1px' if bg == CHALK else ''}"))
    body = (head("Elevation ramp", "Five steps, even to the eye.", cs=6, n="08", dark=True)
        + "".join(out)
        + at(X(0), Y(5) + 56, '<p class="cap mu">Bar length = OKLab lightness.</p>', w=WD(3)) + at(X(4), Y(5) + 56, '<p class="cap mu">WCAG 2.2 contrast, computed from sRGB values. Text needs 4.5:1 (AA); large text and graphics need 3:1. E0 is for graphics only. Basalt on Lichen measures 10.06:1.</p>', w=WD(8)))
    D.add(13, body, "Colour", "dk")
from palette import to_oklab

def b14(D):
    w = [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700)]
    ws = "".join(f'<div class="rule" style="display:flex;justify-content:space-between;align-items:baseline;padding:8px 0 16px"><span style="font-weight:{v};font-size:40px;line-height:48px;letter-spacing:-.02em">Observe first.</span><span class="lab mu">{n} · {v}</span></div>' for n, v in w)
    ws += f'<div class="rule" style="display:flex;justify-content:space-between;align-items:baseline;padding:8px 0 16px"><span style="font-family:\'HCO Cond\';font-weight:600;font-size:40px;line-height:48px;letter-spacing:.02em;text-transform:uppercase">Field intelligence</span><span class="lab mu">Condensed · 600</span></div>'
    body = (head("Typography", "Instrument Sans for everything people read.", cs=4, n="09")
        + at(X(0), Y(2) + 8, f'<div style="font-weight:600;font-size:280px;line-height:280px;letter-spacing:-.05em">Aa</div>', w=WD(4))
        + at(X(0), Y(4) + 40, '<p class="s mu">A contemporary grotesk with a condensed width for labels. Pixel letters are kept for the wordmark and figures; text is always set in Instrument Sans.</p>'
             '<p class="cap mu" style="margin-top:16px">Licence: SIL Open Font License 1.1, which permits print, web and app use and embedding. Final typeface to be confirmed at Stage 2.</p>', w=WD(3))
        + at(X(5), Y(0) + 8, ws, w=WD(7))
        + at(X(5), Y(3) + 40, f'<div class="lab mu" style="margin-bottom:16px">Pairing</div><div style="display:flex;gap:24px;align-items:flex-start"><svg width="72" height="40" style="flex:none;overflow:visible">{pnum("03", 0, 0, 40, BASALT)}</svg>'
             '<div><div class="h3">Priority areas</div><p class="s mu" style="margin-top:4px">Pixel figures mark the number; Instrument Sans carries the words.</p></div></div>', w=WD(7))
        + at(X(5), Y(4) + 72, '<div class="lab mu" style="margin-bottom:8px">Character set (excerpt)</div><p style="font-size:20px;line-height:32px;letter-spacing:.01em">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br><span class="num">0123456789</span> &amp; @ € £ % ( ) → ·</p>', w=WD(7)))
    D.add(14, body, "Typography")

def b15(D):
    st = [("Display", "d1", "112 / 112 · −3.5% · 600", "Field to report."),
          ("Heading 1", "h1", "72 / 72 · −3% · 600", "Start with the problem."),
          ("Heading 2", "h2", "40 / 48 · −2% · 600", "We actually show up."),
          ("Heading 3", "h3", "24 / 32 · −1% · 600", "Practical. Not theory."),
          ("Body large", "bl", "20 / 32 · 400", "Your operation comes first."),
          ("Body", "b", "16 / 24 · 400", "We show up, learn the operation, identify the issue, and give you practical options for what to do next."),
          ("Label", "lab", "12 / 16 · Condensed 600 · +11% caps", "Field intelligence · Business & operations"),
          ("Caption", "cap", "12 / 16 · 400", "Figure 03 · Illustrative data, not survey results.")]
    hs = {"d1": 112, "h1": 72, "h2": 48, "h3": 32, "bl": 32, "b": 24, "lab": 16, "cap": 16}
    y = Y(1) - 8; out = []
    lines = "".join(ln(X(3), yy, X(12) - GUT, yy, FLAG, 1, None, .10) for yy in range(Y(1) - 8, 920, 8))
    for name, cls, spec, sample in st:
        h = hs[cls]
        out.append(at(X(0), y, f'<div class="lab">{name}</div><div class="cap mu num" style="margin-top:4px">{spec}</div>', w=WD(3)))
        out.append(at(X(3), y, f'<div class="{cls}" style="white-space:nowrap;overflow:hidden;text-overflow:clip">{e(sample)}</div>', w=WD(9), h=h, style="overflow:hidden"))
        y += max(h, 40) + 24
    body = (head("Type system", "One scale on an 8 px baseline.", cs=8, n="09") + svgl(lines, z=0) + "".join(out)
        + at(X(9), Y(0) + 8, '<p class="cap mu">Every size and line-height is a multiple of 8 px. Sample lines use the client’s own words from the existing flyer.</p>', w=WD(3)))
    D.add(15, body, "Typography")

def b16(D):
    o = []
    # 01 sample: monitoring chart from cells
    x0, y0 = X(0), Y(1) + 40; cm = 24; vals = [2, 3, 3, 5, 6, 8, 7, 9, 10, 9, 11, 12]
    for i, v in enumerate(vals):
        for j in range(v):
            t = min(4, j * 5 // 13); o.append(rect(x0 + i * (cm + 14) + 1, y0 + 12 * cm - (j + 1) * cm + 1, cm - 2, cm - 2, E[t]))
    o.append(tx(x0, y0 + 12 * cm + 28, "Repeat visits · illustrative counts", INK2, 11))
    # 02 profile: section at pixel resolution, 2-px pen
    prof = np.array(SEC["profile"]); x1 = X(4); p = 8; cols = WD(4) // p
    lv = np.round(np.interp(np.linspace(0, 95, cols), np.arange(96), prof) * 30).astype(int); yb = Y(1) + 40 + 34 * p
    for i, l in enumerate(lv):
        lo = l - 1
        for nb in (i - 1, i + 1):
            if 0 <= nb < cols and lv[nb] < lo: lo = lv[nb]
        for r in range(lo, l + 1): o.append(rect(x1 + i * p, yb - (r + 1) * p, p, p, E[min(4, max(0, r * 5 // 31))]))
    for s in range(8):
        xs = x1 + (WD(4) * s) / 8; o.append(ln(xs, yb + 8, xs, yb + 16, CHALK, 1, None, .4))
    o.append(tx(x1, yb + 40, "Section A–A · 2-px pen · stairs of 1 px", INK2, 11))
    # 03 flag: map tile with observations
    x2, y2 = X(8), Y(1) + 40; sz = HT(3); tile = img("assets/map-tile.png", x2, y2, sz, sz, cls="pix")
    cell = sz / 24
    for n_, (i, j) in zip(("01", "02", "03"), ((5, 17), (14, 9), (19, 15))):
        cx, cy = x2 + i * cell, y2 + j * cell
        o.append(rect(cx, cy, cell * 2, cell * 2, FLAG)); o.append(pnum(n_, cx + 4, cy + cell - 6, 12, BASALT))
    txt = [(0, "Sample", "The cell is the unit of every chart, bullet and progress mark. Counts are stacked, never smoothed."),
           (4, "Profile", "Lines are drawn with the wordmark’s pen: two pixels thick, stepping in single pixels."),
           (8, "Flag", "Flag marks an observation, numbered in pixel figures. The same marker appears on maps and in the field.")]
    body = (head("Graphic language", "Samples, profiles and flags.", cs=6, n="10", dark=True)
        + tile + svgl("".join(o))
        + "".join(at(X(c), Y(4) + 88, f'<div class="rule" style="padding-top:8px"><div class="lab ac">0{k + 1}<span style="display:inline-block;width:8px"></span>{h}</div><p class="s mu" style="margin-top:8px">{t}</p></div>', w=WD(4) - (24 if c < 8 else 0)) for k, (c, h, t) in enumerate(txt)))
    D.add(16, body, "Graphic language", "dk")

def b17(D):
    H = HT(4); W = WD(3); y = Y(1)
    panels = [(0, "Pixel ridgelines", "Covers, hero images, motion.", crop("assets/ridges-tall.png", 1200, 1680, 79 * 0 + 160, 0, H / 1680, X(0), y, W, H)),
              (3, "Block model", "Explaining method, reports.", crop("assets/voxel-whole.png", 3600, 2250, 1640, 100, 0.36, X(3), y, W, H)),
              (6, "Pixel map", "Maps, report spreads, screens.", crop("assets/bg-pixel.png", 1920, 1200, 1060, 40, 0.48, X(6), y, W, H, cls="pix")),
              (9, "Dot matrix", "Large formats, print texture.", crop("assets/bg-dots.png", 1920, 1200, 1060, 40, 0.48, X(9), y, W, H))]
    body = head("Imagery", "One dataset, four ways of seeing.", cs=6, n="11", dark=True)
    for c, h, t, im in panels:
        body += im + at(X(c), Y(5) - 8, f'<div class="rule" style="padding-top:8px"><div class="lab ac">{h}</div><p class="cap mu" style="margin-top:4px">{t}</p></div>', w=W)
    body += at(X(6), Y(0) + 8, '<p class="cap mu">All four are generated from one illustrative terrain model. For client work, regenerate them from licensed elevation data for the actual property. They are never survey outputs.</p>', w=WD(6))
    D.add(17, body, "Imagery", "dk")
