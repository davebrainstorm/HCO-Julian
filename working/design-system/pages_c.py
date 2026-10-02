"""Pages: maps and charts, capture and bands."""
from site_base import *
import numpy as np
F = FIELD; ST = F["stats"]

def mapstage(id_="m1", layer="vigour", height=None, side=True, threshold=True):
    seg = "".join(f'<button aria-pressed="{"true" if k == layer else "false"}" data-value="{k}">{t}</button>' for k, t in (("vigour", "Vigour"), ("redge", "Red edge"), ("elevation", "Elevation"), ("land", "Land")))
    obs = "".join(f'''<li><button class="ds-obs" data-obs="{o["n"]}"><span class="gw-marker gw-marker--s"><span data-px="{o["n"]}"></span></span><span><b>{e(o["title"])}</b><small>{e(o["block"])} · {e(o["kind"])}</small></span>
        <span class="gw-priority" data-level="{o["priority"]}"><i><b></b><b></b><b></b></i></span></button></li>''' for o in F["observations"])
    thr = f'''<div class="ds-thr"><button class="gw-switch" aria-checked="false" id="{id_}-thr"><span class="gw-switch__track"></span><span>Show cells below</span></button>
        <input class="gw-range" type="range" id="{id_}-thv" min="0.30" max="0.80" step="0.01" value="0.55" aria-label="Threshold"><output class="gw-num" id="{id_}-tho">0.55</output><span class="gw-num ds-thr__pct" id="{id_}-thp"></span></div>''' if threshold else ""
    panel = f'''<aside class="ds-mapside"><div class="gw-label" style="color:var(--hco-text-subtle)">Observations · Flight 03</div><ul class="ds-obslist">{obs}</ul>
        <div class="ds-obsdetail" id="{id_}-det"><p class="ds-p" style="font-size:14px">Select an observation on the map or in the list.</p></div></aside>''' if side else ""
    return f'''<div class="ds-mapwrap" id="{id_}" data-theme="dark"><div class="ds-maptool"><div class="gw-segmented" data-single>{seg}</div>{thr}<span class="gw-tag gw-tag--caution" style="margin-left:auto">Illustrative data</span></div>
      <div class="ds-mapgrid{" ds-mapgrid--side" if side else ""}"><div><div class="gw-map" data-fieldmap data-layer="{layer}" data-legend="#{id_}-leg"><div class="gw-map__controls"><button aria-label="Zoom in" disabled>{ic("zoom-in")}</button><button aria-label="Zoom out" disabled>{ic("zoom-out")}</button><button aria-label="Full screen" disabled>{ic("fullscreen")}</button></div></div>
      <div class="ds-mapfoot"><div class="gw-legend" id="{id_}-leg"></div><div class="ds-mapfoot__r"><div class="gw-scale" aria-label="Scale: 200 metres"><span>0 · 100 · 200 m</span><span class="gw-scale__bar"><i></i><i></i><i></i><i></i></span></div>
      <div class="ds-stamp"><span>Flight 03 · 9 Sep 2026</span><span>Sample property · 65.5 ha · 8 m cells</span></div>{ic("north", label="North")}</div></div></div>{panel}</div></div>
      <script>document.addEventListener("DOMContentLoaded",function(){{setTimeout(function(){{var w=document.getElementById("{id_}"),m=w.querySelector(".gw-map").__map,D=window.GW_FIELD;
        w.querySelector(".gw-segmented").addEventListener("gw:select",function(e){{m.setLayer(e.detail);upd()}});
        var s=document.getElementById("{id_}-thr"),r=document.getElementById("{id_}-thv"),p=document.getElementById("{id_}-thp");
        function upd(){{if(!s)return;var on=s.getAttribute("aria-checked")==="true";m.setThreshold(on?+r.value:null);var b=m.below(+r.value);p.textContent=on&&b!=null?Math.round(b*100)+"% of cropped area":""}}
        if(s){{s.addEventListener("change",upd);r.addEventListener("input",function(){{if(s.getAttribute("aria-checked")==="true")upd()}})}}
        function show(n){{var o=D.observations.filter(function(x){{return x.n===n}})[0];if(!o)return;m.select(n);w.querySelectorAll("[data-obs]").forEach(function(b){{b.classList.toggle("is-active",b.dataset.obs===n)}});
          var d=document.getElementById("{id_}-det");if(!d)return;d.innerHTML='<div class="gw-label" style="color:var(--hco-observation-text)">Observation '+o.n+' · '+o.kind+'</div><div class="gw-h4" style="margin:8px 0">'+o.title+'</div><p class="ds-p" style="font-size:14px;line-height:20px">'+o.text+'</p><div class="gw-caption gw-subtle">'+o.block+' · cell '+o.x+', '+o.y+'</div>';}}
        w.addEventListener("gw:obs",function(e){{show(e.detail.n)}});w.querySelectorAll("[data-obs]").forEach(function(b){{b.addEventListener("click",function(){{show(b.dataset.obs)}})}});}},30)}})</script>'''

def cellbars():
    rows = ""
    for s in ST:
        n = int(round(s["ndvi"] * 20)); cells = "".join(f'<i style="background:{T["vigour"][min(8, int(k / 20 * 9))] if k < n else "transparent"};{"" if k < n else "box-shadow:inset 0 0 0 1px var(--hco-border)"}"></i>' for k in range(20))
        rows += f'<div class="ds-cbar"><span>{s["id"]} · {e(s["name"])}</span><div class="ds-cbar__cells">{cells}</div><b class="gw-num">{s["ndvi"]:.2f}</b></div>'
    return f'<div class="ds-chart"><div class="ds-chart__head"><div><b>Mean vigour by block</b><span>Vegetation index, Flight 03. One sample = 0.05.</span></div></div>{rows}<div class="ds-chart__foot">Illustrative data</div></div>'
def trend():
    W, H, pad = 460, 230, 40; xs = [pad + i * (W - 2 * pad - 10) / 3 for i in range(4)]
    y = lambda v: H - pad - (v - 0.5) / 0.35 * (H - 2 * pad)
    grid = "".join(f'<line x1="{pad}" x2="{W - pad}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--hco-border)"/><text x="{pad - 10}" y="{y(v) + 4:.1f}" text-anchor="end" font-size="11" fill="var(--hco-text-subtle)">{v:.2f}</text>' for v in (0.5, 0.6, 0.7, 0.8))
    lines = ""
    for s in ST:
        hi = s["id"] == "B"; col = "var(--hco-cat-lichen)" if hi else "var(--hco-stone-400)"
        pts = " ".join(f"{x:.1f},{y(v):.1f}" for x, v in zip(xs, s["trend"]))
        lines += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>' + "".join(f'<rect x="{x - 4:.1f}" y="{y(v) - 4:.1f}" width="8" height="8" fill="{col}"/>' for x, v in zip(xs, s["trend"]))
        lines += f'<text x="{xs[-1] + 10:.1f}" y="{y(s["trend"][-1]) + 4:.1f}" font-size="12" font-weight="600" fill="{col}">{s["id"]}</text>'
    xl = "".join(f'<text x="{x:.1f}" y="{H - 12}" text-anchor="middle" font-size="11" fill="var(--hco-text-subtle)">Flight 0{i + 1}</text>' for i, x in enumerate(xs))
    flag = f'<rect x="{xs[3] - 10:.1f}" y="{y(ST[1]["trend"][3]) - 34:.1f}" width="20" height="20" fill="var(--hco-flag)"/><text x="{xs[3]:.1f}" y="{y(ST[1]["trend"][3]) - 20:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="#0E2423">02</text>'
    return (f'<div class="ds-chart"><div class="ds-chart__head"><div><b>Repeat monitoring</b><span>Mean vegetation index per block over four flights. Block B highlighted; observation 02 flagged.</span></div></div>'
            f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;font-family:var(--hco-font-sans)">{grid}{xl}{lines}{flag}</svg><div class="ds-chart__foot">Illustrative data</div></div>')
def histogram():
    from colour import mix
    D = F; al = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    nd = np.array([al.index(c) for c in D["ndvi"]]).reshape(D["h"], D["w"]) / 63 * 1.0 - 0.1
    b = D["blocks"][1]; v = nd[b["y0"]:b["y1"] + 1, b["x0"]:b["x1"] + 1].ravel()
    bins = np.linspace(0.30, 0.80, 21); hist, _ = np.histogram(v, bins); mx = hist.max()
    bars = ""
    for i, hcount in enumerate(hist):
        c = (bins[i] + bins[i + 1]) / 2; t = (c - 0.15) / 0.75; col = T["vigour"][min(8, max(0, int(t * 8.999)))]
        n = int(round(hcount / mx * 12))
        bars += f'<div class="ds-hist__col" title="{bins[i]:.3f}–{bins[i+1]:.3f}: {hcount} cells">' + "".join(f'<i style="background:{col}"></i>' for _ in range(n)) + "</div>"
    return (f'<div class="ds-chart"><div class="ds-chart__head"><div><b>Distribution, north-east block</b><span>Cells by vegetation index, 0.30–0.80. One sample ≈ {mx / 12:.0f} cells.</span></div></div>'
            f'<div class="ds-hist">{bars}</div><div class="ds-hist__axis gw-num"><span>0.30</span><span>0.55</span><span>0.80</span></div><div class="ds-chart__foot">Illustrative data</div></div>')
def profile():
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    el = np.array([al.index(c) for c in F["elev"]]).reshape(F["h"], F["w"]) / 63
    row = el[30, :]; n = 32; s = row.reshape(n, -1).mean(1); lv = np.round((s - s.min()) / (s.max() - s.min()) * 7).astype(int)
    tr = trace(tuple(int(x) for x in lv), u=10, style="width:100%;color:var(--hco-e2)")
    return (f'<div class="ds-chart"><div class="ds-chart__head"><div><b>Section across the property</b><span>Relative elevation along row 30, west to east, in 32 samples joined by 45° slopes.</span></div></div>'
            f'<div style="padding:8px 0 0">{tr}</div><div class="ds-hist__axis gw-num"><span>West</span><span>1,024 m</span><span>East</span></div><div class="ds-chart__foot">Illustrative data</div></div>')

def data():
    princ = f'<div class="ds-grid ds-grid--4">{"".join(f"<div class=ds-rulecard><span class=gw-px data-px=0{i + 1} style=height:20px></span><b>{t}</b><span>{d}</span></div>" for i, (t, d) in enumerate((("Source on every map", "Flight number, date and property on the map itself, not only in the caption."), ("Cells, not blur", "Show the sampling. Never smooth, interpolate or glow measured values."), ("Colour plus number", "Hover, legends and labels give the value; colour alone never carries meaning."), ("Label the illustrative", "Sample and modelled data carry a visible tag until replaced."))))}</div>'
    ramps = table(["Layer", "Domain", "Ramp", "Notes"], [
        ["Vegetation index", '<span class="gw-num">0.15 – 0.90</span>', ramp_strip(T["vigour"]), "NDVI-style. Brighter is more vigorous."],
        ["Red-edge index", '<span class="gw-num">0.05 – 0.55</span>', ramp_strip(T["vigour"]), "NDRE-style; same ramp, its own domain."],
        ["Relative vigour", '<span class="gw-num">−4 … +4</span>', ramp_strip(T["relative"]), "Difference from the block mean, in steps of 0.05."],
        ["Elevation", '<span class="gw-num">0 – 38 m</span>', ramp_strip(T["terrain"]), "Relative to the lowest point."],
        ["Categorical", "Up to 5 series", ramp_strip(list(T["categorical"].values())), "Beyond five, use small multiples."]])
    mk = f'''<div class="ds-grid ds-grid--4">
      <div class="ds-comp"><div class="ds-comp__fig"><span class="gw-marker gw-marker--s"><span data-px="01"></span></span><span class="gw-marker"><span data-px="02"></span></span><span class="gw-marker gw-marker--l"><span data-px="03"></span></span></div><b>Observation marker</b><span>24, 32, 48 px. The cut corner is the location.</span></div>
      <div class="ds-comp"><div class="ds-comp__fig" style="display:block"><div class="gw-legend" style="width:100%"><div class="gw-label">Vegetation index</div><div class="gw-legend__ramp">{"".join(f'<i style="background:{c}"></i>' for c in T["vigour"])}</div><div class="gw-legend__ticks"><span>0.15</span><span>0.50</span><span>0.90</span></div></div></div><b>Legend</b><span>Nine samples, three ticks, a unit or index name.</span></div>
      <div class="ds-comp"><div class="ds-comp__fig"><div class="gw-scale"><span>0 · 100 · 200 m</span><span class="gw-scale__bar"><i></i><i></i><i></i><i></i></span></div>{ic("north", size=48, label="North")}</div><b>Scale and north</b><span>Alternating samples; north as a pixel arrow.</span></div>
      <div class="ds-comp"><div class="ds-comp__fig" style="display:block"><div class="ds-stamp" style="position:static"><span>Flight 03 · 9 Sep 2026</span><span>Sample property · 8 m cells</span></div></div><b>Map stamp</b><span>Source and date, always on the map.</span></div></div>'''
    charts = f'<div class="ds-wide"><div class="ds-grid ds-grid--2">{cellbars()}{trend()}{histogram()}{profile()}</div></div>'
    crules = dodont("Start bars at zero, label lines directly, and flag observations on the chart where they happened.", "Use 3D, gradients, pie charts, dual axes or more than five colours in one chart.")
    secs = [("principles", "Principles", ("Maps and charts are HCO’s product. They carry evidence, so they follow stricter rules than the rest of the system.", princ)),
            ("map", "The field map", ("Hover a cell for its value. Switch layers to see the scan. Turn on the threshold to light up cells below a value, and select an observation to see its note.", '<div class="ds-wide">' + mapstage() + '</div>')),
            ("ramps", "Layers and ramps", ramps), ("map-parts", "Map components", mk),
            ("charts", "Charts", ("Charts count in samples, connect at 45° and carry the same source line as maps.", charts + crules))]
    return page("data.html", "Maps and charts", "Interactive field maps, legends and charts built from samples: every value sourced, labelled and readable without colour.", "03", "Data", secs,
                meta=("Canvas map", "5 ramps", "4 chart types"), extra_js=("assets/data/field.js", "assets/js/fieldmap.js"))
def ramp_strip(cols): return f'<div class="ds-ramp ds-ramp--s" style="--n:{len(cols)};width:220px">' + "".join(f'<div style="background:{c}"></div>' for c in cols) + "</div>"

def spectrum_svg():
    W, H = 1000, 220; x = lambda w: (w - 400) / 500 * W
    stops = "".join(f'<stop offset="{(w - 400) / 300:.3f}" stop-color="{c}"/>' for w, c in T["spectrum"])
    bands = ""
    for k, b in T["bands"].items():
        x0, x1 = x(b["centre"] - b["half"]), x(b["centre"] + b["half"]); fill = b["colour"] if k != "nir" else "url(#dots)"
        bands += (f'<rect x="{x0:.1f}" y="40" width="{x1 - x0:.1f}" height="100" fill="{fill}" stroke="var(--hco-text)" stroke-width="1.5"/>'
                  f'<text x="{(x0 + x1) / 2:.1f}" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="var(--hco-text)">{k.upper()}</text>'
                  f'<text x="{(x0 + x1) / 2:.1f}" y="164" text-anchor="middle" font-size="14" fill="var(--hco-text-muted)">{b["centre"]} ± {b["half"]}</text>')
    ticks = "".join(f'<line x1="{x(w):.1f}" x2="{x(w):.1f}" y1="176" y2="184" stroke="var(--hco-text-subtle)"/><text x="{x(w):.1f}" y="202" text-anchor="middle" font-size="13" fill="var(--hco-text-subtle)">{w}</text>' for w in range(400, 901, 50))
    return f'''<svg viewBox="-28 0 {W + 56} {H}" style="width:100%;height:auto;font-family:var(--hco-font-sans)" role="img" aria-label="Spectral bands of the multispectral camera on a 400 to 900 nanometre axis">
      <defs><linearGradient id="vis" x1="0" x2="1">{stops}</linearGradient><pattern id="dots" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="var(--hco-stone-800)"/><rect x="1" y="1" width="2" height="2" fill="var(--hco-chalk)"/></pattern>
      <pattern id="dim" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="var(--hco-stone-950)"/><rect x="2" y="2" width="2" height="2" fill="var(--hco-stone-700)"/></pattern></defs>
      <rect x="0" y="60" width="{x(700):.1f}" height="60" fill="url(#vis)" opacity=".85"/><rect x="{x(700):.1f}" y="60" width="{W - x(700):.1f}" height="60" fill="url(#dim)"/>
      <text x="{x(800):.1f}" y="95" text-anchor="middle" font-size="14" font-weight="600" fill="var(--hco-text-muted)" style="text-transform:uppercase;letter-spacing:.1em;font-stretch:75%">Invisible to the eye</text>
      {bands}<line x1="0" x2="{W}" y1="176" y2="176" stroke="var(--hco-border-strong)"/>{ticks}<text x="{W}" y="218" text-anchor="end" font-size="11" fill="var(--hco-text-subtle)">nm</text></svg>'''

def capture():
    B = T["bands"]
    spec_rows = [["RGB camera", "20 MP"], ["Multispectral cameras", "Four, 5 MP each"], ["Bands", "Green 560 ± 16 nm · Red 650 ± 16 nm · Red edge 730 ± 16 nm · Near infrared 860 ± 26 nm"],
                 ["Light sensing", "Sunlight sensor on the airframe"], ["Positioning", "RTK module"], ["Endurance", "Up to 43 minutes per flight"], ["Coverage", "Up to 200 ha per flight"]]
    aircraft = f'''<div class="ds-aircraft"><div class="ds-aircraft__fig">{ic("drone", size=144)}<span class="gw-label">DJI Mavic 3 Multispectral</span></div>
      <div>{table(["", "Manufacturer specification"], spec_rows)}<p class="ds-p" style="font-size:13px;margin-top:12px">Figures are DJI’s published specifications, quoted for design purposes. Check the current specification sheet before quoting them to clients, and never present them as HCO results. No DJI marks or product photography are used in Groundwork.</p></div></div>'''
    bands = f'''{spectrum_svg()}<div class="ds-grid ds-grid--4" style="margin-top:24px">{"".join(f'<div class="ds-band"><i style="background:{b["colour"] if k != "nir" else "repeating-linear-gradient(90deg,var(--hco-chalk) 0 2px,transparent 2px 6px),var(--hco-stone-800)"}"></i><b>{b["name"]}</b><span class="gw-num">{b["centre"]} ± {b["half"]} nm</span><code>--hco-band-{k}</code></div>' for k, b in B.items())}</div>'''
    idx = f'''<div class="ds-grid ds-grid--2"><div class="ds-formula"><div class="gw-label">Vegetation index · NDVI</div><div class="ds-formula__f"><span class="nw">(NIR − Red)</span> <span>/</span> <span class="nw">(NIR + Red)</span></div><p class="ds-p">Healthy canopy reflects near infrared strongly and absorbs red. Higher values mean more vigorous vegetation. In dense canopy NDVI flattens out.</p></div>
      <div class="ds-formula"><div class="gw-label">Red-edge index · NDRE</div><div class="ds-formula__f"><span class="nw">(NIR − Red edge)</span> <span>/</span> <span class="nw">(NIR + Red edge)</span></div><p class="ds-p">The red edge responds to chlorophyll, so NDRE often separates differences that NDVI misses in dense or later-stage crops.</p></div></div>
      {note("Index values are relative. Compare within a field and across flights of the same field, and confirm on the ground before acting. Groundwork never presents an index as a diagnosis.")}'''
    steps = [("calendar", "Plan", "Boundaries, flight time, light and wind."), ("drone", "Fly", "RGB and four bands, with sunlight readings."), ("layers", "Process", "Orthomosaic and index layers."),
             ("flag", "Observe", "Numbered observations, located on the map."), ("report", "Report", "Plain findings and next steps."), ("repeat", "Follow up", "The next flight checks what changed.")]
    flow = '<ol class="ds-flow">' + "".join(f'<li><span class="ds-flow__n gw-px" data-px="0{i + 1}" style="height:16px"></span>{ic(icn, size=48)}<b>{t}</b><span>{d}</span></li>' for i, (icn, t, d) in enumerate(steps)) + "</ol>"
    stamp = spec("Map stamp", '<div class="ds-stamp" style="position:static;display:inline-grid"><span>Flight 03 · 9 Sep 2026 · 10:40</span><span>Mavic 3 Multispectral · G R RE NIR · RTK</span><span>Sample property · 8 m cells · processing [version]</span></div>',
                 src='<div class="ds-stamp">\n  <span>Flight 03 · 9 Sep 2026 · 10:40</span>\n  <span>Mavic 3 Multispectral · G R RE NIR · RTK</span>\n  <span>Sample property · 8 m cells · processing [version]</span>\n</div>',
                 cap="Every map and export carries flight, date, aircraft, bands and processing version.")
    secs = [("aircraft", "The aircraft", ("HCO flies a DJI Mavic 3 Multispectral. The system names it plainly, in text, wherever data comes from it.", aircraft)),
            ("bands", "Four bands", ("The multispectral camera reads four narrow bands. Groundwork gives each a token, so legends and charts name them the same way. Near infrared is drawn as a pattern, because nobody can see it.", bands)),
            ("indices", "Indices", idx), ("flow", "From flight to report", ("Six steps from planning a flight to checking what changed on the next one.", flow)), ("stamp", "Metadata", stamp)]
    return page("capture.html", "Capture and bands", "How data reaches the design: the aircraft HCO flies, the four bands it reads, the indices it makes and the stamp every output carries.", "03", "Data", secs,
                meta=("Mavic 3 Multispectral", "G · R · RE · NIR", "NDVI · NDRE"))
