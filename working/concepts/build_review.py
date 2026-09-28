"""Builds the Stage-1 concept review (exploration boards) as paginated HTML,
then PDF + PNG previews via ../tools/render.mjs. Internal / approval use only."""
import re, os, html

M = "marks/"
def mark(name, h=None, w=None, extra=""):
    s = open(M + name + ".svg").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r'^<svg[^>]*>|</svg>$', '', s)
    size = (f"height:{h}mm;width:auto;" if h else "") + (f"width:{w}mm;height:auto;" if w else "")
    return f'<svg viewBox="{vb}" style="{size}display:block;{extra}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{inner}</svg>'

F = "../fonts-ofl/"
FACES = [
 ("Hanken Grotesk", "hankengrotesk/HankenGrotesk[wght].ttf", "hankengrotesk/HankenGrotesk-Italic[wght].ttf", "100 900"),
 ("Instrument Sans", "instrumentsans/InstrumentSans[wdth,wght].ttf", "instrumentsans/InstrumentSans-Italic[wdth,wght].ttf", "400 700"),
 ("Newsreader", "newsreader/Newsreader[opsz,wght].ttf", "newsreader/Newsreader-Italic[opsz,wght].ttf", "200 800"),
 ("Public Sans", "publicsans/PublicSans[wght].ttf", "publicsans/PublicSans-Italic[wght].ttf", "100 900"),
 ("IBM Plex Sans", "ibmplexsans/IBMPlexSans[wdth,wght].ttf", "ibmplexsans/IBMPlexSans-Italic[wdth,wght].ttf", "100 700"),
]
css_faces = ""
for n, r, i, w in FACES:
    css_faces += f"@font-face{{font-family:'{n}';src:url('{F}{r}');font-weight:{w};font-style:normal}}\n"
    css_faces += f"@font-face{{font-family:'{n}';src:url('{F}{i}');font-weight:{w};font-style:italic}}\n"
for wt, st in [(400, "Regular"), (500, "Medium"), (600, "SemiBold")]:
    css_faces += f"@font-face{{font-family:'IBM Plex Mono';src:url('{F}ibmplexmono/IBMPlexMono-{st}.ttf');font-weight:{wt}}}\n"

CSS = css_faces + r"""
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#d9d9d6}
body{font-family:'Hanken Grotesk';color:#141414;-webkit-font-smoothing:antialiased;font-kerning:normal}
.page{width:297mm;height:210mm;background:#fff;position:relative;overflow:hidden;page-break-after:always;break-after:page}
@media screen{.page{margin:0 auto 8mm;box-shadow:0 1px 6px rgba(0,0,0,.15)}}
.hd{position:absolute;left:14mm;right:14mm;top:9mm;display:flex;justify-content:space-between;font-size:7.5pt;font-weight:500;letter-spacing:.02em;color:#6b6b6b;border-bottom:.5pt solid #cfcfcb;padding-bottom:2.2mm}
.lab{font-size:7.5pt;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:#6b6b6b}
.t1{font-size:25pt;line-height:1.08;font-weight:600;letter-spacing:-.012em}
.t2{font-size:15pt;line-height:1.15;font-weight:600;letter-spacing:-.005em}
.p{font-size:10.5pt;line-height:1.42}
.ps{font-size:9pt;line-height:1.4}
.muted{color:#5e5e5b}
.abs{position:absolute}
.rule{border-top:.5pt solid #cfcfcb}
.pix{image-rendering:pixelated;display:block}
.cell{position:absolute;top:150mm;height:46mm;border-top:.5pt solid #cfcfcb;padding-top:3mm}
.tag{display:inline-block;font-size:7pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border:.5pt solid #9a9a96;border-radius:0;padding:.6mm 1.4mm;color:#555}
.ill{font-size:6pt;letter-spacing:.06em;text-transform:uppercase;color:#8a8a86}
"""

def header(left, right):
    return f'<div class="hd"><span>{left}</span><span>{right}</span></div>'

pages = []
TOTAL = 11
def pg(n, body, label):
    pages.append((n, f'<section class="page">{header("HCO — Identity exploration · Stage 1 · For approval", f"{label} &nbsp;·&nbsp; {n:02d}/{TOTAL:02d}")}{body}</section>'))

# ------------------------------------------------------------------ 01 cover
pg(1, f"""
<div class="abs" style="left:14mm;top:30mm;width:180mm">
  <div class="lab">Working document · 28 September 2026</div>
  <div class="t1" style="font-size:40pt;margin-top:8mm;line-height:1.02">Three routes.<br>Three type directions.<br>One recommendation.</div>
  <p class="p muted" style="margin-top:9mm;width:150mm">Exploration boards for HCO — High Country Observations. They are here to choose a direction, not to finish one. Once a route and a type direction are approved, the chosen identity is refined, built into a system and delivered as the five-page identity pack.</p>
</div>
<div class="abs" style="left:14mm;bottom:14mm;right:14mm;display:flex;gap:10mm" >
  <div style="flex:1" class="rule"><div class="lab" style="margin-top:2.5mm">01–02</div><div class="ps" style="margin-top:1mm">What we heard</div></div>
  <div style="flex:1" class="rule"><div class="lab" style="margin-top:2.5mm">03–08</div><div class="ps" style="margin-top:1mm">Routes 1, 2 and 3</div></div>
  <div style="flex:1" class="rule"><div class="lab" style="margin-top:2.5mm">09</div><div class="ps" style="margin-top:1mm">Typography directions</div></div>
  <div style="flex:1" class="rule"><div class="lab" style="margin-top:2.5mm">10–11</div><div class="ps" style="margin-top:1mm">Recommendation and decisions</div></div>
</div>
""", "Cover")

# ------------------------------------------------------------------ 02 what we heard
pg(2, f"""
<div class="abs" style="left:14mm;top:24mm;width:120mm"><div class="lab">What we heard</div>
<div class="t1" style="margin-top:4mm">A practical business that shows up, learns the operation and says what to do next.</div></div>
<div class="abs" style="left:14mm;top:66mm;width:84mm">
 <div class="lab">The work</div>
 <p class="ps" style="margin-top:2mm"><b>Business &amp; operations</b> — regulatory and compliance research, business decisions, contracts and vendors, markets and supply chains.</p>
 <p class="ps" style="margin-top:2.5mm"><b>Field &amp; property intelligence</b> — drone mapping, crop-health observations, farm and ranch mapping, repeat monitoring and clear practical reports.</p>
 <p class="ps" style="margin-top:2.5mm">For farmers, ranchers and agricultural business owners and operators. It has to feel straightforward to an owner-operator and credible in front of a larger organisation.</p>
</div>
<div class="abs" style="left:106.5mm;top:66mm;width:84mm">
 <div class="lab">The territory · Grounded intelligence</div>
 <p class="ps" style="margin-top:2mm">The relationship between seeing the wider system and understanding what is happening on the ground. HCO turns observation into useful judgement and practical next steps. Technology supports that promise; it is not the business.</p>
 <div style="margin-top:4mm;display:flex;flex-wrap:wrap;gap:1.6mm"><span class="tag">Grounded</span><span class="tag">Clear-sighted</span><span class="tag">Capable</span><span class="tag">Independent</span><span class="tag">Direct</span></div>
 <p class="ps muted" style="margin-top:4mm">Internal territory only — not a public tagline.</p>
</div>
<div class="abs" style="left:199mm;top:66mm;width:84mm">
 <div class="lab">What the current material tells us</div>
 <p class="ps" style="margin-top:2mm">A peak above initials is the category's most common mark, and gold on black reads as luxury or outdoor gear rather than advice.</p>
 <p class="ps" style="margin-top:2.5mm">The flyer's content is strong. Its presentation — generated photography, distressed type, icon sets — undersells it.</p>
 <p class="ps" style="margin-top:2.5mm">Worth keeping: the plain, practical voice, and “Understand systems. Protect people.” as an optional line, not fixed to the logo.</p>
</div>
<div class="abs" style="left:14mm;right:14mm;bottom:14mm;padding-top:3mm" >
 <div class="rule" style="padding-top:3mm;display:flex;gap:8mm;align-items:baseline"><span class="lab" style="flex:none">Naming — to confirm</span>
 <span class="ps">The existing logo reads “High Country Observations <b>Group</b>”; the flyer uses “…Observations <b>Consulting</b>” and “HCO Consulting”. These boards use <b>HCO</b> as the principal identifier, <b>High Country Observations</b> as the expanded name, and <b>Consulting</b> as an optional descriptor.</span></div>
</div>
""", "Context")

# ------------------------------------------------------------------ route mark pages
def px_block(r, word_note):
    return f"""
<div style="display:flex;gap:4mm;align-items:flex-end">
  <div><img class="pix" src="px/{r}-compact-16-x6.png" style="width:17mm;height:17mm;border:.4pt solid #e2e2df"><div class="ill" style="margin-top:1mm">16 px ×6</div></div>
  <div style="display:flex;gap:2.5mm;align-items:flex-end;padding-bottom:4.3mm">
    <img src="px/{r}-compact-16.png" style="width:16px;height:16px"><img src="px/{r}-compact-24.png" style="width:24px;height:24px"><img src="px/{r}-compact-32.png" style="width:32px;height:32px">
  </div>
</div>
<div class="ill" style="margin-top:1mm">Actual 16 · 24 · 32 px</div>
<img src="px/{r}-word-20.png" style="height:20px;margin-top:3mm;display:block"><div class="ill" style="margin-top:1mm">{word_note}</div>"""

def route_marks(n, num, name, kind, idea, weak, primary, compact, reverse, lock_black_small, compact_small, r):
    pg(n, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Route {num} · {kind}</div><div class="t1" style="margin-top:2.5mm">{name}</div></div>
<div class="abs" style="left:14mm;top:52mm;width:178mm;height:88mm;display:flex;align-items:center;justify-content:flex-start">{primary}</div>
<div class="abs" style="left:204mm;top:24mm;width:79mm">
  <div class="lab">The idea</div><p class="p" style="margin-top:2mm">{idea}</p>
  <div class="lab" style="margin-top:6mm">Most important weakness</div><p class="ps" style="margin-top:2mm">{weak}</p>
</div>
<div class="cell" style="left:14mm;width:84mm"><div class="lab">Reverse</div><div style="margin-top:3mm;background:#141414;height:31mm;display:flex;align-items:center;padding:0 7mm">{reverse}</div></div>
<div class="cell" style="left:104mm;width:42mm"><div class="lab">Compact mark</div><div style="margin-top:3mm;height:31mm;display:flex;align-items:center">{compact}</div></div>
<div class="cell" style="left:152mm;width:62mm"><div class="lab">Screen sizes</div><div style="margin-top:3mm">{px_block(r, 'Signature at 20 px high')}</div></div>
<div class="cell" style="left:220mm;width:63mm"><div class="lab">Print sizes (actual)</div>
  <div style="margin-top:3mm">{lock_black_small}</div><div class="ill" style="margin-top:1.2mm">Signature at 30 mm wide</div>
  <div style="margin-top:3mm;display:flex;gap:4mm;align-items:flex-end">{compact_small}</div><div class="ill" style="margin-top:1.2mm">Compact mark at 8 mm and 5 mm high</div></div>
""", f"Route {num}")

route_marks(3, 1, "High Bar", "Custom typographic",
 "A custom-drawn HCO in which the crossbar of the H sits high — the horizon as you see it from high ground, with more land in view than sky. That one line becomes the system: layouts hang their content below the same high horizon, and photographs are cropped the same way.",
 "The idea lives in a single detail. Without the system around it, some people will simply see a well-drawn HCO, and a crossbar pushed any higher starts to look like a period mannerism.",
 mark("r1-lockup-black", w=176), mark("r1-compact-black", h=24), mark("r1-lockup-white", w=70),
 mark("r1-lockup-black", w=30), mark("r1-compact-black", h=8) + mark("r1-compact-black", h=5), "r1")

route_marks(5, 2, "Rise", "Land and observation",
 "One line, read two ways. From above it is a boundary between fields; from the side it is ground rising to high country. The symbol is a change of perspective — the map and the ground, the plan and the section — which is exactly what HCO's work brings together.",
 "Abstract geometry is easily misread: at a glance the line can look like a step chart or a stair, and rising-line marks are common in consulting. It needs the two-tone version or real context to read as land.",
 mark("r2-lockup-black", w=150), mark("r2-symbol-black", h=24), mark("r2-lockup-white", w=66),
 mark("r2-lockup-black", w=30), mark("r2-symbol-black", h=8) + mark("r2-symbol-black", h=5), "r2")

route_marks(7, 3, "The Point", "Alternative interpretation",
 "HCO's real product is clarity: after the visit you know what the issue is and what to do next. The identity is plain-spoken — a confident serif name closed by a square point, the same point that marks each observation on a map and ends each recommendation.",
 "Full-stop wordmarks are a familiar device, and a square alone is too generic to own. The compact mark is the weakest of the three, and the serif leans further towards editorial than field.",
 mark("r3-wordmark-accent", w=150), mark("r3-compact-black", h=24), mark("r3-wordmark-white", w=58),
 mark("r3-wordmark-black", w=30), mark("r3-compact-black", h=8) + mark("r3-compact-black", h=5), "r3")

# ------------------------------------------------------------------ route system pages
SPEC_COPY = {
 "head": "Field &amp; Operations Review",
 "sub": "Operational priorities",
 "para": "We show up, learn the operation, identify the issue, and give you practical options for what to do next. Each observation is tied to a location, a date and a recommended next step.",
}
def spec(fam_head, fam_body, fam_label, head_w, body_w, label_css, numstyle, note, head_extra="", italic_line=""):
    return f"""
<div class="lab">Type direction</div><div class="ps" style="margin-top:1.5mm">{note}</div>
<div style="margin-top:5mm;font-family:{fam_head};font-weight:{head_w};font-size:25pt;line-height:1.05;letter-spacing:-.012em;{head_extra}">{SPEC_COPY['head']}</div>
<div style="margin-top:4mm;font-family:{fam_head};font-weight:{head_w};font-size:13pt;line-height:1.2">{SPEC_COPY['sub']}</div>
<p style="margin-top:2mm;font-family:{fam_body};font-weight:{body_w};font-size:10.5pt;line-height:1.45">{SPEC_COPY['para']} {italic_line}</p>
<div style="margin-top:5mm;border-top:.75pt solid #141414;padding-top:2mm;font-family:{fam_label};{label_css}">
 <div style="display:flex;justify-content:space-between;{numstyle}"><span>Observation 03 · North block</span><span>Priority 1</span></div>
</div>
<table style="margin-top:3mm;width:100%;border-collapse:collapse;font-family:{fam_body};font-size:9.5pt;{numstyle}">
 <tr style="border-bottom:.5pt solid #cfcfcb"><td style="padding:1.3mm 0">Area mapped</td><td style="text-align:right">148.6 ha</td></tr>
 <tr style="border-bottom:.5pt solid #cfcfcb"><td style="padding:1.3mm 0">Mean NDVI, this visit</td><td style="text-align:right">0.72</td></tr>
 <tr style="border-bottom:.5pt solid #cfcfcb"><td style="padding:1.3mm 0">Change since last visit</td><td style="text-align:right">−0.06</td></tr>
 <tr><td style="padding:1.3mm 0">Priority areas identified</td><td style="text-align:right">3</td></tr>
</table>
<div class="ill" style="margin-top:1.5mm">Illustrative figures — not project data</div>"""

def cover_r1():
    return f"""
<div style="width:118mm;height:167mm;background:#fff;position:relative;box-shadow:0 .4mm 2.4mm rgba(0,0,0,.18);font-family:'Instrument Sans'">
  <div style="position:absolute;left:9mm;top:9mm">{mark("r1-wordmark-black", h=7.2)}</div>
  <div style="position:absolute;right:9mm;top:9mm;font-size:6.5pt;font-weight:500;text-align:right;line-height:1.35">Field &amp; property<br>intelligence</div>
  <div style="position:absolute;left:0;right:0;top:47.6mm;border-top:.75pt solid #141414"></div>
  <div style="position:absolute;left:9mm;top:37mm;font-size:6.5pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase">Assessment report</div>
  <div style="position:absolute;left:9mm;top:53mm;right:9mm;font-size:25pt;font-weight:600;line-height:1.02;letter-spacing:-.015em">Field &amp;<br>Operations<br>Review</div>
  <div style="position:absolute;left:9mm;right:9mm;top:104mm;font-size:7pt;line-height:1.75;font-weight:500">
    <div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">01</span>Observations</div>
    <div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">02</span>Operational priorities</div>
    <div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">03</span>Recommended next steps</div></div>
  <div style="position:absolute;left:9mm;bottom:9mm;right:9mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;font-size:6.5pt;line-height:1.35;border-top:.5pt solid #141414;padding-top:2mm">
    <div><div style="color:#6b6b6b">Prepared for</div>[Client name]</div><div><div style="color:#6b6b6b">Property</div>[Property name]</div><div><div style="color:#6b6b6b">Visit</div>[Month Year]</div>
  </div>
</div>"""

def cover_r2():
    return f"""
<div style="width:118mm;height:167mm;background:#fff;position:relative;box-shadow:0 .4mm 2.4mm rgba(0,0,0,.18);font-family:'IBM Plex Sans';overflow:hidden">
  <svg viewBox="0 0 1180 1670" style="position:absolute;inset:0;width:100%;height:100%" preserveAspectRatio="none">
    <path d="M0 1120 L470 1120 L700 790 L1180 790 L1180 1670 L0 1670Z" fill="#1c1f1d"/>
    <path d="M700 790 L1180 790 L1180 1670 L0 1670 L0 1120 L470 1120Z" fill="none"/>
  </svg>
  <div style="position:absolute;left:9mm;top:9mm">{mark("r2-lockup-black", h=8)}</div>
  <div style="position:absolute;left:9mm;top:34mm;right:9mm;font-size:23pt;font-weight:600;line-height:1.04;letter-spacing:-.01em">Field &amp;<br>Operations<br>Review</div>
  <div style="position:absolute;left:9mm;top:70mm;font-family:'IBM Plex Mono';font-size:6.5pt;letter-spacing:.02em">[Property name] · [Month Year]</div>
  <div style="position:absolute;left:9mm;bottom:9mm;right:9mm;color:#fff;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;font-family:'IBM Plex Mono';font-size:6pt;line-height:1.4;border-top:.5pt solid #7c847b;padding-top:2mm">
    <div>01<br>Observations</div><div>02<br>Operational priorities</div><div>03<br>Recommended next steps</div>
  </div>
</div>"""

def cover_r3():
    sq = '<span style="display:inline-block;width:1.6mm;height:1.6mm;background:#E4502A;margin-right:2mm;vertical-align:.1mm"></span>'
    return f"""
<div style="width:118mm;height:167mm;background:#fff;position:relative;box-shadow:0 .4mm 2.4mm rgba(0,0,0,.18);font-family:'Public Sans'">
  <div style="position:absolute;left:9mm;top:9mm">{mark("r3-wordmark-accent", h=7)}</div>
  <div style="position:absolute;left:9mm;top:42mm;right:9mm;font-family:Newsreader;font-variation-settings:'opsz' 72;font-size:27pt;font-weight:500;line-height:1.02;letter-spacing:-.01em">Field &amp; Operations Review<span style="display:inline-block;width:2.6mm;height:2.6mm;background:#E4502A;margin-left:1mm"></span></div>
  <div style="position:absolute;left:9mm;right:9mm;top:92mm;font-size:7pt;line-height:1.9;border-top:.5pt solid #141414;padding-top:2mm">
   <div>{sq}01 &nbsp;Observations</div><div>{sq}02 &nbsp;Operational priorities</div><div>{sq}03 &nbsp;Recommended next steps</div></div>
  <div style="position:absolute;left:9mm;bottom:9mm;right:9mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;font-size:6.5pt;line-height:1.35;color:#141414">
    <div><div style="color:#6b6b6b">Prepared for</div>[Client name]</div><div><div style="color:#6b6b6b">Property</div>[Property name]</div><div><div style="color:#6b6b6b">Visit</div>[Month Year]</div>
  </div>
</div>"""

def route_system(n, num, name, cover, specimen, device_title, device_text):
    pg(n, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Route {num} · {name}</div><div class="t2" style="margin-top:2mm">In use</div></div>
<div class="abs" style="left:14mm;top:36mm">{cover}<div class="ill" style="margin-top:2mm">Report cover study · placeholders in brackets · restrained, flat, no photography</div></div>
<div class="abs" style="left:146mm;top:36mm;width:66mm">{specimen}</div>
<div class="abs" style="left:222mm;top:36mm;width:61mm"><div class="lab">Graphic language</div><div class="t2" style="margin-top:2mm;font-size:12.5pt">{device_title}</div><p class="ps" style="margin-top:2mm">{device_text}</p></div>
""", f"Route {num}")

route_system(4, 1, "High Bar", cover_r1(),
 spec("'Instrument Sans'", "'Instrument Sans'", "'Instrument Sans'", 600, 400,
      "font-size:7.5pt;font-weight:600;letter-spacing:.05em;text-transform:uppercase",
      "font-variant-numeric:tabular-nums lining-nums",
      "A — Clear authority · Instrument Sans (one family)", italic_line="<i>Recommended next steps</i> close every section."),
 "The high horizon",
 "A single rule set at the crossbar's height — 28.5% down from the top of any format. Context sits above it (who, where, when); the ground sits below (observations, priorities, next steps). Photography follows the same rule: a high horizon, more ground than sky.")

route_system(6, 2, "Rise", cover_r2(),
 spec("'IBM Plex Sans'", "'IBM Plex Sans'", "'IBM Plex Mono'", 600, 400,
      "font-size:7pt;font-weight:500;letter-spacing:.02em;text-transform:uppercase",
      "font-variant-numeric:tabular-nums",
      "C — Field precision · IBM Plex Sans + IBM Plex Mono"),
 "The dividing line",
 "The rise line divides formats into two fields — the plan above, the ground below — and pairs images the same way: an aerial view with a view from the ground. On maps the same line weight marks boundaries and change between visits.")

route_system(8, 3, "The Point", cover_r3(),
 spec("Newsreader", "'Public Sans'", "'Public Sans'", 500, 400,
      "font-size:7.5pt;font-weight:600;letter-spacing:.05em;text-transform:uppercase",
      "font-variant-numeric:tabular-nums lining-nums",
      "B — Editorial judgement · Newsreader + Public Sans", head_extra="font-variation-settings:'opsz' 72;"),
 "The square point",
 "One small square does three jobs: it closes the name, it marks each observation location on a map, and it flags each recommended next step. Reserved for things that need attention — never decoration.")

# ------------------------------------------------------------------ 09 typography comparison
def tcol(code, title, fams, head_f, head_w, body_f, label_f, label_css, stand_in, extra_head="", hco_f=None, hco_w=None):
    hco_f = hco_f or head_f; hco_w = hco_w or head_w
    return f"""
<div style="flex:1;border-top:.75pt solid #141414;padding-top:3mm">
 <div class="lab" style="color:#141414">{code} — {title}</div>
 <div class="ps muted" style="margin-top:1mm;height:9mm">{fams}</div>
 <div style="font-family:{hco_f};font-weight:{hco_w};font-size:38pt;line-height:1;margin-top:3mm;{extra_head}">HCO</div>
 <div style="font-family:{head_f};font-weight:{head_w};font-size:19pt;line-height:1.06;letter-spacing:-.01em;margin-top:4mm;height:17mm;{extra_head}">Field &amp; Operations Review</div>
 <div style="font-family:{head_f};font-weight:{head_w};font-size:11pt;margin-top:2mm;{extra_head}">Operational priorities</div>
 <p style="font-family:{body_f};font-size:9.5pt;line-height:1.45;margin-top:1.5mm;height:24mm">We show up, learn the operation, identify the issue, and give you practical options for what to do next. <i>Understand systems. Protect people.</i></p>
 <div style="font-family:{label_f};{label_css};margin-top:3mm;display:flex;justify-content:space-between;border-bottom:.5pt solid #cfcfcb;padding-bottom:1.2mm"><span>Field observations</span><span>Recommended next steps</span></div>
 <div style="font-family:{body_f};font-size:9.5pt;margin-top:1.5mm;font-variant-numeric:tabular-nums lining-nums;display:grid;grid-template-columns:1fr auto;row-gap:.8mm;line-height:1.35">
   <span>Area mapped</span><span>148.6 ha</span><span>Change since last visit</span><span>−0.06</span><span>Figures</span><span>0123456789</span></div>
 <div class="ill" style="margin-top:3mm;line-height:1.5">In place of: {stand_in}</div>
</div>"""
pg(9, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Typography · identical content, three directions</div><div class="t2" style="margin-top:2mm">Choose a voice, not a font</div></div>
<div class="abs" style="left:14mm;right:14mm;top:42mm;display:flex;gap:9mm">
 {tcol("A", "Clear authority", "Instrument Sans · Regular, Italic, Medium, SemiBold, condensed widths — one family", "'Instrument Sans'", 600, "'Instrument Sans'", "'Instrument Sans'", "font-size:7pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase", "Söhne, Neue Haas Grotesk, GT America (not reachable here)", hco_w=700)}
 {tcol("B", "Editorial judgement", "Newsreader (display + text) · Public Sans (labels, data)", "Newsreader", 500, "Newsreader", "'Public Sans'", "font-size:7pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase", "Tiempos or Suisse Works with Graphik or Söhne", extra_head="font-variation-settings:'opsz' 72;")}
 {tcol("C", "Field precision", "IBM Plex Sans · IBM Plex Mono (labels, data)", "'IBM Plex Sans'", 600, "'IBM Plex Sans'", "'IBM Plex Mono'", "font-size:7pt;font-weight:500;letter-spacing:.02em;text-transform:uppercase", "selected on merit from the open inventory")}
</div>
<div class="abs ps muted" style="left:14mm;right:14mm;bottom:12mm">All three use open-licence (SIL OFL) families verified to render in this environment; your licensed premium families could not be reached. Real italics and tabular lining figures throughout; no synthetic bold or stretched type.</div>
""", "Typography")

# ------------------------------------------------------------------ 10 evaluation
def dots(n): return "<span style='display:inline-flex;gap:1mm'>" + "".join(f"<span style='width:2.2mm;height:2.2mm;display:inline-block;background:{'#141414' if i < n else '#d6d6d2'}'></span>" for i in range(5)) + "</span>"
ROWS = [
 ("Business relevance", [(4, "A direct translation of the name; plain enough for a truck door or a lender's desk."),
                          (4, "Closest to the field work — plan and section; says less about the advisory half."),
                          (3, "Captures the advisory value; says least about land and the field.")]),
 ("Distinctiveness", [(4, "A raised crossbar is rare in the category and ownable without a symbol."),
                      (3, "Clean, but steps and rising lines are common forms."),
                      (2, "Full-stop names and serif wordmarks are familiar.")]),
 ("Typographic craft", [(4, "Drawn lettering gives control of every join and space; needs a refinement pass."),
                        (3, "A well-set typeface rather than drawn lettering."),
                        (3, "Handsome serif; point spacing needs care; not custom.")]),
 ("Small-scale performance", [(4, "The H holds at 16 px; the raised bar is still legible at 24 px."),
                              (3, "Holds at 24 px; at 16 px the line starts to close — needs a small-size cut."),
                              (2, "“H.” reads as an initial; at 16 px the point is a pixel or two.")]),
 ("Potential for a wider system", [(5, "One measure organises reports, vehicles, web and photography."),
                                   (4, "Strong for maps and paired images; risk of repetitive dividers."),
                                   (3, "Useful markers in maps and lists; the rest is typographic voice.")]),
]
rows_html = ""
for crit, cells in ROWS:
    rows_html += f"<tr><td class='lab' style='color:#141414;padding:2.4mm 3mm 2.4mm 0;vertical-align:top;width:40mm'>{crit}</td>"
    for n, note in cells:
        rows_html += f"<td style='padding:2.4mm 4mm 2.4mm 0;vertical-align:top'>{dots(n)}<div class='ps' style='font-size:8.5pt;margin-top:.8mm'>{note}</div></td>"
    rows_html += "</tr>"
pg(10, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Evaluation · internal working view</div><div class="t2" style="margin-top:2mm">How the routes compare</div></div>
<table class="abs" style="left:14mm;top:40mm;width:269mm;border-collapse:collapse">
 <tr style="border-bottom:.75pt solid #141414"><td></td><td class="lab" style="padding-bottom:1.5mm;color:#141414">Route 1 · High Bar</td><td class="lab" style="padding-bottom:1.5mm;color:#141414">Route 2 · Rise</td><td class="lab" style="padding-bottom:1.5mm;color:#141414">Route 3 · The Point</td></tr>
 {rows_html.replace("<tr>", "<tr style='border-bottom:.5pt solid #cfcfcb'>")}
</table>
<div class="abs" style="left:14mm;right:14mm;bottom:13mm;background:#141414;color:#fff;padding:5mm 6mm;display:flex;gap:8mm;align-items:flex-start">
 <div style="flex:none;width:52mm"><div class="lab" style="color:#bdbdb8">Recommendation</div><div class="t2" style="margin-top:1.5mm;color:#fff">Route 1 — High Bar,<br>with type direction A</div></div>
 <p class="ps" style="color:#fff;flex:1">It is the most distinctive without leaning on a symbol, it survives at the smallest sizes, and its one idea generates the most useful system — for the advisory half of the business as much as the field half. The weakness is addressed in refinement: draw the letters properly (overshoots, C aperture, spacing), keep the crossbar at 71.5% and no higher, and make the high horizon a working rule in every layout so the detail has a reason to be noticed.</p>
</div>
""", "Evaluation")

# ------------------------------------------------------------------ 11 decisions
pg(11, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Decisions needed</div><div class="t2" style="margin-top:2mm">Before the identity pack is built</div></div>
<div class="abs" style="left:14mm;top:42mm;width:128mm">
 <div class="rule" style="padding-top:2.5mm"><div class="lab" style="color:#141414">1 · Route</div><p class="ps" style="margin-top:1.5mm">Approve Route 1 (recommended), choose Route 2 or 3, or redirect. Routes will not be merged; once one is approved its mark and idea are locked and only the craft is refined.</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:5mm"><div class="lab" style="color:#141414">2 · Typography</div><p class="ps" style="margin-top:1.5mm">Approve direction A (recommended), B or C — and decide how the final type will be licensed (right).</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:5mm"><div class="lab" style="color:#141414">3 · Naming</div><p class="ps" style="margin-top:1.5mm">Confirm “Group” or “Consulting”. Until then: HCO, High Country Observations, and Consulting as an optional descriptor.</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:5mm"><div class="lab" style="color:#141414">4 · Contact details</div><p class="ps" style="margin-top:1.5mm">The phone number and the email address on the flyer are not used anywhere in this work. The address is on a default Microsoft domain; a branded domain is worth setting up before release.</p></div>
</div>
<div class="abs" style="left:155mm;top:42mm;width:128mm">
 <div class="rule" style="padding-top:2.5mm"><div class="lab" style="color:#141414">Font access · what was found</div>
 <p class="ps" style="margin-top:1.5mm">This work runs in a remote Linux environment, not on your computer, so your installed fonts are not visible to it. None of Söhne, GT America, Graphik, Neue Haas Grotesk, Suisse Int'l or Works, Founders Grotesk or Tiempos is available here. Neue Haas Grotesk appears in the connected Adobe Fonts library, but Adobe's font servers are blocked by this environment's network policy, so it cannot be rendered or checked here.</p>
 <p class="ps" style="margin-top:2.5mm">The directions shown use open-licence families that were verified to render here.</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:5mm"><div class="lab" style="color:#141414">Two ways forward</div>
 <p class="ps" style="margin-top:1.5mm"><b>a · Approve the open-licence type.</b> It can be embedded in PDFs, used on a website and installed on HCO's own computers at no cost — the simplest handover.</p>
 <p class="ps" style="margin-top:2mm"><b>b · Use a licensed family.</b> Name it and provide approved access — for example, run the documented build on your own machine where it is installed. The client would need its own licence for web and office use; desktop availability does not grant that.</p></div>
</div>
""", "Decisions")

# ------------------------------------------------------------------ write
open("concept-review.html", "w").write(f"<!doctype html><html lang='en'><meta charset='utf-8'><title>HCO — Identity exploration</title><style>{CSS}</style><body>{''.join(h for _, h in sorted(pages))}</body></html>")
print(len(pages), "pages")
