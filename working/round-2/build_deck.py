"""HCO Round 2 — logo design presentation. 16:10 boards (1600×1000 CSS px)."""
import re, json, html, numpy as np
from lockup import PAL, M
from designs import ALL
SYM = json.load(open("marks/symbols.json"))
F = "../fonts-ofl/"
def e(t): return html.escape(t, quote=False)
def mk(name, h=None, w=None, style=""):
    s = open(f"marks/{name}.svg").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r'^<svg[^>]*>|</svg>$', '', s)
    size = (f"height:{h}px;width:auto;" if h else "") + (f"width:{w}px;height:auto;" if w else "")
    return f'<svg viewBox="{vb}" style="{size}display:block;{style}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def vbw(name):
    vb = re.search(r'viewBox="([^"]+)"', open(f"marks/{name}.svg").read()).group(1).split(); return float(vb[2]), float(vb[3]), float(vb[0]), float(vb[1])

B, C, L, FL, SG, MO = PAL["basalt"], PAL["chalk"], PAL["lichen"], PAL["flag"], PAL["sage"], PAL["moss"]
CSS = f"""
@font-face{{font-family:'Instrument Sans';src:url('{F}instrumentsans/InstrumentSans[wdth,wght].ttf');font-weight:400 700;font-stretch:75% 100%}}
@font-face{{font-family:'Instrument Sans';src:url('{F}instrumentsans/InstrumentSans-Italic[wdth,wght].ttf');font-weight:400 700;font-style:italic;font-stretch:75% 100%}}
@page{{size:1600px 1000px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#c9ccc8}}
body{{font-family:'Instrument Sans';color:{B};-webkit-font-smoothing:antialiased;font-kerning:normal;font-variant-numeric:tabular-nums}}
.page{{width:1600px;height:1000px;position:relative;overflow:hidden;background:{C};break-after:page}}
@media screen{{.page{{margin:0 auto 24px}}}}
.dk{{background:{B};color:{C}}}
.abs{{position:absolute}}
.lab{{font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}}
.mut{{color:#5d6b64}} .dk .mut{{color:#93a79c}}
.h1{{font-size:60px;font-weight:600;line-height:1.02;letter-spacing:-.02em}}
.h2{{font-size:36px;font-weight:600;line-height:1.08;letter-spacing:-.012em}}
.h3{{font-size:22px;font-weight:600;line-height:1.2}}
.p{{font-size:19px;line-height:1.45}} .ps{{font-size:16px;line-height:1.45}} .xs{{font-size:12.5px;line-height:1.4;letter-spacing:.02em}}
.hd{{position:absolute;z-index:5;left:80px;right:80px;top:48px;display:flex;justify-content:space-between;font-size:13px;font-weight:500;letter-spacing:.04em}}
.rule{{border-top:1px solid #c2c8c2}} .dk .rule{{border-color:#2e4b43}}
.tag{{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:4px 9px;border:1px solid currentColor}}
.pix{{image-rendering:pixelated;display:block}}
.cap{{font-size:12.5px;letter-spacing:.04em;color:#6f8e7a}}
ul.l{{list-style:none}} ul.l li{{position:relative;padding-left:20px;margin-top:8px}} ul.l li::before{{content:"";position:absolute;left:0;top:9px;width:9px;height:9px;background:currentColor;opacity:.5}}
ul.l.pos li::before{{background:{SG};opacity:1}} ul.l.neg li::before{{background:{FL};opacity:1}}
"""
TOTAL = 16; pages = []
def pg(n, body, label, dark=False, hd=True, hl=None, hr=None):
    hl = hl or ("#93a79c" if dark else "#5d6b64"); hr = hr or hl
    h = f'<div class="hd"><span style="color:{hl}">HCO — Logo design · Round 2</span><span style="color:{hr}">{label} · {n:02d}/{TOTAL}</span></div>' if hd else ""
    pages.append((n, f'<section class="page{" dk" if dark else ""}">{h}{body}</section>'))

def grid_overlay(name, w_px, col="#2e4b43", sub=1):
    """Lines at every module over an SVG artwork displayed at width w_px."""
    W, H, x0, y0 = vbw(name); s = w_px / W; h_px = H * s
    lines = []
    x = 0.0
    while x <= W + 1:
        lines.append(f'<line x1="{(x - x0) * s:.1f}" y1="0" x2="{(x - x0) * s:.1f}" y2="{h_px:.1f}"/>'); x += M / sub
    y = 0.0
    while y <= H + 1:
        lines.append(f'<line x1="0" y1="{(y - y0) * s:.1f}" x2="{w_px:.1f}" y2="{(y - y0) * s:.1f}"/>'); y += M / sub
    return f'<svg style="position:absolute;left:0;top:0;width:{w_px}px;height:{h_px:.1f}px;overflow:visible" stroke="{col}" stroke-width="1" fill="none">{"".join(lines)}</svg>'

# ------------------------------------------------------------------------------------------------ 01 cover
pg(1, f"""
<img src="assets/bg-A-pixel-11.png" class="abs" style="inset:0;width:1600px;height:1000px;object-fit:cover">
<div class="abs lab" style="left:80px;top:64px;color:{C}">HCO / Logo design · Round 2</div>
<div class="abs" style="left:120px;top:395px">{mk("S3-lockup-below-colour", w=640)}</div>
<div class="abs ps" style="left:80px;bottom:64px;color:{C}">For approval · 2 October 2026</div>
<div class="abs cap" style="right:64px;bottom:64px">Illustrative terrain study · procedural, not real elevation data</div>
""", "Cover", dark=True, hd=False)

# ------------------------------------------------------------------------------------------------ 02 process
pg(2, f"""
<div class="abs" style="left:80px;top:110px;width:900px"><div class="lab mut">Process</div><div class="h1" style="margin-top:14px">Found in the terrain.<br>Drawn by hand.</div></div>
<div class="abs" style="left:80px;top:330px;width:440px"><div style="height:275px;overflow:hidden;background:{B}"><img src="assets/process-hillshade.png" style="width:100%;height:100%;object-fit:cover;display:block"></div>
 <div class="h3" style="margin-top:18px">1 · One dataset</div><p class="ps mut" style="margin-top:6px">Band-limited fractal terrain with ridged, anisotropic ranges. Illustrative and procedural: it is not real elevation data and implies no location.</p></div>
<div class="abs" style="left:580px;top:330px;width:440px"><div style="height:275px;overflow:hidden;display:grid;grid-template-rows:1fr 1fr 1fr;gap:4px;background:#c9ccc8">
  <img src="assets/process-plan-sheet.png" style="width:100%;height:100%;object-fit:cover;object-position:left top;display:block">
  <img src="assets/process-ridge-sheet.png" style="width:100%;height:100%;object-fit:cover;object-position:left top;display:block">
  <img src="assets/process-contour-sheet.png" style="width:100%;height:100%;object-fit:cover;object-position:left top;display:block"></div>
 <div class="h3" style="margin-top:18px">2 · 2,379 samples</div><p class="ps mut" style="margin-top:6px">Sampled from above (heightmaps, contours) and from the side (profiles), then filtered against the brief: ≤ 8 × 8 cells, one form, asymmetric, a small summit.</p></div>
<div class="abs" style="left:1080px;top:330px;width:440px"><div style="height:275px;overflow:hidden;display:grid;grid-template-rows:1fr 1fr;gap:4px;background:#c9ccc8">
  <img src="assets/process-designs-sheet.png" style="width:100%;height:100%;object-fit:cover;object-position:left top;display:block">
  <img src="assets/process-designs-sheet-2.png" style="width:100%;height:100%;object-fit:cover;object-position:left top;display:block"></div>
 <div class="h3" style="margin-top:18px">3 · 25 drawn, 3 survive</div><p class="ps mut" style="margin-top:6px">Redrawn by hand on the grid in clean runs. Contour rings read as eyes; most heightmaps read as blobs. Three studies go forward.</p></div>
<div class="abs" style="left:80px;right:80px;bottom:64px;border-left:6px solid {FL};padding-left:20px"><div class="lab">What the test changed</div>
<p class="p" style="margin-top:6px;max-width:1300px">The brief expected the view from above to win. It didn't. A side view survives the ziggurat and bar-chart traps once it plots the surface — one measured line — instead of filling the mass. That is study S3, Ridgeline.</p></div>
""", "Process")

# ------------------------------------------------------------------------------------------------ 03–05 studies
STUDY = {
 "S1": dict(n=3, title="Massif", kind="Plan raster", tag="",
   idea="The summit seen from above, as a drone survey would map it: a small heightmap of cells, coloured from Sage on the lower slopes to Lichen on the ridge and Chalk at the summit.",
   pos=["The richest use of the palette: the logo is literally a data tile.", "Holds at 16 px on a Basalt tile."],
   neg=["In one colour it falls back into a pixel peak — the stock “pixel mountain” form already sold as off-the-shelf outdoor logos.", "Without colour, the idea disappears."]),
 "S2": dict(n=4, title="Observation", kind="Plan raster with Flag", tag="",
   idea="Massif with one cell flagged in survey orange: the terrain measured, and the one place that needs attention marked. It is the business in one cell — identify the issue.",
   pos=["The strongest story of the three: data, then judgement.", "The Flag cell can carry through maps, reports and the website."],
   neg=["Shares Massif's one-colour weakness.", "At 16 px the Flag is a 2 × 2 px dot — legible, but fragile."]),
 "S3": dict(n=5, title="Ridgeline", kind="Profile, plotted as a measured line", tag="Recommended",
   idea="The ridge in section, plotted the way an elevation profile is: one measured cell per step, coloured by height. A long approach, the summit in Chalk, a short steep drop. Drawn with the same weight as the letters — one cell is one stem.",
   pos=["Reads at once as a mountain and as measured data — and not as a pyramid or a bar chart.", "Pixel-perfect at 16 px; the line and the letters share one stroke.", "Not found among existing pixel-mountain marks (search recorded, not clearance)."],
   neg=["In one colour it is close to a rising-line chart; the drop after the summit and the context have to do the work.", "Light next to the bold HCO at very small sizes — use the compact lockup below 120 px."]),
}
for k, st in STUDY.items():
    q = np.array(SYM[k]["cells"]); R, Cc = q.shape
    sym_w = 560 if Cc >= 8 else 480
    W, H, _, _ = vbw(f"{k}-symbol-colour"); sym_h = H * sym_w / W
    pg(st["n"], f"""
<div class="abs" style="left:0;top:0;width:760px;height:1000px;background:{B}"></div>
<div class="abs lab" style="left:80px;top:110px;color:#93a79c">Study {k[1]} · {st['kind']}</div>
<div class="abs h1" style="left:80px;top:140px;color:{C}">{st['title']}</div>
{f'<div class="abs tag" style="left:80px;top:226px;color:{L}">{st["tag"]}</div>' if st['tag'] else ''}
<div class="abs" style="left:{380 - sym_w/2:.0f}px;top:{560 - sym_h/2:.0f}px;width:{sym_w}px;height:{sym_h:.0f}px">{mk(f"{k}-symbol-colour", w=sym_w)}{grid_overlay(f"{k}-symbol-colour", sym_w, col="#2e4b43")}</div>
<div class="abs cap" style="left:80px;bottom:56px">{Cc} × {R} grid · {int((q > 0).sum())} cells · one module</div>
<div class="abs" style="left:840px;top:110px;width:680px">
 <div style="background:{B};height:170px;display:flex;align-items:center;padding:0 44px">{mk(f"{k}-lockup-below-colour", w=430)}</div>
 <div style="display:flex;gap:16px;margin-top:16px">
  <div style="flex:1;height:120px;border:1px solid #d3d7d2;display:flex;align-items:center;padding:0 26px">{mk(f"{k}-lockup-below-basalt", w=280)}</div>
  <div style="flex:1;height:120px;background:{B};display:flex;align-items:center;padding:0 26px">{mk(f"{k}-lockup-below-chalk", w=280)}</div>
 </div>
 <div style="display:flex;gap:30px;align-items:flex-end;margin-top:22px">
  <div><img class="pix" src="marks/{k}-favicon-16-x6.png" style="width:96px;height:96px"><div class="cap" style="margin-top:6px">16 px ×6</div></div>
  <div style="display:flex;gap:14px;align-items:flex-end;padding-bottom:22px"><img src="marks/{k}-favicon-16.png" style="width:16px;height:16px"><img src="marks/{k}-favicon-24.png" style="width:24px;height:24px"><img src="marks/{k}-favicon-32.png" style="width:32px;height:32px"></div>
  <div style="padding-bottom:22px" class="cap">Actual 16 · 24 · 32 px, pixel-aligned</div>
 </div>
 <p class="ps" style="margin-top:20px">{e(st['idea'])}</p>
 <div style="display:flex;gap:28px;margin-top:14px">
  <div style="flex:1"><div class="lab mut">Strengths</div><ul class="l pos ps" style="font-size:15px">{''.join(f'<li>{e(x)}</li>' for x in st['pos'])}</ul></div>
  <div style="flex:1"><div class="lab mut">Weaknesses</div><ul class="l neg ps" style="font-size:15px">{''.join(f'<li>{e(x)}</li>' for x in st['neg'])}</ul></div>
 </div>
</div>
""", f"Study {k[1]} · {st['title']}", hl="#93a79c", hr="#5d6b64")

# ------------------------------------------------------------------------------------------------ 06 wordmarks
def wm_panel(name, title, verdict, rec):
    w = 620; W, H, _, _ = vbw(f"{name}-basalt"); h = H * w / W
    return f"""<div style="flex:1">
 <div style="position:relative;width:{w}px;height:{h:.0f}px;margin:40px 0 0">{mk(f"{name}-basalt", w=w)}{grid_overlay(f"{name}-basalt", w, col="#b9c4bd")}</div>
 <div class="h3" style="margin-top:46px">{title} {'<span class="tag" style="color:'+SG+';margin-left:10px;vertical-align:3px">Recommended</span>' if rec else ''}</div>
 <p class="ps mut" style="margin-top:8px;max-width:600px">{verdict}</p></div>"""
pg(6, f"""
<div class="abs" style="left:80px;top:110px"><div class="lab mut">Wordmark</div><div class="h2" style="margin-top:12px">Drawn on the same module as the symbol</div></div>
<div class="abs" style="left:80px;right:80px;top:250px;display:flex;gap:80px">
 {wm_panel("W1", "W1 · High Bar", "Drawn letters on the module: stem = one cell, cap height = five cells, the raised crossbar sitting in row four (centre at 70%). Round, readable, and clearly custom next to a pixel symbol.", True)}
 {wm_panel("W2", "W2 · Grid-built", "Squared letters built from the module. Consistent with the symbol, but it reads as a display or game face and pulls the brand towards tech — exactly the drift the brief warns against.", False)}
</div>
<div class="abs cap" style="left:80px;bottom:56px">Grid lines show the 200-unit module (one symbol cell)</div>
""", "Wordmark")

# ------------------------------------------------------------------------------------------------ 07 family
def stacked(mono=None, w=300):
    # symbol above the wordmark, both on the module, left-aligned
    sym = f"S3-symbol-{'colour' if not mono else mono}"; lk = f"S3-lockup-below-{'colour' if not mono else mono}"
    Wl, Hl, _, _ = vbw(lk); Ws, Hs, _, _ = vbw(sym)
    return f'<div style="width:{w}px">{mk(sym, w=w * Ws / (Wl - (8 + 1.5) * M))}<div style="height:{w * M / (Wl - 9.5 * M):.1f}px"></div>{mk("W1-chalk" if not mono or mono == "chalk" else "W1-basalt", w=w)}</div>'
fam = lambda dark: f"""
 <div style="display:flex;align-items:center;gap:52px;height:300px">
  <div>{mk("S3-lockup-below-" + ("colour" if dark else "basalt"), w=470)}<div class="cap" style="margin-top:16px">Primary · with descriptor</div></div>
  <div>{mk("S3-lockup-none-" + ("colour" if dark else "basalt"), w=300)}<div class="cap" style="margin-top:16px">Compact</div></div>
  <div>{mk("S3-stacked-" + ("colour" if dark else "basalt"), w=165)}<div class="cap" style="margin-top:16px">Stacked</div></div>
  <div>{mk("W1-" + ("chalk" if dark else "basalt"), w=170)}<div class="cap" style="margin-top:16px">Wordmark</div></div>
  <div>{mk("S3-symbol-" + ("colour" if dark else "basalt"), w=120)}<div class="cap" style="margin-top:16px">Symbol</div></div>
 </div>"""
pg(7, f"""
<div class="abs" style="left:0;top:0;right:0;height:520px;background:{B}"></div>
<div class="abs lab" style="left:80px;top:110px;color:#93a79c">Recommended · Ridgeline with High Bar</div>
<div class="abs" style="left:80px;top:180px;color:{C}">{fam(True)}</div>
<div class="abs" style="left:80px;top:600px">{fam(False)}</div>
<div class="abs ps mut" style="left:80px;bottom:56px;max-width:1300px">Full colour only on Basalt. On Chalk and other light grounds, the one-colour Basalt version — Lichen on Chalk measures 1.47:1.</div>
""", "Logo family", hl="#93a79c")

# ------------------------------------------------------------------------------------------------ 08 construction
Wl, Hl, _, _ = vbw("S3-lockup-below-colour"); cw = 940; ch = Hl * cw / Wl; u = cw / Wl * M
ann = ["1 module = one cell = one stem", "Cap height = 5 modules", "Crossbar in row 4 of 5 (centre 70%)", "Symbol 8 × 5 cells, standing on the baseline",
       "Gap = 1 module; H = 4 modules wide", "Descriptor: the width of HCO, baseline 1.5 modules down", "Clear space = 2 modules on every side"]
lx = (1600 - cw) / 2
pg(8, f"""
<div class="abs lab" style="left:80px;top:110px;color:#93a79c">Construction</div>
<div class="abs h2" style="left:80px;top:140px;color:{C}">One measure for everything</div>
<div class="abs" style="left:{lx:.0f}px;top:{250 + 2*u:.0f}px;width:{cw}px;height:{ch:.0f}px">
 <div class="abs" style="left:{-2*u:.1f}px;top:{-2*u:.1f}px;width:{cw + 4*u:.1f}px;height:{ch + 4*u:.1f}px;border:1px dashed #6f8e7a"></div>
 {mk("S3-lockup-below-colour", w=cw)}{grid_overlay("S3-lockup-below-colour", cw, col="#2e4b43")}
</div>
<div class="abs" style="left:80px;right:80px;top:{250 + ch + 4*u + 34:.0f}px;display:grid;grid-template-columns:repeat(4,1fr);gap:0 36px;color:{C}">{''.join(f'<div class="rule" style="padding:10px 0"><span class="xs" style="color:#93a79c">{i+1:02d}</span> <span class="ps" style="font-size:15px">{e(t)}</span></div>' for i, t in enumerate(ann))}</div>
<div class="abs" style="left:80px;bottom:48px;right:80px;display:flex;gap:60px;color:{C}">
 <div><div class="lab" style="color:#93a79c">Minimum · primary</div><div class="ps" style="margin-top:6px">240 px wide on screen · 40 mm in print</div></div>
 <div><div class="lab" style="color:#93a79c">Minimum · compact</div><div class="ps" style="margin-top:6px">96 px wide · 18 mm</div></div>
 <div><div class="lab" style="color:#93a79c">Minimum · symbol</div><div class="ps" style="margin-top:6px">16 px (2 px per cell) · 5 mm</div></div>
 <div class="cap" style="align-self:flex-end">Provisional: print minimums to be proofed</div>
</div>
""", "Construction", dark=True)

# ------------------------------------------------------------------------------------------------ 09 small sizes
pg(9, f"""
<div class="abs" style="left:80px;top:110px"><div class="lab mut">Small sizes</div><div class="h2" style="margin-top:12px">Built for the pixel grid: every cell lands on whole pixels</div></div>
<div class="abs" style="left:80px;top:270px;display:flex;gap:46px;align-items:flex-end">
 {''.join(f'<div><img class="pix" src="marks/S3-favicon-{p}-x6.png" style="width:{p*6}px;height:{p*6}px"><div class="cap" style="margin-top:8px">{p} px · {c} px cells · ×6</div></div>' for p, c in ((16, 2), (24, 3), (32, 3)))}
 <div><img src="marks/S3-favicon-180.png" style="width:180px;height:180px;display:block;border-radius:40px"><div class="cap" style="margin-top:8px">180 px · app icon</div></div>
</div>
<div class="abs" style="left:80px;top:640px;width:900px">
 <div class="lab mut">At actual size</div>
 <div style="margin-top:14px;background:#e3e6e2;border-radius:10px 10px 0 0;width:560px;height:44px;display:flex;align-items:center;gap:10px;padding:0 16px">
  <div style="background:#fff;border-radius:8px 8px 0 0;height:36px;align-self:flex-end;display:flex;align-items:center;gap:9px;padding:0 14px;width:300px">
   <img src="marks/S3-favicon-16.png" style="width:16px;height:16px"><span style="font-size:13px">HCO — High Country Observations</span></div></div>
 <div style="background:{B};width:900px;height:72px;display:flex;align-items:center;padding:0 28px;justify-content:space-between">
  {mk("S3-lockup-none-colour", h=28)}<span style="color:{C};font-size:14px;display:flex;gap:28px"><span>Business &amp; operations</span><span>Field &amp; property intelligence</span><span>Contact</span></span></div>
 <div class="cap" style="margin-top:8px">Website header study · compact lockup at 28 px · illustrative navigation</div>
</div>
<div class="abs" style="left:1080px;top:640px;width:440px"><div class="lab mut">Rule</div><p class="ps" style="margin-top:8px">Below 120 px wide, drop the descriptor and use the compact lockup. Below 48 px, use the symbol alone. Favicons always sit on a Basalt tile, so the full-colour ramp stays legible.</p></div>
""", "Small sizes")

# ------------------------------------------------------------------------------------------------ 10 palette
def lum(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
def rgb(h): return ", ".join(str(int(h[i:i+2], 16)) for i in (1, 3, 5))
SW = [("Basalt", B, "Field · about 60%"), ("Chalk", C, "Type and light ground · about 25%"), ("Lichen", L, "Signal: the highest value · about 10%"), ("Flag", FL, "The observation · under 3%")]
TN = [("Moss", MO, "Ramp, low"), ("Sage", SG, "Ramp, mid")]
pairs = [("Chalk", C, "Basalt", B), ("Lichen", L, "Basalt", B), ("Flag", FL, "Basalt", B), ("Sage", SG, "Basalt", B), ("Basalt", B, "Chalk", C), ("Flag", FL, "Chalk", C), ("Lichen", L, "Chalk", C)]
rows = "".join(f'<tr style="border-bottom:1px solid #d6dad5"><td style="padding:7px 0"><span style="display:inline-block;width:14px;height:14px;background:{fc};outline:1px solid #ccc;vertical-align:-2px"></span> on <span style="display:inline-block;width:14px;height:14px;background:{bc};outline:1px solid #ccc;vertical-align:-2px"></span>&nbsp; {fa} / {ba}</td><td style="text-align:right">{cr(fc, bc):.2f}:1</td><td style="padding-left:18px;color:{"#141414" if cr(fc,bc) >= 3 else FL}">{"Text" if cr(fc,bc) >= 4.5 else ("Large text, graphics" if cr(fc,bc) >= 3 else "Never for text or marks")}</td></tr>' for fa, fc, ba, bc in pairs)
pg(10, f"""
<div class="abs" style="left:80px;top:110px"><div class="lab mut">Colour</div><div class="h2" style="margin-top:12px">The palette is the elevation ramp</div></div>
<div class="abs" style="left:80px;top:230px;width:860px;display:flex;gap:12px">
 {''.join(f'<div style="flex:{f}"><div style="height:170px;background:{h};{"border:1px solid #d3d7d2;" if n=="Chalk" else ""}padding:16px;display:flex;flex-direction:column;justify-content:flex-end;color:{B if n in ("Chalk","Lichen") else C}"><div class="h3">{n}</div><div class="xs" style="margin-top:4px">{h} · RGB {rgb(h)}</div></div><p class="ps" style="font-size:14.5px;margin-top:8px">{e(u)}</p></div>' for (n, h, u), f in zip(SW, (3, 2.2, 1.6, 1.3)))}
</div>
<div class="abs" style="left:80px;top:500px;width:860px">
 <div class="lab mut">Ramp · low → high · symbol, maps and reports</div>
 <div style="display:flex;margin-top:12px">{''.join(f'<div style="flex:1"><div style="height:46px;background:{h};{"border:1px solid #d3d7d2;" if h==C else ""}"></div><div class="xs mut" style="margin-top:6px">{n} {h}</div></div>' for n, h in [("Basalt", B), ("Moss", MO), ("Sage", SG), ("Lichen", L), ("Chalk", C)])}</div>
 <div style="display:flex;gap:24px;margin-top:40px;align-items:flex-start">
  <div style="width:300px"><img src="explore/lichen-test.png" style="width:300px;display:block;object-fit:cover;object-position:left;height:96px"><div class="cap" style="margin-top:6px">Study 01 lime #D6E65D (left) vs Lichen #C9D36E</div></div>
  <p class="ps" style="flex:1">Lichen moves from Study 01's lime (#D6E65D) to a mineral #C9D36E. It is still unmistakably the signal colour, at 10.06:1 on Basalt, but it reads as lichen on rock rather than the tech “volt” green that has dated fast since 2024.</p>
 </div>
</div>
<div class="abs" style="left:1000px;top:230px;width:520px"><div class="lab mut">Measured contrast (WCAG)</div><table class="ps" style="width:100%;border-collapse:collapse;margin-top:10px;font-size:14.5px">{rows}</table>
 <p class="cap" style="margin-top:18px;line-height:1.5">HEX and RGB only. No Pantone or CMYK until a print profile is agreed with a supplier.</p></div>
""", "Colour")

# ------------------------------------------------------------------------------------------------ 11 backgrounds
pg(11, f"""
<div class="abs lab" style="left:80px;top:110px;color:#93a79c">Background</div>
<div class="abs h2" style="left:80px;top:140px;color:{C}">One dataset, three renderings</div>
<div class="abs" style="left:80px;right:80px;top:240px;display:flex;gap:30px">
 {''.join(f'<div style="flex:1"><div style="height:300px;overflow:hidden"><img src="assets/{f}" style="width:100%;height:100%;object-fit:cover;object-position:75% 50%;display:block"></div><div class="h3" style="margin-top:16px;color:{C}">{t}</div><p class="ps" style="margin-top:6px;color:#c9d3cc;font-size:15px">{d}</p></div>' for f, t, d in [("bg-A-pixel-11.png", "A · Pixel heightmap", "Cells coloured by the ramp, lit by the relief. The symbol at full resolution — the hero mode."), ("bg-B-dots-11.png", "B · Dot matrix", "Dot size is elevation. A quieter, more editorial texture for reports and covers."), ("bg-C-hillshade-11.png", "C · Quantised hillshade", "Relief in six field tones, no signal colour. The quietest: safe under long text.")])}
</div>
<div class="abs" style="left:80px;right:80px;bottom:64px;display:flex;gap:60px;color:{C}">
 <div style="flex:1"><div class="lab" style="color:#93a79c">Rules</div><p class="ps" style="margin-top:6px;font-size:15px">Logo sits in the quiet lowland, never over a ridge. Text over terrain measures ≥ 4.5:1 against the busiest area beneath it. No glow, blur or cinematic lighting.</p></div>
 <div style="flex:1"><div class="lab" style="color:#93a79c">Data</div><p class="ps" style="margin-top:6px;font-size:15px">Procedural and labelled “Illustrative terrain study” until a real region is confirmed; then Copernicus GLO-30 (attributed) or USGS 3DEP. No place names or coordinates.</p></div>
</div>
""", "Background", dark=True)

# ------------------------------------------------------------------------------------------------ 12–14 identity studies
IS = [(12, "01", "S3", "bg-A-pixel-11.png", 600), (13, "02", "S2", "bg-B-dots-11.png", 600), (14, "03", "S1", "bg-C-hillshade-11.png", 600)]
for n, num, k, bg, w in IS:
    pg(n, f"""
<img src="assets/{bg}" class="abs" style="inset:0;width:1600px;height:1000px;object-fit:cover">
<div class="abs xs" style="left:120px;top:72px;color:{C};letter-spacing:.06em">HCO / IDENTITY STUDY {num} · {SYM[k]['name'].upper()}</div>
<div class="abs" style="left:120px;top:{500 - 0.5 * w * vbw(f'{k}-lockup-below-colour')[1] / vbw(f'{k}-lockup-below-colour')[0]:.0f}px">{mk(f"{k}-lockup-below-colour", w=w)}</div>
<div class="abs ps" style="left:120px;bottom:80px;color:{C}">Business &amp; operations · Field &amp; property intelligence</div>
<div class="abs cap" style="right:80px;bottom:80px">Illustrative terrain study</div>
""", f"Identity study {num}", dark=True, hd=False)

# ------------------------------------------------------------------------------------------------ 15 flat
pg(15, f"""
<div class="abs" style="left:80px;top:110px"><div class="lab mut">Without the background</div><div class="h2" style="margin-top:12px">Each study, flat — the test the terrain can't help with</div></div>
<div class="abs" style="left:80px;right:80px;top:250px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px">
 {''.join(f'<div><div style="height:200px;border:1px solid #d3d7d2;display:flex;align-items:center;justify-content:center">{mk(f"{k}-lockup-below-basalt", w=360)}</div><div style="height:200px;background:{B};display:flex;align-items:center;justify-content:center;margin-top:12px">{mk(f"{k}-lockup-below-colour", w=360)}</div><div class="h3" style="margin-top:16px">{k} · {SYM[k]["name"]}</div><p class="ps mut" style="margin-top:4px;font-size:15px">{v}</p></div>' for k, v in [("S3", "Still a measured ridge in one colour. Survives."), ("S2", "Flag lost in one colour; reads as a pixel peak."), ("S1", "Reads as a pixel peak — the stock form.")])}
</div>
""", "Flat")

# ------------------------------------------------------------------------------------------------ 16 evaluation
crit = ["Reads as terrain or data in five seconds", "Holds at 16 px (module ≥ 2 px)", "Works in one colour, no background", "Advisory practice, not drone vendor or outdoor brand", "Palette used as a data ramp", "Resemblance search (not clearance)"]
res = {"S3": ["pass", "pass", "pass", "pass", "pass", "pass"], "S2": ["pass", "partial", "partial", "pass", "pass", "partial"], "S1": ["pass", "pass", "fail", "partial", "pass", "fail"]}
note = {"S1": ["Heat-map tile", "", "Pixel peak in mono", "Leans outdoor", "", "Close to stock pixel-mountain logos"], "S2": ["", "Flag is 2 px", "Flag lost in mono", "", "", "Same family as stock pixel mountains"], "S3": ["", "Pixel-perfect", "Rising-line risk, held by the drop", "", "", "No close match found"]}
mark = {"pass": f'<span style="display:inline-block;width:14px;height:14px;background:{SG}"></span>', "partial": f'<span style="display:inline-block;width:14px;height:14px;border:3px solid {SG}"></span>', "fail": f'<span style="display:inline-block;width:14px;height:14px;background:{FL}"></span>'}
trs = "".join(f'<tr style="border-bottom:1px solid #d6dad5"><td style="padding:11px 0;width:460px">{e(c)}</td>' + "".join(f'<td style="padding:11px 12px 11px 0;width:300px">{mark[res[k][i]]} <span class="xs mut" style="margin-left:6px">{e(note[k][i])}</span></td>' for k in ("S3", "S2", "S1")) + "</tr>" for i, c in enumerate(crit))
pg(16, f"""
<div class="abs" style="left:80px;top:110px"><div class="lab mut">Evaluation</div><div class="h2" style="margin-top:12px">Judged against the brief</div></div>
<table class="abs ps" style="left:80px;top:220px;width:1440px;border-collapse:collapse;font-size:16px">
 <tr style="border-bottom:2px solid {B}"><td></td><td class="lab" style="padding-bottom:10px">S3 · Ridgeline</td><td class="lab" style="padding-bottom:10px">S2 · Observation</td><td class="lab" style="padding-bottom:10px">S1 · Massif</td></tr>{trs}</table>
<div class="abs xs mut" style="left:80px;top:690px">{mark['pass']} meets the brief &nbsp;&nbsp; {mark['partial']} partly &nbsp;&nbsp; {mark['fail']} fails — designer judgement from the artwork and tests, not measured data</div>
<div class="abs" style="left:80px;right:80px;bottom:64px;background:{B};color:{C};padding:30px 36px;display:flex;gap:50px;align-items:center">
 <div style="flex:none">{mk("S3-lockup-below-colour", w=330)}</div>
 <div><div class="lab" style="color:{L}">Recommendation</div><p class="p" style="margin-top:8px">S3 Ridgeline with the High Bar wordmark, the mineral Lichen palette and the pixel-heightmap background as hero. Keep S2's Flag cell as a system device for maps and reports, not in the logo. On approval: refine, build the logo family and export the identity pack.</p></div>
</div>
""", "Evaluation")

open("deck.html", "w").write(f"<!doctype html><html lang='en'><meta charset='utf-8'><title>HCO — Logo design, Round 2</title><style>{CSS}</style><body>{''.join(h for _, h in sorted(pages))}</body></html>")
print(len(pages), "boards")
