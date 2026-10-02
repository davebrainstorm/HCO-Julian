"""Render the v2 logo brief: Markdown (agent-readable) + paginated HTML → PDF."""
import re, html
from content import *

# ================================================================= Markdown
md = [f"# HCO — Logo brief v2: {TITLE}", "", f"_{SUB}_", "", f"**Status:** {STATUS}", ""]
md += ["## 1. The ask", "", *[f"{i}. {a}" for i, a in enumerate(ASK, 1)], "", "**What still holds**", "", *[f"- {h}" for h in HOLDS], "", f"> **The tension.** {TENSION}", ""]
md += ["## 2. Reading the references", "", f"### {REF1['title']}", "", "![Study 01](refs/ref1-hco-identity-study-01.webp)", "",
       "**Measured:** " + " ".join(REF1["measured"]), "", "**Take**", *[f"- {t}" for t in REF1["take"]], "", "**Leave**", *[f"- {t}" for t in REF1["leave"]], "",
       "Small-size test (symbol cropped from the study and resampled): ![16 px ×8](assets/ref1-symbol-16-x8.png) ![32 px ×8](assets/ref1-symbol-32-x8.png)", ""]
for r in REFS:
    md += [f"### {r['title']}", "", f"![{r['title']}]({r['img']})", "", f"- **Take:** {r['take']}", f"- **Leave:** {r['leave']}", ""]
md += [f"_{BRACE}_", "", "### What the references agree on", "", *[f"{i}. **{a}.** {b}" for i, (a, b) in enumerate(PRINCIPLES, 1)], ""]
md += ["_The reference images in `refs/` are third-party work, kept for internal discussion only. Never publish or adapt them._", ""]
md += [f"## 3. The idea: {TITLE}", "", *IDEA, "", f"**Key finding.** {FINDING}", "",
       "Principle diagrams (procedural terrain, not logo proposals): side view ![silhouette](assets/profile-continuous.svg) → ![8 columns](assets/profile-8.svg) · section ![section](assets/section-continuous.svg) → ![8 columns](assets/section-8.svg) · plan view ![96](assets/raster-96.svg) → ![24](assets/raster-24.svg) → ![8×5](assets/raster-8.svg)", ""]
md += ["## 4. Requirements", "", "### Symbol", "", *[f"- **{a}.** {b}" for a, b in SYMBOL], "", "### Wordmark", "", *[f"- **{a}.** {b}" for a, b in WORDMARK], ""]
md += ["## 5. Colour: the palette is a data ramp", "", "| Role | Name | HEX | Use |", "|---|---|---|---|"]
md += [f"| Core | {n} | `{h}` | {u} |" for n, h, u in SWATCHES] + [f"| Ramp tint | {n} | `{h}` | {u} |" for n, h, u in TINTS]
md += ["", "**Measured contrast (WCAG 2.x)**", "", "| Foreground on background | Ratio | Use |", "|---|---|---|"]
for a, b, v in C["contrast"]:
    use = "text (AA)" if v >= 4.5 else ("large text and graphics" if v >= 3 else "not for text or marks")
    md.append(f"| {a.title()} on {b.title()} | {v}:1 | {use} |")
md += ["", f"_{LIME_RISK}_", "", "**Rules**", *[f"- {r}" for r in COLOUR_RULES], ""]
md += ["## 6. Background: digitised mountains", "", *[f"- **{a}.** {c} ![{a}]({b})" for a, b, c in BG_MODES], "", f"**Data.** {BG_DATA}", "", "**Rules**", *[f"- {r}" for r in BG_RULES], "", f"**Avoid:** {BG_AVOID}", ""]
md += ["## 7. This round", "", "### Deliverables", *[f"{i}. **{a}.** {b}" for i, (a, b) in enumerate(DELIVER, 1)], "", "### How we'll judge it", *[f"- {j}" for j in JUDGE], "", "### Open questions", *[f"{i}. {q}" for i, q in enumerate(QUESTIONS, 1)], ""]
open("HCO-Logo-Brief-v2.md", "w").write("\n".join(md))

# ================================================================= HTML
F = "../fonts-ofl/"
def inline_svg(path, style=""):
    s = open(path).read()
    s = re.sub(r'<svg ', f'<svg style="display:block;{style}" preserveAspectRatio="xMidYMid slice" ', s, count=1)
    return s
def e(t): return html.escape(t, quote=False)

CSS = f"""
@font-face{{font-family:'Hanken Grotesk';src:url('{F}hankengrotesk/HankenGrotesk[wght].ttf');font-weight:100 900}}
@font-face{{font-family:'Hanken Grotesk';src:url('{F}hankengrotesk/HankenGrotesk-Italic[wght].ttf');font-weight:100 900;font-style:italic}}
@font-face{{font-family:'IBM Plex Mono';src:url('{F}ibmplexmono/IBMPlexMono-Regular.ttf');font-weight:400}}
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#d9d9d6}}
body{{font-family:'Hanken Grotesk';color:#141414;-webkit-font-smoothing:antialiased;font-kerning:normal}}
.page{{width:297mm;height:210mm;background:#fff;position:relative;overflow:hidden;break-after:page}}
@media screen{{.page{{margin:0 auto 8mm;box-shadow:0 1px 6px rgba(0,0,0,.15)}}}}
.dark{{background:{PAL['basalt']};color:{PAL['chalk']}}}
.hd{{position:absolute;left:14mm;right:14mm;top:9mm;display:flex;justify-content:space-between;font-size:7.5pt;font-weight:500;letter-spacing:.02em;color:#6b6b6b;border-bottom:.5pt solid #cfcfcb;padding-bottom:2.2mm}}
.dark .hd{{color:#9fb0a6;border-color:#2e4b43}}
.abs{{position:absolute}}
.lab{{font-size:7.5pt;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:#6b6b6b}}
.dark .lab{{color:#9fb0a6}}
.t1{{font-size:25pt;line-height:1.08;font-weight:600;letter-spacing:-.012em}}
.t2{{font-size:14pt;line-height:1.15;font-weight:600}}
.p{{font-size:10.5pt;line-height:1.42}}
.ps{{font-size:9pt;line-height:1.4}}
.ill{{font-size:6.5pt;letter-spacing:.05em;text-transform:uppercase;color:#8a8a86}}
.rule{{border-top:.5pt solid #cfcfcb}}
ol.n{{list-style:none;counter-reset:n}} ol.n li{{counter-increment:n;position:relative;padding-left:6.5mm;margin-top:2mm}}
ol.n li::before{{content:counter(n,decimal-leading-zero);position:absolute;left:0;top:.2mm;font-size:7.5pt;font-weight:600;color:#8a8a86}}
ul.d{{list-style:none}} ul.d li{{position:relative;padding-left:4mm;margin-top:1.6mm}}
ul.d li::before{{content:"";position:absolute;left:0;top:1.75mm;width:1.6mm;height:1.6mm;background:currentColor;opacity:.55}}
ul.d.take li::before{{background:{PAL['sage']};opacity:1}} ul.d.leave li::before{{background:{PAL['flag']};opacity:1}}
.pix{{image-rendering:pixelated;display:block}}
.sw{{height:26mm;display:flex;flex-direction:column;justify-content:flex-end;padding:2.5mm;font-size:8pt;font-weight:600}}
"""
TOTAL = 9
pages = []
def pg(n, body, label, dark=False):
    pages.append(f'<section class="page{" dark" if dark else ""}"><div class="hd"><span>HCO — Logo brief v2 · {e(TITLE)}</span><span>{label} &nbsp;·&nbsp; {n:02d}/{TOTAL:02d}</span></div>{body}</section>')

# ---------------------------------------------------------- 01 cover
pg(1, f"""
<div class="abs" style="left:140mm;top:0;right:0;bottom:0">{inline_svg('assets/bg-pixel.svg', 'width:100%;height:100%')}</div>
<div class="abs" style="left:14mm;top:30mm;width:112mm">
 <div class="lab">Logo brief v2 · Draft for approval</div>
 <div class="t1" style="font-size:40pt;margin-top:7mm;line-height:1.0">The mountain,<br>measured.</div>
 <p class="p" style="margin-top:8mm;color:#c9d3cc">{e(SUB)}</p>
 <p class="ps" style="margin-top:4mm;color:#9fb0a6">{e(STATUS)}</p>
</div>
<div class="abs" style="left:14mm;bottom:14mm;width:112mm;display:flex;gap:6mm">
 {''.join(f'<div style="flex:1;border-top:.5pt solid #2e4b43;padding-top:2mm"><div class="lab">{a}</div><div class="ps" style="margin-top:1mm;color:#c9d3cc">{b}</div></div>' for a, b in [("01–02","The ask and the references"),("03","The idea"),("04–06","Symbol, colour, background"),("07","This round")])}
</div>
<div class="abs ill" style="left:14mm;bottom:6mm;color:#6f8e7a">Illustrative terrain study · procedural, not real elevation data</div>
""", "Cover", dark=True)

# ---------------------------------------------------------- 02 ask
pg(2, f"""
<div class="abs" style="left:14mm;top:24mm;width:170mm"><div class="lab">01 · The ask</div><div class="t1" style="margin-top:3mm">Bring the mountain back — as data, not scenery.</div></div>
<div class="abs" style="left:14mm;top:58mm;width:84mm"><div class="lab" style="color:#141414">What you asked for</div><ol class="n ps" style="margin-top:1mm">{''.join(f'<li>{e(a)}</li>' for a in ASK)}</ol></div>
<div class="abs" style="left:106mm;top:58mm;width:84mm"><div class="lab" style="color:#141414">What still holds</div><ul class="d ps" style="margin-top:1mm">{''.join(f'<li>{e(h)}</li>' for h in HOLDS)}</ul></div>
<div class="abs" style="left:199mm;top:58mm;width:84mm;background:{PAL['basalt']};color:{PAL['chalk']};padding:6mm 6mm 7mm">
 <div class="lab" style="color:{PAL['lichen']}">The tension</div><p class="p" style="margin-top:2.5mm;font-size:10pt">{e(TENSION)}</p></div>
<div class="abs" style="left:0;right:0;bottom:0;height:58mm">{inline_svg('assets/bg-pixel.svg', 'width:100%;height:100%')}</div>
<div class="abs ill" style="left:14mm;bottom:4mm;color:#9fb0a6">Terrain as data · illustrative, procedural</div>
""", "The ask")

# ---------------------------------------------------------- 03 reference 1
pg(3, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">02 · Reading the references</div><div class="t2" style="margin-top:2mm">{REF1['title']}</div></div>
<div class="abs" style="left:14mm;top:40mm;width:150mm"><img src="refs/ref1-hco-identity-study-01.webp" style="width:150mm;display:block"></div>
<div class="abs" style="left:14mm;top:139mm;width:150mm;display:flex;gap:6mm;align-items:flex-end">
 <div><img class="pix" src="assets/ref1-symbol-16-x8.png" style="width:25.6mm"><div class="ill" style="margin-top:1mm">16 px, enlarged ×8</div></div>
 <div style="display:flex;gap:3mm;align-items:flex-end;padding-bottom:4mm"><img src="assets/ref1-symbol-16.png" style="width:16px"><img src="assets/ref1-symbol-24.png" style="width:24px"><img src="assets/ref1-symbol-32.png" style="width:32px"><img src="assets/ref1-symbol-48.png" style="width:48px"></div>
 <div style="flex:1"><div class="lab" style="color:#141414">Measured</div><ul class="d ps" style="margin-top:.5mm;font-size:8.3pt">{''.join(f'<li>{e(m)}</li>' for m in REF1['measured'])}</ul></div>
</div>
<div class="abs ill" style="left:14mm;top:198mm">Actual size: 16 · 24 · 32 · 48 px — the symbol cropped from the study and resampled</div>
<div class="abs" style="left:174mm;top:40mm;width:109mm">
 <div class="lab" style="color:#141414">Take</div><ul class="d take ps" style="margin-top:.5mm">{''.join(f'<li>{e(t)}</li>' for t in REF1['take'])}</ul>
 <div class="lab" style="color:#141414;margin-top:6mm">Leave</div><ul class="d leave ps" style="margin-top:.5mm">{''.join(f'<li>{e(t)}</li>' for t in REF1['leave'])}</ul>
</div>
""", "References")

# ---------------------------------------------------------- 04 references 2–5 + synthesis
cards = ""
for r in REFS:
    cards += f"""<div style="flex:1">
 <div style="height:40mm;background:{r['bg']};display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{r['img']}" style="max-width:100%;max-height:40mm;display:block"></div>
 <div class="t2" style="font-size:11pt;margin-top:2.5mm">{e(r['title'])}</div>
 <ul class="d take ps" style="font-size:8.5pt;margin-top:.5mm"><li>{e(r['take'])}</li></ul>
 <ul class="d leave ps" style="font-size:8.5pt;margin-top:.5mm"><li>{e(r['leave'])}</li></ul></div>"""
pg(4, f"""
<div class="abs" style="left:14mm;top:24mm;width:150mm"><div class="lab">02 · Reading the references</div><div class="t2" style="margin-top:2mm">Four more, and what they agree on</div></div>
<div class="abs ps" style="left:183mm;top:24mm;width:100mm;color:#5e5e5b;font-size:8.3pt">{e(BRACE)}</div>
<div class="abs" style="left:14mm;right:14mm;top:42mm;display:flex;gap:6mm">{cards}</div>
<div class="abs" style="left:14mm;right:14mm;top:142mm;background:{PAL['basalt']};color:{PAL['chalk']};padding:5mm 6mm;display:flex;gap:6mm">
 {''.join(f'<div style="flex:1"><div class="lab" style="color:{PAL["lichen"]}">{i:02d} · {a}</div><p class="ps" style="margin-top:1.5mm">{e(b)}</p></div>' for i, (a, b) in enumerate(PRINCIPLES, 1))}
</div>
<div class="abs ill" style="left:14mm;bottom:5mm">Third-party references, kept for internal discussion only — not to be published or adapted</div>
""", "References")

# ---------------------------------------------------------- 05 the idea
def dia(path, w, h, label, note=None, bg=PAL['chalk']):
    return f"""<div><div style="width:{w}mm;height:{h}mm;background:{bg};overflow:hidden">{inline_svg(path, 'width:100%;height:100%')}</div>
<div class="ill" style="margin-top:1.2mm;color:#5e5e5b">{label}</div>{f'<div class="ps" style="font-size:8pt;font-weight:600;color:{PAL["flag"]};margin-top:.4mm">{note}</div>' if note else ''}</div>"""
arrow = '<div style="align-self:center;font-size:12pt;color:#8a8a86;padding-bottom:6mm">→</div>'
pg(5, f"""
<div class="abs" style="left:14mm;top:24mm;width:96mm"><div class="lab">03 · The idea</div>
 <div class="t1" style="margin-top:3mm">{TITLE}.</div>
 {''.join(f'<p class="p" style="margin-top:4mm;font-size:10pt">{e(p)}</p>' for p in IDEA)}
 <div style="margin-top:5mm;border-left:1.2mm solid {PAL['flag']};padding-left:4mm"><div class="lab" style="color:#141414">Key finding</div><p class="ps" style="margin-top:1mm">{e(FINDING)}</p></div>
</div>
<div class="abs" style="left:120mm;top:24mm;width:163mm">
 <div class="lab" style="color:#141414">Side view</div>
 <div style="display:flex;gap:3mm;margin-top:2mm;align-items:flex-start">
  {dia('assets/profile-continuous.svg', 38, 21, 'Silhouette')}{arrow}{dia('assets/profile-8.svg', 28, 21, '8 columns', 'Ziggurat')}
  <div style="width:2mm"></div>
  {dia('assets/section-continuous.svg', 38, 21, 'One section')}{arrow}{dia('assets/section-8.svg', 28, 21, '8 columns', 'Bar chart')}
 </div>
 <div class="lab" style="color:#141414;margin-top:12mm">Plan view · the way a drone sees it</div>
 <div style="display:flex;gap:3mm;margin-top:2mm;align-items:flex-start">
  {dia('assets/raster-96.svg', 58, 36.25, '96 × 60 cells · the background')}{arrow}{dia('assets/raster-24.svg', 40, 25, '24 × 15 cells')}{arrow}{dia('assets/raster-8.svg', 40, 25, '8 × 5 cells · the scale of a symbol')}
 </div>
 <div class="ill" style="margin-top:6mm">Principle diagrams from one procedural terrain — illustrative, not real elevation data and not logo proposals</div>
</div>
""", "The idea")

# ---------------------------------------------------------- 06 requirements
def grid_svg():
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 164 124" style="width:100%;display:block">']
    for i in range(9):
        s.append(f'<line x1="{i*10}" y1="0" x2="{i*10}" y2="80" stroke="#b9bfb9" stroke-width=".3"/><line x1="0" y1="{i*10}" x2="80" y2="{i*10}" stroke="#b9bfb9" stroke-width=".3"/>')
    s.append(f'<rect x="0" y="0" width="80" height="80" fill="none" stroke="{PAL["basalt"]}" stroke-width=".8"/>')
    s.append(f'<rect x="0" y="70" width="10" height="10" fill="{PAL["basalt"]}"/>')
    s.append('<text x="0" y="90" font-size="4.2" font-family="Hanken Grotesk" fill="#5e5e5b">8 × 8 maximum. One filled module shown.</text>')
    s.append('<text x="0" y="96" font-size="4.2" font-family="Hanken Grotesk" fill="#5e5e5b">At 16 px: 16 ÷ 8 = 2 px per module.</text>')
    # H on 8 rows with crossbar in row 6
    ox = 100
    for i in range(9):
        s.append(f'<line x1="{ox}" y1="{i*10}" x2="{ox+56}" y2="{i*10}" stroke="#b9bfb9" stroke-width=".3"/>')
    s.append(f'<rect x="{ox+4}" y="0" width="10" height="80" fill="{PAL["basalt"]}"/><rect x="{ox+42}" y="0" width="10" height="80" fill="{PAL["basalt"]}"/><rect x="{ox+14}" y="20" width="28" height="10" fill="{PAL["basalt"]}"/>')
    s.append(f'<text x="{ox}" y="90" font-size="4.2" font-family="Hanken Grotesk" fill="#5e5e5b">W1: crossbar in row 6 of 8;</text>')
    s.append(f'<text x="{ox}" y="96" font-size="4.2" font-family="Hanken Grotesk" fill="#5e5e5b">stem = one module.</text>')
    s.append("</svg>"); return "".join(s)
def spec(items): return "".join(f'<div class="rule" style="padding:1.8mm 0 1.6mm;display:grid;grid-template-columns:27mm 1fr;gap:3mm"><div class="lab" style="color:#141414;font-size:7pt">{e(a)}</div><div class="ps" style="font-size:8.6pt">{e(b)}</div></div>' for a, b in items)
pg(6, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">04 · Requirements</div><div class="t2" style="margin-top:2mm">Symbol and wordmark</div></div>
<div class="abs" style="left:14mm;top:40mm;width:128mm"><div class="lab" style="color:#141414;margin-bottom:1.5mm">Symbol</div>{spec(SYMBOL)}</div>
<div class="abs" style="left:150mm;top:40mm;width:133mm"><div class="lab" style="color:#141414;margin-bottom:1.5mm">Wordmark</div>{spec(WORDMARK)}</div>
<div class="abs" style="left:150mm;top:128mm;width:88mm">{grid_svg()}</div>
""", "Requirements")

# ---------------------------------------------------------- 07 colour
sw = "".join(f'<div style="flex:{f}"><div class="sw" style="background:{h};color:{"#141414" if n in ("Chalk","Lichen") else PAL["chalk"]};{"border:.5pt solid #d6d6d2;" if n=="Chalk" else ""}">{n}<span style="font-family:IBM Plex Mono;font-weight:400;font-size:7pt;margin-top:.6mm">{h}</span></div><p class="ps" style="font-size:8.2pt;margin-top:1.5mm">{e(u)}</p></div>' for (n, h, u), f in zip(SWATCHES, [3, 2, 1.6, 1.3]))
ramp = "".join(f'<div style="flex:1;height:9mm;background:{h};{"border:.5pt solid #d6d6d2;" if h==PAL["chalk"] else ""}"></div>' for h in [PAL['moss'], PAL['sage'], PAL['lichen'], PAL['chalk']])
rows = ""
for a, b, v in C["contrast"]:
    use = "Text (AA)" if v >= 4.5 else ("Large text, graphics" if v >= 3 else "Not for text or marks")
    rows += f'<tr style="border-bottom:.5pt solid #e1e1dd"><td style="padding:1mm 0"><span style="display:inline-block;width:3mm;height:3mm;background:{PAL[a]};vertical-align:-.4mm;outline:.4pt solid #ccc"></span> on <span style="display:inline-block;width:3mm;height:3mm;background:{PAL[b]};vertical-align:-.4mm;outline:.4pt solid #ccc"></span> &nbsp;{a.title()} / {b.title()}</td><td style="text-align:right;font-variant-numeric:tabular-nums">{v}:1</td><td style="padding-left:4mm;color:{"#141414" if v>=3 else PAL["flag"]}">{use}</td></tr>'
pg(7, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">05 · Colour</div><div class="t2" style="margin-top:2mm">The palette is a data ramp</div></div>
<div class="abs" style="left:14mm;top:40mm;width:170mm;display:flex;gap:3mm">{sw}</div>
<div class="abs" style="left:14mm;top:102mm;width:170mm">
 <div class="lab" style="color:#141414">The ramp: low → high, in the logo, the maps and the reports</div>
 <div style="display:flex;margin-top:2mm">{ramp}</div>
 <div style="display:flex" class="ill">{''.join(f'<span style="flex:1;margin-top:1mm">{n} {PAL[n.lower()]}</span>' for n in ["Moss", "Sage", "Lichen", "Chalk"])}</div>
 <div class="lab" style="color:#141414;margin-top:6mm">Rules</div><ul class="d ps" style="margin-top:.5mm">{''.join(f'<li>{e(r)}</li>' for r in COLOUR_RULES)}</ul>
</div>
<div class="abs" style="left:194mm;top:40mm;width:89mm">
 <div class="lab" style="color:#141414">Measured contrast (WCAG)</div>
 <table class="ps" style="width:100%;border-collapse:collapse;margin-top:1.5mm;font-size:8pt">{rows}</table>
 <div style="margin-top:6mm;border-left:1.2mm solid {PAL['flag']};padding-left:4mm"><div class="lab" style="color:#141414">Trend risk</div><p class="ps" style="margin-top:1mm;font-size:8.5pt">{e(LIME_RISK)}</p></div>
 <p class="ill" style="margin-top:5mm;line-height:1.5">Starting hypotheses for testing — HEX and RGB only. No Pantone or CMYK until a print profile is agreed.</p>
</div>
""", "Colour")

# ---------------------------------------------------------- 08 background
tiles = ""
for a, path, c in BG_MODES:
    img = inline_svg(path, 'width:100%;height:100%') if path.endswith('.svg') else f'<img src="{path}" style="width:100%;height:100%;object-fit:cover;display:block">'
    tiles += f'<div style="flex:1"><div style="height:52mm;overflow:hidden;background:{PAL["basalt"]}">{img}</div><div class="t2" style="font-size:10.5pt;margin-top:2.5mm">{a}</div><p class="ps" style="font-size:8.5pt;margin-top:.8mm">{e(c)}</p></div>'
pg(8, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">06 · Background</div><div class="t2" style="margin-top:2mm">Digitised mountains: three render modes, one dataset</div></div>
<div class="abs" style="left:14mm;right:14mm;top:40mm;display:flex;gap:6mm">{tiles}</div>
<div class="abs" style="left:14mm;top:124mm;width:84mm"><div class="lab" style="color:#141414">Data</div><p class="ps" style="margin-top:1mm">{e(BG_DATA)}</p></div>
<div class="abs" style="left:106mm;top:124mm;width:84mm"><div class="lab" style="color:#141414">Rules</div><ul class="d ps" style="margin-top:.5mm">{''.join(f'<li>{e(r)}</li>' for r in BG_RULES)}</ul></div>
<div class="abs" style="left:199mm;top:124mm;width:84mm;border-left:1.2mm solid {PAL['flag']};padding-left:4mm"><div class="lab" style="color:#141414">Avoid</div><p class="ps" style="margin-top:1mm">{e(BG_AVOID)}</p></div>
<div class="abs ill" style="left:14mm;bottom:8mm">All three tiles render the same procedural terrain — illustrative, not real elevation data</div>
""", "Background")

# ---------------------------------------------------------- 09 this round
pg(9, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">07 · This round</div><div class="t2" style="margin-top:2mm">What comes back, and how it's judged</div></div>
<div class="abs" style="left:14mm;top:40mm;width:112mm"><div class="lab" style="color:#141414;margin-bottom:1.5mm">Deliverables</div>{spec(DELIVER)}</div>
<div class="abs" style="left:134mm;top:40mm;width:70mm"><div class="lab" style="color:#141414">How we'll judge it</div><ul class="d ps" style="margin-top:.5mm;font-size:8.6pt">{''.join(f'<li>{e(j)}</li>' for j in JUDGE)}</ul></div>
<div class="abs" style="left:14mm;right:14mm;bottom:14mm;border-top:.75pt solid #141414;padding-top:3mm;display:flex;gap:8mm;align-items:baseline"><span class="lab" style="color:#141414;flex:none">Next</span><span class="p">On approval of this brief, the three symbol studies, two wordmarks, palette and background modes are produced and presented as set out above.</span></div>
<div class="abs" style="left:212mm;top:40mm;width:71mm;background:{PAL['basalt']};color:{PAL['chalk']};padding:5mm"><div class="lab" style="color:{PAL['lichen']}">Open questions</div><ol class="n ps" style="margin-top:.5mm;font-size:8.6pt">{''.join(f'<li>{e(q)}</li>' for q in QUESTIONS)}</ol></div>
""", "This round")

open("brief.html", "w").write(f"<!doctype html><html lang='en'><meta charset='utf-8'><title>HCO — Logo brief v2</title><style>{CSS}</style><body>{''.join(pages)}</body></html>")
print(len(pages), "pages; md", len(md), "lines")
