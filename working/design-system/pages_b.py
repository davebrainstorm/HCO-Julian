"""Pages: colour, typography, layout, motion, icons."""
from site_base import *
from colour import contrast, lch, to_oklab, hex2rgb
TH = T["themes"]

def sw(name, hx, role, ink=None):
    L, C, h = lch(hx); r, g, b = (round(v * 255) for v in hex2rgb(hx))
    ink = ink or ("#0E2423" if L > 0.6 else "#F4F5EF")
    return (f'<button class="ds-swatch" data-copy="{hx}" aria-label="Copy {name} {hx}"><div class="ds-swatch__chip" style="background:{hx};{"outline:1px solid var(--hco-border);outline-offset:-1px;" if L > .93 else ""}"><span style="color:{ink}">{e(name)}</span></div>'
            f'<div class="ds-swatch__meta"><b>{hx}</b><span>RGB {r} {g} {b}</span><span>OKLCH {L:.2f} {C:.3f} {h:.0f}</span><span>{role}</span></div></button>')
def ramp_row(label, cols, txt=False):
    cells = "".join(f'<div style="background:{c}">{f"<span style=color:{chr(35)}0E2423>{i}</span>" if txt else ""}</div>' for i, c in enumerate(cols))
    return f'<div class="ds-ramp-row"><span>{label}</span><div class="ds-ramp ds-ramp--s" style="--n:{len(cols)}">{cells}</div></div>'
def rating(r): return ("AAA", "pass") if r >= 7 else ("AA", "pass") if r >= 4.5 else ("Large / graphics", "pass") if r >= 3 else ("Not for text", "fail")

def colour():
    C = T["core"]
    core = "".join(sw(n.title(), C[n], r) for n, r in (("basalt", "Ground. The default canvas and text on light."), ("chalk", "Light ground and text on dark."), ("moss", "Secondary dark ground; links on light."),
                                                        ("sage", "Ramp step E1; quiet graphics."), ("lichen", "Signal: primary action on dark, positive, E3."), ("flag", "Observations only. Never decoration.")))
    st = T["stone"]
    stone = '<div class="ds-ramp" style="--n:16">' + "".join(f'<div style="background:{st[k]};outline:1px solid var(--hco-border);outline-offset:-1px"><span style="color:{"#0E2423" if int(k) < 400 else "#F4F5EF"}">{k}</span></div>' for k in st) + "</div>"
    stone += table(["Step", "Hex", "Use"], [[f"<code>stone-{k}</code>", f'<span class="sw" style="background:{st[k]}"></span> {st[k]}', u] for k, u in (
        ("0", "Raised surfaces in light theme (cards, inputs)."), ("50", "Chalk. Light canvas; text on dark."), ("300", "Muted text on dark (5.95:1 on Basalt)."), ("500", "Subtle text on light (4.72:1 on Chalk)."),
        ("600", "Muted text on light (6.35:1)."), ("850", "Raised surfaces in dark theme."), ("900", "Basalt. Dark canvas; text on light."), ("950", "Sunken surfaces, inputs and map canvas on dark."), ("975", "Deepest: map backgrounds and tooltips."))])
    sem_keys = [("canvas", "Page background"), ("surface", "Default surface"), ("surface-raised", "Cards, panels"), ("surface-sunken", "Wells, code, hover"), ("border", "Hairlines"), ("border-strong", "Inputs, emphasis"),
                ("text", "Body text"), ("text-muted", "Secondary text"), ("text-subtle", "Placeholders, captions"), ("accent", "Primary action"), ("on-accent", "Text on primary action"), ("signal", "Active marks, indicators"),
                ("focus", "Focus ring"), ("link", "Links"), ("positive", "Positive status"), ("caution", "Caution status"), ("critical", "Critical status"), ("info", "Information"), ("observation", "Observation marker")]
    sem = table(["Token", "Dark", "Light", "Use"], [[f"<code>--hco-{k}</code>", f'<span class="sw" style="background:{TH["dark"][k]}"></span> {TH["dark"][k]}', f'<span class="sw" style="background:{TH["light"][k]}"></span> {TH["light"][k]}', u] for k, u in sem_keys])
    def status_stage(th):
        return (f'<div data-theme="{th}" style="background:var(--hco-canvas);color:var(--hco-text);padding:24px;display:grid;gap:16px">'
                f'<div class="gw-label" style="color:var(--hco-text-muted)">{th.title()} theme</div><div style="display:flex;flex-wrap:wrap;gap:8px">'
                + "".join(f'<span class="gw-tag gw-tag--{k}">{t}</span>' for k, t in (("positive", "On track"), ("caution", "Check"), ("critical", "Action needed"), ("info", "Processing"), ("observation", "Observation 03")))
                + f'</div><div class="gw-alert gw-alert--critical">{ic("error")}<div><div class="gw-alert__title">Upload failed</div><div class="gw-alert__body">Two images were missing location data. Nothing else was lost.</div></div></div></div>')
    status = f'<div class="ds-grid ds-grid--2" style="gap:1px;background:var(--hco-border);border:1px solid var(--hco-border)">{status_stage("dark")}{status_stage("light")}</div>'
    status += note("Status colours always travel with an icon or a word. <strong>Flag is not an error colour</strong>: errors use Critical, so a red-orange square always means an observation.")
    rows = []
    for c in T["checks"]:
        if c["bg"] not in ("canvas", "surface-raised") and not c["bg"].endswith("tint") and c["fg"] not in ("on-accent", "focus"): continue
        lab, cl = rating(c["ratio"])
        rows.append([c["theme"].title(), f'<code>{c["fg"]}</code>', f'<code>{c["bg"]}</code>', f'<span class="gw-num">{c["ratio"]:.2f}:1</span>', f'<span class="{cl}">{lab}</span>'])
    con = table(["Theme", "Foreground", "Background", "Ratio", "Rating"], rows)
    D = [("Elevation E0–E4", T["elevation"]), ("Terrain, 9 steps", T["terrain"]), ("Vigour, 9 steps", T["vigour"]), ("Relative vigour, −4…+4", T["relative"]), ("Categorical, 5", list(T["categorical"].values())), ("Bands G · R · RE · NIR", [b["colour"] for b in T["bands"].values()])]
    data = "".join(ramp_row(l, c) for l, c in D) + f'<p class="ds-p" style="margin-top:16px">Ranges, domains and map rules are on <a href="data.html#ramps">Maps and charts</a>.</p>'
    cv = T["cvd"]
    vis = ""
    for key, label in (("vigour", "Vigour"), ("relative", "Relative vigour"), ("categorical", "Categorical")):
        base = T["vigour"] if key == "vigour" else T["relative"] if key == "relative" else list(T["categorical"].values())
        vis += f'<h3>{label}</h3>' + ramp_row("Typical vision", base) + "".join(ramp_row(k.title(), cv[k][key]) for k in ("protanopia", "deuteranopia", "tritanopia", "greyscale"))
    vis += note(f'Lightness in the vigour ramp rises evenly (OKLab L {T["L"]["vigour"][0]:.2f} → {T["L"]["vigour"][-1]:.2f}), so order survives every simulation and greyscale. The five categorical colours stay at least ΔE {T["cat_min_de"]["tritanopia"]:.1f} apart under every simulation (Machado et al. 2009, full severity).')
    rules = dodont("Use the full-colour symbol and colour ramps on Basalt, Moss or the map canvas.", "Put Lichen, E3 or E4 on Chalk: Lichen on Chalk is 1.47:1.") + dodont("Reserve Flag for observations, so the marker always means the same thing.", "Use Flag for errors, highlights, buttons or decoration.")
    secs = [("core", "Core palette", ("Six colours, measured. Basalt is the ground, colour is the signal. Click a swatch to copy its value.", f'<div class="ds-grid">{core}</div>')),
            ("stone", "Stone neutrals", ("Sixteen steps between Basalt and white, interpolated in OKLab so each step is even to the eye. Brand anchors are exact: stone-900 is Basalt, stone-50 is Chalk.", stone)),
            ("themes", "Themes", ("Components never use raw colours. They use semantic tokens, which change with the theme.", sem)),
            ("status", "Status", ("Four states plus the observation marker, tuned separately for each theme.", status)),
            ("contrast", "Contrast", ("Every text pairing below is computed from the token values (WCAG 2.2 relative luminance). Subtle text is for placeholders and captions only.", con)),
            ("data", "Data colour", ("Ramps for maps and charts. Each is monotonic in lightness, so values read in order without relying on hue.", data)),
            ("vision", "Colour vision", ("The data ramps as seen with the three common colour-vision deficiencies and in greyscale.", vis)),
            ("rules", "Rules", rules)]
    return page("colour.html", "Colour", "A Basalt ground, colour as signal, and data ramps that hold up in greyscale and for colour-blind readers.", "02", "Foundations", secs,
                meta=("6 core", "16 neutrals", "2 themes", "5 data ramps"))

def typography():
    Tt = T["type"]
    weights = "".join(f'<div class="ds-weight"><span style="font-weight:{w}">Observe first.</span><span class="gw-label">{n} · {w}</span></div>' for n, w in (("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700)))
    weights += '<div class="ds-weight"><span style="font-weight:600;font-stretch:75%;text-transform:uppercase;letter-spacing:.04em">Field intelligence</span><span class="gw-label">Condensed · 600</span></div>'
    face = f'''<div class="ds-face"><div class="ds-face__aa">Aa</div><div><div class="gw-label" style="color:var(--hco-text-subtle)">Primary typeface</div><div class="gw-h2" style="margin:8px 0 16px">Instrument Sans</div>
      <p class="ds-p">A contemporary grotesk with a true condensed width, used for everything people read. Pixel letters are kept for the wordmark and pixel figures.</p>
      <p class="ds-p" style="font-size:13px">Licence: SIL Open Font License 1.1, which permits print, web and app use. Loaded from Google Fonts on this site; font files are not packaged with Groundwork. The final typeface is a Stage 2 decision.</p></div></div>
      <div class="ds-weights">{weights}</div>'''
    glyphs = f'<div class="ds-glyphs">{px("0123456789", 56)}<div style="margin-top:24px">{px("0.71 · 65.5 · 12/09 · 94% · +3", 32)}</div></div>'
    live = f'''<div class="ds-pxlive"><label class="gw-field" style="max-width:320px"><span class="gw-field__label">Type a figure</span><span class="gw-input gw-input--l"><input id="pxin" value="2026" inputmode="decimal" maxlength="12" autocomplete="off"></span><span class="gw-field__hint">Digits, . , - + : / and % are drawn.</span></label>
      <div class="ds-pxlive__out" id="pxout" data-px="2026" style="height:96px;color:var(--hco-signal)"></div></div>
      <script>document.addEventListener("DOMContentLoaded",function(){{var i=document.getElementById("pxin"),o=document.getElementById("pxout");i.addEventListener("input",function(){{o.setAttribute("data-px",i.value.replace(/[^0-9.,:+\\-/% ]/g,"")||"0");o.__px=null;GW.renderPx(o.parentNode)}})}})</script>'''
    scale = ""
    samples = {"display-xl": "Field to report.", "display": "Start with the problem.", "h1": "We actually show up.", "h2": "Practical. Not theory.", "h3": "Your operation comes first.",
               "h4": "Three areas to look at first", "body-lg": "HCO helps farmers, ranchers and agricultural businesses solve business, regulatory and field problems.",
               "body": "We show up, learn the operation, identify the issue, and give you practical options for what to do next.", "body-sm": "Flight 03 · 9 September 2026 · 1,231 images",
               "label": "Field intelligence · Business & operations", "caption": "Figure 2 · Illustrative data, not survey results."}
    for k, (sz, lh, tr, w) in Tt.items():
        cls = "gw-" + k
        scale += f'<div class="ds-type-row"><div class="ds-type-row__spec"><b>{k}</b><span class="gw-num">{sz} / {lh} · {"+" if tr > 0 else ""}{tr * 100:g}% · {w}</span><code>.{cls}</code></div><div class="{cls} ds-type-row__s">{e(samples[k])}</div></div>'
    resp = table(["Style", "Desktop", "Below 768 px"], [["display-xl", "112 / 112", "56 / 56"], ["display", "80 / 80", "48 / 48"], ["h1", "56 / 56", "40 / 44"], ["h2", "40 / 48", "30 / 36"], ["h3 and below", "unchanged", "unchanged"]])
    rhythm = f'''<div style="max-width:560px"><div class="gw-label" style="color:var(--hco-text-muted)">Observation 02</div><div class="gw-h3" style="margin-top:8px">Uneven growth on the upper slope</div>
      <p class="gw-body" style="margin:16px 0 0;color:var(--hco-text-muted)">Patchy canopy, clearer in the red-edge layer than in the vegetation index. Scout on foot to confirm the cause before the next flight.</p>
      <div class="gw-caption gw-subtle" style="margin-top:16px">North-east block · Flight 03 · 9 Sep 2026</div></div>'''
    nums = table(["Value", "Format", "Example"], [["Index (NDVI, NDRE)", "2 decimals", '<span class="gw-num">0.71</span>'], ["Area", "1 decimal, unit", '<span class="gw-num">65.5 ha</span> or <span class="gw-num">161.9 ac</span>'],
                                                 ["Share", "Whole per cent", '<span class="gw-num">6%</span>'], ["Date", "Day month year", "9 Sep 2026; 9 September 2026 in reports"], ["Counts", "Thousands separator", '<span class="gw-num">1,231 images</span>']])
    secs = [("typeface", "Typeface", face), ("pixel", "Pixel figures", ("Bespoke tabular figures drawn with the wordmark’s pen: 8 × 10 px, one-pixel tracking. Use them for section numbers, observation markers and key figures, never for running text.", glyphs + spec("Live pixel figures", live, grid=False, theme=False))),
            ("scale", "Type scale", ("Eleven styles. Every size and line height is a multiple of 4 px; space between blocks keeps to the 8 px grid.", f'<div class="ds-type">{scale}</div>')),
            ("responsive", "Responsive sizes", resp), ("rhythm", "Rhythm", ("Turn on the grid to see text and spacing keep to the 8 px grid.", spec("Observation text on the 8 px grid", rhythm))),
            ("numbers", "Numbers and units", ("Figures are tabular in tables and data. Units always travel with the value.", nums))]
    return page("typography.html", "Typography", "Instrument Sans for everything people read, pixel figures for the numbers that matter, and one scale on a 4 px rhythm.", "02", "Foundations", secs,
                meta=("Instrument Sans", "11 styles", "4 px rhythm"), desc="Groundwork typography: typeface, pixel figures, scale and rhythm.")

def layout():
    S = T["space"]
    space = "".join(f'<div class="ds-space"><code>space-{k}</code><span class="gw-num">{v} px</span><i style="width:{max(v, 1)}px"></i></div>' for k, v in S.items() if k != "0")
    def gridrow(cols, margin, gutter, label, w=100):
        cells = "".join('<i></i>' for _ in range(cols))
        return f'<div class="ds-gridrow"><div class="gw-label">{label}</div><div class="ds-gridrow__cols" style="--c:{cols};--g:{gutter}px;padding:0 {margin}px">{cells}</div></div>'
    grids = gridrow(12, 40, 12, "Desktop · 12 columns · margin 80 · gutter 24") + gridrow(8, 24, 10, "Tablet · 8 columns · margin 40 · gutter 16") + gridrow(4, 12, 8, "Phone · 4 columns · margin 16 · gutter 16")
    bp = table(["Token", "Min width", "Columns", "Margin", "Gutter"], [["sm", "480 px", "4", "16", "16"], ["md", "768 px", "8", "40", "16"], ["lg", "1024 px", "12", "56", "24"], ["xl", "1280 px", "12", "80", "24"], ["2xl", "1536 px", "12", "auto, max 1440 content", "24"]])
    shape = f'''<div class="ds-grid ds-grid--4">
      <div class="ds-shape"><div class="ds-shape__fig"><i style="width:64px;height:64px;border:2px solid currentColor"></i></div><b>Radius 0</b><span>Every corner is square.</span></div>
      <div class="ds-shape"><div class="ds-shape__fig"><span class="gw-marker gw-marker--l"><span data-px="01"></span></span></div><b>45° notch</b><span>Markers and tooltips point with a 45° cut.</span></div>
      <div class="ds-shape"><div class="ds-shape__fig"><button class="gw-btn gw-btn--secondary" style="outline:2px solid var(--hco-focus);outline-offset:2px">Focus</button></div><b>2 px pen</b><span>Focus rings, controls and icons share one stroke.</span></div>
      <div class="ds-shape"><div class="ds-shape__fig"><svg viewBox="0 0 64 64" style="width:64px" fill="currentColor"><path d="M20 0h24v2h-24zM16 2h32v2h-32zM14 4h4v2h-4zM46 4h4v2h-4z"/></svg>{ic("clock", size=48)}</div><b>Octagons, not circles</b><span>Round things step at 45°, like the O.</span></div></div>'''
    elev = f'''<div class="ds-grid ds-grid--4">{"".join(f'<div class="ds-elev" style="{s}"><b>{n}</b><span>{d}</span></div>' for n, d, s in (
        ("Level 0 · flat", "Content on the canvas.", "background:var(--hco-canvas)"), ("Level 1 · rule", "Hairline border, same surface.", "background:var(--hco-canvas);border:1px solid var(--hco-border)"),
        ("Level 2 · raised", "Raised surface and border.", "background:var(--hco-surface-raised);border:1px solid var(--hco-border)"), ("Level 3 · overlay", "Menus, dialogs, toasts. The only shadow.", "background:var(--hco-surface-overlay);border:1px solid var(--hco-border-strong);box-shadow:var(--hco-shadow-overlay)")))}</div>'''
    z = table(["Token", "Value", "Use"], [[f"<code>--hco-z-{k}</code>", v, u] for (k, v), u in zip(T["z"].items(), ("Content", "Raised cards", "Sticky headers", "Top navigation", "Drawers", "Dialogs", "Toasts", "Tooltips"))])
    secs = [("module", "One module", ("In print the module is 1M, the width of one symbol sample. On screen the sample is 8 px: space, sizes and the baseline are all counted in samples or half-samples.",
             f'<div class="ds-module">{"".join(f"<div><i style=width:{s}px;height:{s}px></i><span class=gw-num>{s} px</span><span>{t}</span></div>" for s, t in ((4, "Half-sample"), (8, "Sample"), (16, "2 samples"), (24, "Icon"), (40, "Control"), (48, "Primary target")))}</div>')),
            ("spacing", "Spacing", ("Fourteen steps, from 4 to 160 px. Use the scale; never type a value in between.", f'<div class="ds-spaces">{space}</div>')),
            ("grid", "Grid", ("A 12-column grid on desktop, 8 on tablet and 4 on phones. Content aligns to columns; space between components comes from the spacing scale.", grids)),
            ("breakpoints", "Breakpoints", bp), ("shape", "Shape", shape), ("elevation", "Elevation", ("Borders do the work. Shadows are reserved for things that float.", elev + z))]
    return page("layout.html", "Layout and space", "One module everywhere: an 8 px sample for space and size, a 12-column grid, square corners and 45° angles.", "02", "Foundations", secs,
                meta=("8 px sample", "12 / 8 / 4 columns", "Radius 0"))

def motion():
    M_ = T["motion"]; EZ = T["ease"]
    toks = table(["Token", "Value", "Use"], [[f"<code>--hco-dur-{k}</code>", f'<span class="gw-num">{v}</span>', u] for (k, v), u in zip(M_.items(), ("Hover colour, toggles", "Buttons, chips", "Most transitions", "Panels, dialogs", "Map scan"))]
                + [[f"<code>--hco-ease-{k}</code>", f"<code>{v}</code>", u] for (k, v), u in zip(EZ.items(), ("Things arriving", "Things leaving", "Pixel elements: five steps, like the five levels", "Progress, timers"))])
    demo = f'''<div class="ds-motion">{"".join(f'<div class="ds-motion__row"><span class="gw-label">{n}</span><div class="ds-motion__track"><i style="transition-timing-function:var(--hco-ease-{k});transition-duration:{d}"></i></div></div>' for n, k, d in (("Settle · 320 ms", "settle", "320ms"), ("Step · 320 ms", "step", "320ms"), ("Exit · 200 ms", "exit", "200ms"), ("Linear · 1200 ms", "linear", "1200ms")))}
      <button class="gw-btn gw-btn--secondary gw-btn--s" onclick="this.parentNode.classList.toggle('is-go')">{ic("play")}Play</button></div>'''
    sig = f'''<div class="ds-grid ds-grid--2">
      <div class="ds-motion-card"><div class="ds-motion-card__fig"><span class="gw-loader" style="--u:10px"></span></div><b>Ridgeline loader</b><span>The symbol builds sample by sample in five steps. Use it for waits over 400 ms.</span></div>
      <div class="ds-motion-card"><div class="ds-motion-card__fig"><button class="gw-btn gw-btn--primary" data-toast="Report shared" data-toast-body="The link expires in 14 days.">Share report</button></div><b>Toast timer</b><span>Twelve samples drain as the toast times out, so the wait is visible.</span></div>
      <div class="ds-motion-card"><div class="ds-motion-card__fig"><span class="gw-btn gw-btn--secondary">Open report {ic("arrow-right", "gw-btn__arrow")}</span></div><b>Step</b><span>Arrows move one sample in steps on hover. Data never glides.</span></div>
      <div class="ds-motion-card"><div class="ds-motion-card__fig" style="padding:0"><div class="ds-scan-demo" data-fieldmap data-pins="off" data-layer="land"></div></div><b>Scan</b><span>Changing a map layer sweeps across like a pass of the drone. <button class="gw-btn gw-btn--ghost gw-btn--s" data-scan>Run scan</button></span></div></div>
      <script>document.addEventListener("click",function(e){{var b=e.target.closest("[data-scan]");if(!b)return;var m=document.querySelector(".ds-scan-demo").__map;m.setLayer(m.layer==="land"?"vigour":"land")}})</script>'''
    secs = [("principles", "Principles", f'<div class="ds-grid">{"".join(f"<div><h3 style=margin-top:0>{t}</h3><p class=ds-p>{d}</p></div>" for t, d in (("Settle, don’t bounce", "Things arrive quickly and come to rest. No elastic overshoot, no springs."), ("Step for data", "Pixel elements move in five steps, like the five levels of the symbol: numbers tick, samples fill."), ("Scan for change", "When data changes, a single sweep shows what changed. Never fade data in and out.")))}</div>'),
            ("tokens", "Tokens", (None, toks + spec("Easing compared", demo, grid=False))), ("signatures", "Signature motion", sig),
            ("reduced", "Reduced motion", note("When the operating system asks for reduced motion, every animation in Groundwork completes instantly: loaders show the full symbol, scans redraw in one frame and toasts stay until dismissed.", "eye"))]
    secs[1] = ("tokens", "Tokens", toks + spec("Easing compared", demo, grid=False))
    return page("motion.html", "Motion", "Motion that settles, steps and scans, with five durations and four easings, and nothing that bounces.", "02", "Foundations", secs,
                meta=("5 durations", "4 easings", "Reduced-motion safe"), extra_js=("assets/data/field.js", "assets/js/fieldmap.js"))

def icons():
    groups = {}
    for n, d in ICONS.items(): groups.setdefault(d["group"], []).append(n)
    tiles = ""
    for g, names in groups.items():
        tiles += f'<h3 class="ds-icgroup">{g} <span class="gw-num gw-subtle">{len(names)}</span></h3><div class="ds-icons">' + "".join(
            f'<button class="ds-ic" data-copy=\'<svg class="gw-icon"><use href="#i-{n}"/></svg>\' data-name="{n}" aria-label="Copy {n} icon">{ic(n)}<span>{n}</span></button>' for n in names) + "</div>"
    tools = f'''<div class="ds-ictools"><label class="gw-input" style="width:min(360px,100%)">{ic("search")}<input type="search" id="icq" placeholder="Filter {len(ICONS)} icons" aria-label="Filter icons"></label>
      <div class="gw-segmented" data-single id="icsize"><button aria-pressed="true" data-value="24">24 px</button><button aria-pressed="false" data-value="48">48 px</button></div></div>
      <script>document.addEventListener("DOMContentLoaded",function(){{var q=document.getElementById("icq");q.addEventListener("input",function(){{var v=q.value.toLowerCase();document.querySelectorAll(".ds-ic").forEach(function(b){{b.hidden=v&&b.dataset.name.indexOf(v)<0}})}});
      document.getElementById("icsize").addEventListener("gw:select",function(e){{document.querySelector(".ds-iconset").classList.toggle("is-48",e.detail==="48")}})}})</script>'''
    rows = ICONS["drone"]["rows"]
    big = "".join(f'<i class="{"on" if ch == "#" else ""}{" live" if 2 <= x <= 21 and 2 <= y <= 21 else ""}"></i>' for y, r in enumerate(rows) for x, ch in enumerate(r))
    cons = f'''<div class="ds-iccons"><div class="ds-icgrid">{big}</div><div><h3 style="margin-top:0">Drawn on 24 × 24</h3><ul class="ds-checks">
      {"".join(f"<li>{ic('check')}<span>{t}</span></li>" for t in ("Live area 20 × 20, with 2 px of padding.", "Strokes are 2 px: the wordmark’s pen at icon size.", "Diagonals are 45° stairs of 1 px.", "No curves: circles are octagons, like the O in HCO.", "Shapes are merged into one path and use currentColor."))}</ul></div></div>'''
    use = table(["Context", "Size", "Note"], [["Inline with 14–16 px text", "24 px", "Align to the text’s centre; 8 px gap"], ["Buttons and fields", "24 px", "20 px in dense menus"], ["Empty states, feature tiles", "48 px", "Exact 2× scale only"], ["Touch targets", "40–48 px", "The icon is 24 px; the target is larger"]])
    use += dodont("Scale icons in whole multiples (24, 48, 72) so pixels stay sharp.", "Scale to 20 or 30 px, rotate, or mix with rounded icon sets.")
    secs = [("set", "The set", (f"{len(ICONS)} icons in three groups. Click an icon to copy its markup.", tools + f'<div class="ds-iconset">{tiles}</div>')),
            ("construction", "Construction", cons), ("usage", "Usage", use)]
    return page("icons.html", "Icons", f"{len(ICONS)} pixel icons drawn with the wordmark’s pen: 24 px grid, 2 px strokes, 45° stairs and no curves.", "02", "Foundations", secs,
                meta=(f"{len(ICONS)} icons", "24 px grid", "SVG sprite"))
