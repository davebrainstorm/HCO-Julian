"""Top-five concepts, ranked: overview, one page per concept, comparison,
next steps. Reuses the Stage-1 board styles and covers from build_review.py."""
from build_review import CSS, mark, cover_r1, cover_r2, cover_r3, px_block, header, F

CSS5 = CSS + f"""
@font-face{{font-family:'Source Serif 4';src:url('{F}sourceserif4/SourceSerif4[opsz,wght].ttf');font-weight:200 900}}
.rank{{font-family:'Hanken Grotesk';font-weight:600;font-size:9pt;letter-spacing:.04em}}
.thumb{{position:relative;overflow:visible}}
.thumb>.in{{transform-origin:0 0;position:absolute;left:0;top:0}}
"""
TOTAL = 8
pages = []
def pg(n, body, label):
    pages.append((n, f'<section class="page">{header("HCO — Identity exploration · Top five concepts", f"{label} &nbsp;·&nbsp; {n:02d}/{TOTAL:02d}")}{body}</section>'))

def thumb(cover_html, scale=0.45):
    return f'<div class="thumb" style="width:{118*scale:.1f}mm;height:{167*scale:.1f}mm"><div class="in" style="transform:scale({scale})">{cover_html}</div></div>'

SECTIONS = """<div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">01</span>Observations</div>
<div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">02</span>Operational priorities</div>
<div style="display:grid;grid-template-columns:8mm 1fr"><span style="color:#6b6b6b">03</span>Recommended next steps</div>"""

def cover_r4():
    return f"""
<div style="width:118mm;height:167mm;background:#fff;position:relative;box-shadow:0 .4mm 2.4mm rgba(0,0,0,.18);font-family:'Instrument Sans';overflow:hidden">
  <div style="position:absolute;left:9mm;top:9mm">{mark("r4-lockup-black", h=8)}</div>
  <div style="position:absolute;left:9mm;top:34mm;right:9mm;font-size:24pt;font-weight:600;line-height:1.03;letter-spacing:-.012em">Field &amp;<br>Operations<br>Review</div>
  <div style="position:absolute;left:9mm;top:71mm;font-size:6.5pt;font-weight:500">[Property name] · [Month Year]</div>
  <div style="position:absolute;left:54mm;top:103mm;width:32mm;height:32mm;background:#141414"></div>
  <div style="position:absolute;left:86mm;top:135mm;width:32mm;height:32mm;background:#141414"></div>
  <div style="position:absolute;left:9mm;bottom:9mm;width:42mm;font-size:6.5pt;line-height:1.75;font-weight:500">{SECTIONS}</div>
</div>"""

def cover_r5():
    return f"""
<div style="width:118mm;height:167mm;background:#fff;position:relative;box-shadow:0 .4mm 2.4mm rgba(0,0,0,.18);font-family:'Source Serif 4';overflow:hidden">
  <div style="position:absolute;left:9mm;right:0;top:12mm;height:.9mm;background:#141414"></div>
  <div style="position:absolute;left:9mm;top:16.5mm">{mark("r5-name-black", h=8)}</div>
  <div style="position:absolute;left:9mm;top:52mm;right:9mm;font-size:26pt;font-weight:600;font-variation-settings:'opsz' 60;line-height:1.02;letter-spacing:-.01em">Field &amp; Operations Review</div>
  <div style="position:absolute;left:9mm;right:9mm;top:98mm;font-size:7pt;line-height:1.75;font-variation-settings:'opsz' 12">{SECTIONS}</div>
  <div style="position:absolute;left:9mm;bottom:9mm;right:9mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;font-size:6.5pt;line-height:1.35;border-top:.5pt solid #141414;padding-top:2mm;font-variation-settings:'opsz' 12">
    <div><div style="color:#6b6b6b">Prepared for</div>[Client name]</div><div><div style="color:#6b6b6b">Property</div>[Property name]</div><div><div style="color:#6b6b6b">Visit</div>[Month Year]</div></div>
</div>"""

C = [  # rank order
 dict(r="r1", name="High Bar", kind="Custom typographic", line="The horizon, drawn into the H.",
      primary=mark("r1-lockup-black", w=168), over=mark("r1-lockup-black", w=46), reverse=mark("r1-lockup-white", w=54), compact=mark("r1-compact-black", h=22), cover=cover_r1(),
      idea="A custom-drawn HCO in which the crossbar of the H sits high — the horizon as you see it from high ground, with more land in view than sky. That one line becomes the system: layouts hang their content below the same high horizon, and photographs are cropped the same way.",
      weak="The idea lives in a single detail. Without the system around it, some people will simply see a well-drawn HCO, and a crossbar pushed any higher starts to look like a period mannerism.",
      why="Strongest on every test, and the idea lives in the name itself — it cannot be separated from HCO or copied onto someone else's initials."),
 dict(r="r4", name="Ground Truth", kind="Field and observation", line="The map, checked on the ground.",
      primary=mark("r4-lockup-black", w=150), over=mark("r4-lockup-black", w=40), reverse=mark("r4-lockup-white", w=52), compact=mark("r4-symbol-black", h=22), cover=cover_r4(),
      idea="In drone mapping, a two-square target is laid on the ground so the aerial map can be pinned to real positions: the picture from above, checked against the ground. That is HCO's promise in one object. The point where the squares meet marks exact locations in every map, photograph and report.",
      weak="Two squares are simple, common geometry. Repeated, they read as a racing flag, and the reference could imply surveying services HCO does not offer. It has to be owned through disciplined use and never tiled into a pattern.",
      why="The most business-specific symbol and the best performer at 16 px. It ranks below High Bar because the form itself is generic and must be earned through use."),
 dict(r="r2", name="Rise", kind="Land and observation", line="A field boundary from above; rising ground from the side.",
      primary=mark("r2-lockup-black", w=146), over=mark("r2-lockup-black", w=40), reverse=mark("r2-lockup-white", w=54), compact=mark("r2-symbol-black", h=22), cover=cover_r2(),
      idea="One line, read two ways. From above it is a boundary between fields; from the side it is ground rising to high country. The symbol is a change of perspective — the map and the ground, the plan and the section — which is exactly what HCO's work brings together.",
      weak="Abstract geometry is easily misread: at a glance the line can look like a step chart or a stair, and rising-line marks are common in consulting. It needs the two-tone version or real context to read as land.",
      why="The richest idea of the five, but the one most likely to be misread without explanation — a risk for a mark that often appears alone."),
 dict(r="r5", name="Horizon Line", kind="Evolution of the current logo", line="Keep the horizon; lose the mountain.",
      primary=mark("r5-lockup-black", w=160), over=mark("r5-lockup-black", w=46), reverse=mark("r5-lockup-white", w=54), compact=mark("r5-compact-black", h=22), cover=cover_r5(),
      idea="The evolution route. It keeps what the current logo got right — a horizon over the name — and drops what works against it: the stock peak, the gold on black and the fragile type. The single line runs to the edge of every format, because HCO looks past the field to the wider system.",
      weak="A rule over a serif name is a familiar device, so this is the least distinctive of the five, and it keeps the brand close to the current logo's formal, heritage tone.",
      why="The safest step from today's logo — worth having if continuity matters to HCO's existing clients — but High Bar makes the same horizon idea far more ownable."),
 dict(r="r3", name="The Point", kind="Alternative interpretation", line="Every visit ends in a point.",
      primary=mark("r3-wordmark-accent", w=140), over=mark("r3-wordmark-black", w=38), reverse=mark("r3-wordmark-white", w=50), compact=mark("r3-compact-black", h=22), cover=cover_r3(),
      idea="HCO's real product is clarity: after the visit you know what the issue is and what to do next. The identity is plain-spoken — a confident serif name closed by a square point, the same point that marks each observation on a map and ends each recommendation.",
      weak="Full-stop wordmarks are a familiar device, and a square alone is too generic to own. The compact mark is the weakest of the five, and the serif leans further towards editorial than field.",
      why="A strong verbal idea with the weakest mark: it would rely on copy and layout to do the work a logo should."),
]

# ------------------------------------------------------------------ 01 overview
cols = ""
for i, c in enumerate(C, 1):
    cols += f"""
<div style="flex:1;border-top:{'1.5pt' if i == 1 else '.75pt'} solid #141414;padding-top:3mm;display:flex;flex-direction:column">
  <div class="rank">№ {i}{' &nbsp;<span class="tag" style="font-size:6pt;padding:.3mm 1.1mm;vertical-align:.3mm">New</span>' if c['r'] in ('r4', 'r5') else ''}</div>
  <div class="t2" style="margin-top:1.5mm;font-size:14pt">{c['name']}</div>
  <div class="lab" style="margin-top:1mm;font-size:6.8pt">{c['kind']}</div>
  <div style="height:44mm;display:flex;align-items:center">{c['over']}</div>
  <div style="display:flex;gap:2.5mm;align-items:flex-end;height:9mm"><img src="px/{c['r']}-compact-16.png" style="width:16px;height:16px"><img src="px/{c['r']}-compact-32.png" style="width:32px;height:32px"></div>
  <div class="ill" style="margin-top:1mm">Compact · 16 and 32 px actual</div>
  <p class="ps" style="margin-top:4mm">{c['line']}</p>
</div>"""
pg(1, f"""
<div class="abs" style="left:14mm;top:24mm;width:200mm"><div class="lab">Stage 1 · Top five concepts, ranked</div>
<div class="t1" style="margin-top:3mm">Five ways to say “grounded intelligence”.</div>
<p class="p muted" style="margin-top:3mm;width:190mm">The three routes already reviewed, plus the two strongest ideas held back from the first round: <b style="color:#141414">Ground Truth</b> and <b style="color:#141414">Horizon Line</b>. Ranked on relevance, distinctiveness, craft, small-scale performance and system potential. All marks are outlined vector artwork, shown flat in black on white.</p></div>
<div class="abs" style="left:14mm;right:14mm;top:78mm;display:flex;gap:6mm">{cols}</div>
""", "Overview")

# ------------------------------------------------------------------ 02–06 concept pages
for i, c in enumerate(C, 1):
    r = c["r"]
    pg(i + 1, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab"><span class="rank" style="color:#141414">№ {i}</span> &nbsp;·&nbsp; {c['kind']}</div><div class="t1" style="margin-top:2.5mm">{c['name']}</div></div>
<div class="abs" style="left:14mm;top:50mm;width:172mm;height:80mm;display:flex;align-items:center">{c['primary']}</div>
<div class="cell" style="left:14mm;width:66mm;top:142mm;height:54mm"><div class="lab">Reverse</div><div style="margin-top:3mm;background:#141414;height:32mm;display:flex;align-items:center;padding:0 6mm">{c['reverse']}</div></div>
<div class="cell" style="left:86mm;width:34mm;top:142mm;height:54mm"><div class="lab">Compact mark</div><div style="margin-top:3mm;height:32mm;display:flex;align-items:center">{c['compact']}</div></div>
<div class="cell" style="left:126mm;width:60mm;top:142mm;height:54mm"><div class="lab">Screen sizes</div><div style="margin-top:3mm">{px_block(r, 'Signature at 20 px high')}</div></div>
<div class="abs" style="left:198mm;top:24mm;width:85mm">
  <div class="lab">The idea</div><p class="ps" style="margin-top:1.5mm;font-size:9.6pt">{c['idea']}</p>
  <div class="lab" style="margin-top:4mm">Most important weakness</div><p class="ps" style="margin-top:1.5mm">{c['weak']}</p>
  <div class="lab" style="margin-top:4mm">Why № {i}</div><p class="ps" style="margin-top:1.5mm">{c['why']}</p>
</div>
<div class="abs" style="left:198mm;top:{196 - 167*0.45:.1f}mm">{thumb(c['cover'])}</div>
<div class="abs ill" style="left:198mm;top:{196 - 167*0.45 - 4:.1f}mm">Report cover study · illustrative</div>
""", f"№ {i} · {c['name']}")

# ------------------------------------------------------------------ 07 comparison
def dots(n): return "<span style='display:inline-flex;gap:.9mm'>" + "".join(f"<span style='width:2mm;height:2mm;display:inline-block;background:{'#141414' if k < n else '#d6d6d2'}'></span>" for k in range(5)) + "</span>"
ROWS = [
 ("Business relevance", [(4, "Translates the name; plain enough for a truck door or a lender's desk."),
                         (4, "Names the promise exactly; leans to the field half of the work."),
                         (4, "Plan and section; says less about the advisory half."),
                         (3, "Continuity with today; says little new."),
                         (3, "Advisory value; least about land.")]),
 ("Distinctiveness", [(4, "A raised crossbar is rare and ownable without a symbol."),
                      (3, "Specific story, common geometry."),
                      (3, "Steps and rising lines are common forms."),
                      (2, "A rule over a serif name is familiar."),
                      (2, "Full-stop wordmarks are familiar.")]),
 ("Typographic craft", [(4, "Drawn lettering; every join controllable."),
                        (3, "Well-set type beside a symbol."),
                        (3, "Well-set type beside a symbol."),
                        (3, "Sturdy serif, set rather than drawn."),
                        (3, "Handsome serif; point spacing needs care.")]),
 ("Small-scale performance", [(4, "H holds at 16 px; bar legible at 24 px."),
                              (5, "Two solid squares: the clearest at 16 px."),
                              (3, "The line starts to close at 16 px."),
                              (3, "The bar thins to a pixel at 16 px."),
                              (2, "“H.” reads as an initial at 16 px.")]),
 ("System potential", [(5, "One measure organises every format and crop."),
                       (4, "Marks exact points on maps and photos; bold on vehicles."),
                       (4, "Dividing line and paired images; can repeat."),
                       (3, "Flexible line to the edge; little else."),
                       (3, "Useful markers; mostly typographic voice.")]),
]
head = "".join(f"<td class='lab' style='padding-bottom:1.5mm;color:#141414'>№ {i} · {c['name']}</td>" for i, c in enumerate(C, 1))
body = ""
for crit, cells in ROWS:
    body += f"<tr style='border-bottom:.5pt solid #cfcfcb'><td class='lab' style='color:#141414;padding:2.2mm 2mm 2.2mm 0;vertical-align:top;width:31mm'>{crit}</td>"
    for n, note in cells:
        body += f"<td style='padding:2.2mm 3mm 2.2mm 0;vertical-align:top;width:47.6mm'>{dots(n)}<div class='ps' style='font-size:8pt;margin-top:.8mm;line-height:1.35'>{note}</div></td>"
    body += "</tr>"
totals = [sum(cells[k][0] for _, cells in ROWS) for k in range(5)]
body += "<tr><td class='lab' style='color:#141414;padding-top:2.2mm'>Total / 25</td>" + "".join(f"<td style='padding-top:2.2mm;font-weight:600;font-size:11pt'>{t}</td>" for t in totals) + "</tr>"
pg(7, f"""
<div class="abs" style="left:14mm;top:24mm"><div class="lab">Comparison · internal working view</div><div class="t2" style="margin-top:2mm">How the five compare</div></div>
<table class="abs" style="left:14mm;top:40mm;width:269mm;border-collapse:collapse"><tr style="border-bottom:.75pt solid #141414"><td></td>{head}</tr>{body}</table>
<div class="abs ps muted" style="left:14mm;right:14mm;bottom:12mm">Ratings are a designer's judgement from the artwork and the pixel tests on each page, not measured data. A resemblance check against existing identities will be run on the approved concept; it is not trademark clearance.</div>
""", "Comparison")

# ------------------------------------------------------------------ 08 next
pg(8, f"""
<div class="abs" style="left:14mm;top:24mm;width:150mm"><div class="lab">Recommendation</div>
<div class="t1" style="margin-top:3mm">№ 1 High Bar, with type direction A.</div>
<p class="p" style="margin-top:4mm">High Bar is the most distinctive without leaning on a symbol, survives at the smallest sizes, and its one idea generates the most useful system — for the advisory half of the business as much as the field half.</p>
<p class="p" style="margin-top:3mm">If a symbol is wanted as well, <b>Ground Truth</b> is the strongest second choice. It should not be merged with High Bar: each works because it does one thing.</p></div>
<div class="abs" style="left:14mm;right:14mm;top:120mm;bottom:14mm;background:#141414;overflow:hidden">
 <div style="position:absolute;left:12mm;top:{76*0.285 - 150*228/5062:.2f}mm">{mark("r1-lockup-white", w=150)}</div>
 <div style="position:absolute;left:{12+150+7}mm;right:0;top:{76*0.285 - 150*228/5062 + 150*(1012-715)/5062:.2f}mm;border-top:.6pt solid #fff"></div>
 <div class="ill" style="position:absolute;left:12mm;bottom:5mm;color:#9a9a96">The crossbar's height carried to the edge of the format — the high horizon at work</div>
</div>
<div class="abs" style="left:176mm;top:24mm;width:107mm">
 <div class="lab">To move to the identity pack</div>
 <div class="rule" style="padding-top:2.5mm;margin-top:3mm"><div class="lab" style="color:#141414">1 · Choose one concept</div><p class="ps" style="margin-top:1.2mm">It is then locked; only the craft is refined.</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:4mm"><div class="lab" style="color:#141414">2 · Confirm typography</div><p class="ps" style="margin-top:1.2mm">Open-licence direction A (Instrument Sans), or a licensed family with approved access. Your premium fonts cannot be reached from this environment.</p></div>
 <div class="rule" style="padding-top:2.5mm;margin-top:4mm"><div class="lab" style="color:#141414">3 · Confirm the name</div><p class="ps" style="margin-top:1.2mm">“Group” or “Consulting”. Until then: HCO, High Country Observations, and Consulting as an optional descriptor.</p></div>
</div>
""", "Next")

if __name__ == "__main__":
    open("top5-concepts.html", "w").write(f"<!doctype html><html lang='en'><meta charset='utf-8'><title>HCO — Top five concepts</title><style>{CSS5}</style><body>{''.join(h for _, h in sorted(pages))}</body></html>")
    print(len(pages), "pages")
