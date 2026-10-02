"""Pages: overview, principles, brand."""
from site_base import *
from palette import E, BASALT, CHALK, LICHEN, FLAG, MOSS, SAGE

def stat(n, label, sub=""):
    return f'<div class="ds-home__stat"><span class="gw-px" data-px="{n}" style="height:40px"></span><span class="gw-label">{e(label)}</span>{f"<span class=ds-home__sub>{e(sub)}</span>" if sub else ""}</div>'

def overview(counts):
    hero = (f'<canvas data-ridges data-b0=".34" data-amp=".44" class="ds-home__canvas" aria-hidden="true"></canvas>'
            f'<div class="ds-home__actions"><a class="gw-btn gw-btn--primary gw-btn--l" href="principles.html">Start with the principles {ic("arrow-right", "gw-btn__arrow")}</a>'
            f'<a class="gw-btn gw-btn--secondary gw-btn--l" href="tokens.html">{ic("download")}Download tokens</a></div>'
            f'<div class="ds-home__stats">{stat(counts["tokens"], "Tokens")}{stat(counts["icons"], "Pixel icons")}{stat(counts["components"], "Component families")}{stat(5, "Templates")}</div>')
    prim = f'''<div class="ds-prims">
      <div class="ds-prim"><div class="ds-prim__fig"><i class="ds-cell"></i></div><div class="gw-label">01 · Sample</div><h3>The unit of everything</h3>
        <p>One square cell: a symbol sample, a letter stroke, an 8 px step of space. Charts are counted in samples, progress fills in samples, the active page is marked by one.</p></div>
      <div class="ds-prim"><div class="ds-prim__fig">{trace(u=10, style="width:200px;color:var(--hco-signal)")}</div><div class="gw-label">02 · Slope</div><h3>The only angle is 45°</h3>
        <p>Change between samples is drawn at 45°: stairs at small sizes, a straight slope at large sizes. No curves anywhere; even circles become octagons, like the O in HCO.</p></div>
      <div class="ds-prim"><div class="ds-prim__fig"><span class="gw-marker gw-marker--l"><span data-px="03"></span></span></div><div class="gw-label">03 · Flag</div><h3>One colour, one job</h3>
        <p>Flag marks an observation and nothing else. The same numbered marker appears on the map, in the report and on the stake in the field.</p></div></div>'''
    tiles = [("brand.html", "Brand", "Signature, construction, the trace and imagery.", f'{logo(28)}'),
             ("colour.html", "Colour", "Basalt ground, colour as signal, data ramps tested for colour blindness.", '<div class="ds-ramp ds-ramp--s" style="--n:9;width:100%">' + "".join(f'<div style="background:{c}"></div>' for c in T["vigour"]) + "</div>"),
             ("typography.html", "Typography", "Instrument Sans for reading; pixel figures for numbers that matter.", f'<span style="font-weight:600;font-size:64px;line-height:64px;letter-spacing:-.04em">Aa</span><span class="gw-px" data-px="24" style="height:48px;margin-left:16px;color:var(--hco-signal)"></span>'),
             ("components.html", "Components", "Buttons to dialogs, square-cornered and built on one pen.", f'<span class="gw-btn gw-btn--primary">Start {ic("arrow-right")}</span><span class="gw-switch" aria-checked="true" style="margin-left:16px"><span class="gw-switch__track"></span></span>'),
             ("data.html", "Maps and charts", "Interactive field map, legends, cell charts and profiles.", '<div class="ds-mini-map" data-fieldmap data-pins="off"></div>'),
             ("portal.html", "Templates", "Client portal, field report, field app, website and email.", f'<div style="display:flex;gap:8px">' + "".join(f'<span class="gw-marker gw-marker--s"><span data-px="0{i}"></span></span>' for i in range(1, 5)) + "</div>")]
    tl = "".join(f'<a class="ds-tile" href="{u}"><span class="ds-tile__go">{ic("arrow-right")}</span><div class="ds-tile__fig">{fig}</div><h3>{t}</h3><p>{d}</p></a>' for u, t, d, fig in tiles)
    rel = table(["Area", "State in v0.1", "Next"], [
        ["Foundations", '<span class="gw-tag gw-tag--positive">Ready for review</span>', "Approve palette, type and spacing"],
        ["Components", '<span class="gw-tag gw-tag--positive">Ready for review</span>', "Developer handover with tokens"],
        ["Data and maps", '<span class="gw-tag gw-tag--caution">Illustrative data</span>', "Replace with licensed elevation and real flight outputs"],
        ["Typeface", '<span class="gw-tag gw-tag--caution">Decision needed</span>', "Instrument Sans (open licence) or a licensed alternative"],
        ["Trading name", '<span class="gw-tag gw-tag--caution">Decision needed</span>', "“Group” or “Consulting”; descriptor stays as High Country Observations"],
        ["Name and mark check", '<span class="gw-tag gw-tag--critical">Not started</span>', "Clearance by a qualified trademark adviser"],
        ["System name", '<span class="gw-tag">Working name</span>', "“Groundwork” is a working name for the design system; rename freely"]])
    secs = [("what", "What Groundwork is", (
        "Groundwork turns the HCO identity into a working kit: the tokens, components, data styles and templates behind every map, report, screen and sign HCO makes.",
        f'''<div class="ds-grid">{"".join(f'<div class="ds-col"><div class="gw-label" style="color:var(--hco-text-subtle)">{n}</div><h3 style="margin:12px 0 8px">{t}</h3><p class="ds-p">{d}</p></div>' for n, t, d in (
            ("Foundations", "Measured, then drawn", "Colour, type, space and motion as tokens, every value computed and checked rather than picked by eye."),
            ("Data", "Built for observations", "Map layers, legends and charts for drone imagery and field notes, with rules that keep evidence honest."),
            ("Components and templates", "Ready to build", "Square-cornered components and five full templates, written in plain HTML and CSS with no framework required.")))}</div>''')),
        ("primitives", "Three primitives", ("Everything in the system is built from three shapes taken from the symbol.", prim)),
        ("explore", "Explore the system", f'<div class="ds-tiles">{tl}</div>'),
        ("release", "This release", ("Version 0.1 is a working draft for review. These items are open; nothing here is final until they are settled.", rel))]
    return page("index.html", "Groundwork", "The HCO design system: one module, one pen and one set of rules for every map, report, screen and sign.", "01", "Overview", secs,
                hero_extra=hero, hero_cls="ds-hero--home", show_trace=False, extra_js=("assets/data/ridges.js", "assets/js/ridges.js", "assets/data/field.js", "assets/js/fieldmap.js"),
                desc="Groundwork, the HCO design system: tokens, components, data styles and templates.")

def principles():
    P = [("Observe before you design", "Start from what was measured. A layout, a chart or a colour choice should follow the data, not decorate it.",
          ["Show the reading, then the interpretation.", "Cells stay cells: never blur or smooth measured data to make it prettier.", "If a number is estimated, say so next to the number."]),
         ("Plain over clever", "HCO’s clients are busy. Every screen and page should be understood at a glance, outdoors, on a phone.",
          ["One idea per screen; one action per card.", "Sentence case, short words, no jargon without a gloss.", "Write the next step, not just the finding."]),
         ("Colour is data", "Colour reports elevation, vigour or status. It is never used for decoration, and it is never the only signal.",
          ["Pair every colour with a label, a number or a pattern.", "Flag is for observations only.", "Data ramps rise evenly in lightness, so they work in greyscale."]),
         ("One pen", "A 2-pixel stroke and 45° stairs draw the wordmark, the icons, the numerals and the charts.",
          ["No rounded corners; no curves.", "Angles are 0°, 90° or 45°.", "Strokes are 2 px at 24 px and scale in whole multiples."]),
         ("Show the evidence", "Every map and chart carries its source, date and units. Illustrative content is labelled as such.",
          ["Flight number and date on every map.", "Units next to values: ha or ac, %, index.", "Mark samples and placeholders clearly: never present them as results."]),
         ("Built for the field", "Interfaces are used in sun glare, with gloves, on poor signal. Contrast, size and resilience come first.",
          ["Touch targets of at least 40 px; 48 px for primary actions.", "Text contrast of at least 4.5:1, measured.", "Pages work offline-first where possible and degrade gracefully."])]
    blocks = "".join(f'''<article class="ds-principle"><div class="ds-principle__n"><span class="gw-px" data-px="0{i + 1}" style="height:64px"></span></div>
        <div><h3>{t}</h3><p class="ds-p" style="font-size:18px;line-height:28px">{d}</p><ul class="ds-checks">{"".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in li)}</ul></div></article>''' for i, (t, d, li) in enumerate(P))
    secs = [("six", "Six principles", ("These decide every choice that the tokens and components do not. When in doubt, return here.", f'<div class="ds-principles">{blocks}</div>')),
            ("tests", "Four quick tests", ("Run these before anything ships.", table(["Test", "Pass when"], [
                ["Greyscale", "The design still reads with colour removed: values, order and status survive."],
                ["Arm’s length", "A phone held at arm’s length in daylight is readable: no text under 14 px, contrast measured."],
                ["Source", "Every number has a unit, every map a flight and date, every sample a label."],
                ["Next step", "The reader knows what to do next without asking."]])))]
    return page("principles.html", "Principles", "Six rules behind every decision in Groundwork, and four tests to run before anything ships.", "01", "Start", secs)

def brand():
    vers = [("primary-colour", "Primary", BASALT, "Full colour on Basalt. The default."), ("compact-colour", "Compact", BASALT, "Without descriptor, from 96 px."),
            ("stacked-colour", "Stacked", MOSS, "For square and tall formats."), ("symbol-colour", "Symbol", BASALT, "App icons, favicons, social."),
            ("primary-basalt", "One colour, light", CHALK, "Basalt on Chalk or white paper."), ("wordmark-basalt", "Wordmark on Lichen", LICHEN, "Basalt on Lichen, 10.06:1.")]
    cards = "".join(f'''<div class="ds-logo-card"><div class="ds-logo-card__stage" style="background:{bg}"><img src="assets/logos/{f}.svg" alt="HCO {t.lower()}" style="max-height:{96 if 'stacked' in f or 'symbol' in f else 64}px"></div>
        <div class="ds-logo-card__meta"><div><b>{t}</b><span>{d}</span></div><a class="gw-btn gw-btn--ghost gw-btn--s" href="assets/logos/{f}.svg" download>{ic("download")}SVG</a></div></div>''' for f, t, bg, d in vers)
    # construction: compact lockup with module grid
    grid = "".join(f'<line x1="{x}" y1="-200" x2="{x}" y2="1200" />' for x in range(0, 4801, 100)) + "".join(f'<line x1="-200" y1="{y}" x2="5000" y2="{y}" />' for y in range(0, 1001, 100))
    cons = f'''<svg class="hco-logo" viewBox="-400 -360 5600 1760" style="width:100%;height:auto;color:var(--hco-text)" aria-label="Signature construction"><g stroke="var(--hco-flag)" stroke-opacity=".28" stroke-width="4">{grid}</g>
      <g transform="translate(0,0)">{logo(10).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>
      <g fill="var(--hco-text)" font-family="Instrument Sans" font-weight="600" font-size="88" style="text-transform:uppercase;font-stretch:75%" letter-spacing="8">
      <text x="0" y="-200">Symbol 8M</text><text x="1800" y="-200">Wordmark 15M · 30 letter-pixels</text><text x="0" y="1300">1M = 200 units = one sample = one stem</text><text x="3500" y="1300">Cap 5M</text></g>
      <g stroke="var(--hco-flag)" stroke-width="10"><line x1="0" y1="-120" x2="1600" y2="-120"/><line x1="1800" y1="-120" x2="4800" y2="-120"/><line x1="1600" y1="-60" x2="1800" y2="-60"/></g>
      <text x="1640" y="-80" fill="var(--hco-flag)" font-family="Instrument Sans" font-size="64" font-weight="600">1M</text>
      <line x1="-120" y1="600" x2="5000" y2="600" stroke="var(--hco-flag)" stroke-width="8" stroke-dasharray="40 24"/><text x="-380" y="580" fill="var(--hco-flag)" font-family="Instrument Sans" font-size="64" font-weight="600">0.6</text></svg>'''
    trace_demo = f'''<div class="ds-trace-demo">
        <div><div class="gw-label ds-mb8">Ornament · 8 samples</div>{trace(u=10, style="width:160px;color:var(--hco-signal)")}</div>
        <div><div class="gw-label ds-mb8">Divider</div><div style="display:flex;align-items:center;gap:0;color:var(--hco-text-muted)"><span style="flex:1;height:2px;background:currentColor"></span>{trace((0, 0, 1, 2, 2, 1, 0, 0), u=4, style="width:64px")}<span style="flex:1;height:2px;background:currentColor"></span></div></div>
        <div><div class="gw-label ds-mb8">Loader</div><span class="gw-loader" aria-label="Loading example"></span></div>
        <div style="grid-column:1/-1"><div class="gw-label ds-mb8">Display · a measured section at hero scale</div>{trace(tuple([0, 1, 1, 2, 3, 4, 3, 2, 2, 3, 4, 5, 6, 5, 4, 3, 3, 2, 1, 1, 2, 3, 2, 1]), u=10, style="width:100%;color:var(--hco-e3)")}</div></div>'''
    imgs = [("bg-ridges.png", "Pixel ridgelines", "Covers, website hero, motion. Drawn with the wordmark’s pen."), ("block-model.jpg", "Block model", "Explaining method and terrain in reports."),
            ("bg-pixel.png", "Pixel map", "Map backgrounds and screens."), ("bg-dots.jpg", "Dot matrix", "Large print and texture.")]
    imr = "".join(f'<figure class="ds-img"><img src="assets/img/{f}" alt="{t}" loading="lazy"><figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for f, t, d in imgs)
    mis = [("Redraw or reorder the samples", '<svg viewBox="0 0 1600 1000" style="width:100%">' + "".join(f'<rect x="{i*200+10}" y="{(4-h)*200+10}" width="180" height="180" fill="{E[h]}"/>' for i, h in enumerate([0,1,2,3,4,3,2,1])) + "</svg>"),
           ("Round or outline the cells", '<svg viewBox="0 0 1600 1000" style="width:100%">' + "".join(f'<rect x="{i*200+20}" y="{(4-h)*200+20}" width="160" height="160" rx="50" fill="none" stroke="{LICHEN}" stroke-width="24"/>' for i, h in enumerate([0,1,1,2,3,4,3,2])) + "</svg>"),
           ("Use the colour symbol on light grounds", f'<img src="assets/logos/symbol-colour.svg" alt="" style="width:70%">', CHALK),
           ("Retype HCO in a typeface", f'<div style="display:flex;align-items:center;gap:10px"><img src="assets/logos/symbol-colour.svg" alt="" style="width:38%"><span style="font-weight:700;font-size:30px;line-height:1;letter-spacing:-.01em">HCO</span></div>')]
    misr = "".join(f'<div class="ds-mis"><div class="ds-mis__fig" style="{"background:" + m[2] if len(m) > 2 else ""}">{m[1]}<i class="ds-mis__x">{ic("close")}</i></div><p>{m[0]}</p></div>' for m in mis)
    secs = [("signature", "Signature", ("Six versions cover every format. Use the files; never rebuild the artwork.", f'<div class="ds-logos">{cards}</div>')),
            ("construction", "Construction", ("The signature is 24 × 5 modules. The symbol, a sample, a letter stem and the gap between symbol and wordmark are all one module (1M).",
             spec("Signature on the module grid", cons, cap="Letters are drawn on half-module pixels: stems are 2 px, curves step in 1 px stairs, and the crossbar and the C’s upper jaw end on one horizon at 0.6 of the cap height.", grid=False))),
            ("space", "Clear space and size", table(["Version", "Clear space", "Minimum on screen", "Minimum in print"], [
                ["Primary", "2M on every side", "200 px wide", "45 mm wide"], ["Compact", "2M", "96 px", "20 mm"], ["Symbol", "1M", "16 px (pixel-snapped file)", "6 mm"]])
             + note("Below 48 px use the pixel-snapped favicon files: cells sit on whole pixels and the gaps close. Sizes in print are minimums for the descriptor to stay above 6 pt.")),
            ("trace", "The trace", ("A secondary graphic: the eight samples joined by 45° slopes into one continuous line. Use it for dividers, loaders and large display moments, never as a replacement for the symbol.",
             spec("The trace in use", trace_demo, cap="Under 48 px a slope is drawn as pixel stairs; above, as a straight 45° line. The angle is always 45°."))),
            ("imagery", "Imagery", ("All imagery is generated from terrain data. In client work, regenerate it from licensed elevation data for the actual property.", f'<div class="ds-imgs">{imr}</div>')),
            ("misuse", "Misuse", ("Four common mistakes. The Round 3 identity presentation lists the full set.", f'<div class="ds-mises">{misr}</div>'))]
    return page("brand.html", "Brand", "The signature, its construction, the trace and the imagery that carry HCO from a favicon to a vehicle door.", "02", "Foundations", secs,
                meta=("Signature 24 × 5 modules", "Clear space 2M", "Minimum 16 px"))
