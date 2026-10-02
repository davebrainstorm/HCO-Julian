"""Templates: portal, report, field app, website, email. Standalone layouts, built only from Groundwork parts."""
from site_base import *
from pages_c import mapstage, cellbars, trend, spectrum_svg
F = FIELD; OBS = F["observations"]; ST = F["stats"]; FL = F["flights"]

def tbar(name):
    return (f'<div class="tpl-bar" data-theme="dark"><a href="index.html" class="tpl-bar__back">{ic("arrow-left")}Groundwork</a><span class="tpl-bar__sep"></span><span class="gw-label">Template · {e(name)}</span>'
            f'<span class="gw-tag gw-tag--caution">Sample data</span><span style="margin-left:auto"></span><button class="gw-btn gw-btn--ghost gw-btn--icon gw-btn--s" data-theme-toggle aria-label="Switch theme">{ic("sun", "ds-ic-sun")}{ic("moon", "ds-ic-moon")}</button></div>')
def tpl(fname, title, body, theme="dark", js=(), css="templates.css", bodycls=""):
    PAGES[fname] = dict(title=title, sections=[])
    return (head(title, f"Groundwork template: {title}.", css=css, key="gw-theme:" + fname).replace('data-theme="dark"', f'data-theme="{theme}" data-theme-key="gw-theme:{fname}"', 1) + f'<body class="{bodycls}">{SPRITE}{tbar(title)}{body}'
            f'<div class="gw-toast-region" aria-live="polite"></div>{scripts(js)}</body></html>')

def obs_item(o, active=False):
    return (f'<button class="pt-obs{" is-active" if active else ""}" data-obs="{o["n"]}"><span class="gw-marker gw-marker--s"><span data-px="{o["n"]}"></span></span>'
            f'<span class="pt-obs__t"><b>{e(o["title"])}</b><small>{e(o["block"])} · {e(o["kind"])}</small></span><span class="gw-priority" data-level="{o["priority"]}"><i><b></b><b></b><b></b></i></span></button>')

def portal():
    nav = [("home", "Overview", True, ""), ("map", "Map", False, ""), ("flag", "Observations", False, "4"), ("drone", "Flights", False, "4"), ("report", "Reports", False, ""), ("field", "Property", False, "")]
    rail = "".join(f'<a href="#" class="pt-nav{" is-on" if on else ""}"{" aria-current=page" if on else ""}>{ic(i)}<span>{t}</span>{f"<em class=gw-num>{c}</em>" if c else ""}</a>' for i, t, on, c in nav)
    kpi = f'''<div class="pt-kpis">
      <div class="gw-stat pt-kpi"><span class="gw-label gw-muted">Area mapped</span><span class="gw-stat__value"><span data-px="65.5" data-ha="65.5"></span><span class="gw-stat__unit" data-unit>ha</span></span><span class="gw-caption gw-subtle">4 blocks · 8 m cells</span></div>
      <div class="gw-stat pt-kpi"><span class="gw-label gw-muted">Flights this season</span><span class="gw-stat__value"><span data-px="4"></span></span><span class="gw-caption gw-subtle">Next: Flight 05 · to be scheduled</span></div>
      <div class="gw-stat pt-kpi"><span class="gw-label gw-muted">Open observations</span><span class="gw-stat__value"><span data-px="4"></span></span><span class="gw-stat__delta gw-stat__delta--down">{ic("arrow-up")}2 high priority</span></div>
      <div class="gw-stat pt-kpi"><span class="gw-label gw-muted">Mean vigour</span><span class="gw-stat__value"><span data-px="0.70"></span></span><span class="gw-stat__delta gw-stat__delta--up">{ic("arrow-up")}0.03 since Flight 02</span></div></div>'''
    blocks = "".join(f'<tr><td><b>{s["id"]}</b> · {e(s["name"])}</td><td class="is-num" data-ha="{s["area_ha"]}">{s["area_ha"]:.1f}</td><td class="is-num">{s["ndvi"]:.2f}</td><td class="is-num">{s["low_pct"]:.0f}%</td><td><div class="gw-spark" style="height:20px">{"".join(f"<i style=height:{max(2, int((v - 0.5) * 60))}px></i>" for v in s["trend"])}</div></td></tr>' for s in ST)
    flights = "".join(f'<li class="{"is-done" if f["status"] == "Processed" else "is-current"}"><div style="display:flex;justify-content:space-between;gap:12px"><b>Flight {f["n"]}</b><span class="gw-tag gw-tag--{"positive" if f["status"] == "Processed" else "info"}">{f["status"]}</span></div><div class="gw-body-sm gw-muted">{d(f["date"])} · {f["images"]:,} images</div></li>' for f in reversed(FL))
    body = f'''<div class="pt-shell"><aside class="pt-rail"><a class="pt-logo" href="#" aria-label="HCO portal">{logo(18)}</a><nav class="pt-navs">{rail}</nav>
      <div class="pt-rail__foot"><a href="#" class="pt-nav">{ic("help")}<span>Help</span></a><div class="pt-user"><span class="gw-avatar">CL</span><span><b>[Client name]</b><small>Sample property</small></span></div></div></aside>
      <main class="pt-main"><header class="pt-head"><div><ol class="gw-crumbs"><li><a href="#">Properties</a></li><li aria-current="page">Sample property</li></ol>
        <h1 class="gw-h2" style="margin:12px 0 4px">Sample property</h1><div class="gw-body-sm gw-muted"><span data-ha="65.5">65.5</span> <span data-unit>ha</span> · 4 blocks · last flight 9 Sep 2026</div></div>
        <div class="pt-head__acts"><div class="gw-segmented" data-single id="units"><button aria-pressed="true" data-value="ha">ha</button><button aria-pressed="false" data-value="ac">ac</button></div>
        <button class="gw-btn gw-btn--secondary" data-toast="Link copied" data-toast-body="Anyone with the link can view this property for 14 days.">{ic("share")}Share</button><button class="gw-btn gw-btn--primary" data-busy="Report ready">{ic("download")}Season report</button></div></header>
        <div class="gw-alert gw-alert--info pt-alert">{ic("info")}<div><div class="gw-alert__title">Flight 04 is processing</div><div class="gw-alert__body">Images from 23 September arrived. Maps usually update within a day; we will email you.</div></div><button class="gw-btn gw-btn--ghost gw-btn--s">Details</button></div>
        {kpi}
        <section class="pt-card pt-card--map"><div class="pt-card__head"><div><b class="gw-h4">Field map</b><span class="gw-body-sm gw-muted">Flight 03 · 9 Sep 2026</span></div></div>{mapstage("pm", side=True)}</section>
        <div class="pt-two"><section class="pt-card"><div class="pt-card__head"><b class="gw-h4">Blocks</b><a class="gw-btn gw-btn--ghost gw-btn--s" href="#">Compare {ic("arrow-right")}</a></div>
          <div class="gw-table-wrap" style="border:0"><table class="gw-table"><thead><tr><th>Block</th><th class="is-num">Area, <span data-unit>ha</span></th><th class="is-num">Index</th><th class="is-num">Below 0.50</th><th>Trend</th></tr></thead><tbody>{blocks}</tbody></table></div></section>
          <section class="pt-card"><div class="pt-card__head"><b class="gw-h4">Flights</b><button class="gw-btn gw-btn--ghost gw-btn--s">{ic("upload")}Upload</button></div><ol class="gw-timeline" style="padding:8px 24px 0">{flights}</ol></section></div>
        <p class="gw-caption gw-subtle pt-note">Template with illustrative data. Procedural terrain and vegetation; not a real property, not survey data.</p></main></div>
      <script>document.addEventListener("DOMContentLoaded",function(){{document.getElementById("units").addEventListener("gw:select",function(e){{var ac=e.detail==="ac";
        document.querySelectorAll("[data-ha]").forEach(function(n){{var v=+n.dataset.ha*(ac?2.4711:1);if(n.hasAttribute("data-px")){{n.setAttribute("data-px",v.toFixed(1));n.__px=null;GW.renderPx(n.parentNode)}}else n.textContent=v.toFixed(1)}});
        document.querySelectorAll("[data-unit]").forEach(function(n){{n.textContent=ac?"ac":"ha"}})}})}})</script>'''
    return tpl("portal.html", "Client portal", body, js=("assets/data/field.js", "assets/js/fieldmap.js"), bodycls="tpl-portal")

def report():
    def pg(n, title, inner, cls=""):
        return (f'<section class="rp-page {cls}"><header class="rp-run"><span>{logo(12)}</span><span>Field observations report · Sample property · Flight 03</span></header>'
                f'<div class="rp-in">{inner}</div><footer class="rp-foot"><span>Illustrative data. Not a survey, an agronomic prescription or legal advice.</span>{px(f"{n:02d}", 12)}</footer></section>')
    cover = f'''<section class="rp-page rp-cover" data-theme="dark"><div class="rp-cover__img"><canvas data-ridges data-b0=".30" data-amp=".38" data-static="on"></canvas></div>
      <div class="rp-cover__top">{logo(28)}<span class="gw-label">Field observations report</span></div>
      <div class="rp-cover__title"><div class="gw-label" style="color:var(--hco-signal)">Flight 03 · 9 September 2026</div><h1 class="gw-display" style="margin:16px 0 0;font-size:64px;line-height:64px">Sample property</h1>
      <p class="gw-body-lg gw-muted" style="margin:16px 0 0">Four observations across four blocks, two of them high priority.</p></div>
      <div class="rp-cover__foot"><span>Prepared for [Client name]</span><span>Prepared by [Name], HCO</span><span>[Date issued]</span></div></section>'''
    summ = f'''<div class="rp-h"><span class="gw-px" data-px="01" style="height:24px;color:var(--hco-signal)"></span><h2 class="gw-h2">At a glance</h2></div>
      <div class="rp-kpis"><div class="gw-stat"><span class="gw-label gw-muted">Area flown</span><span class="gw-stat__value"><span data-px="65.5"></span><span class="gw-stat__unit">ha</span></span></div>
      <div class="gw-stat"><span class="gw-label gw-muted">Observations</span><span class="gw-stat__value"><span data-px="4"></span></span></div><div class="gw-stat"><span class="gw-label gw-muted">Mean vigour</span><span class="gw-stat__value"><span data-px="0.70"></span></span></div></div>
      <p class="gw-body-lg" style="margin:32px 0 0;max-width:60ch">Most of the property is growing evenly. Two areas need attention before the next irrigation cycle: standing water on the south flats and a dry arc on the outer span of Pivot 1.</p>
      <h3 class="gw-h4" style="margin:40px 0 12px">What to do next</h3><ol class="rp-next">{"".join(f'<li><span class="gw-marker gw-marker--s"><span data-px="{o["n"]}"></span></span><div><b>{e(o["title"])}</b><span>{e(o["text"].split(". ")[-1])}</span></div><span class="gw-priority" data-level="{o["priority"]}"><i><b></b><b></b><b></b></i>{"High" if o["priority"] == 1 else "Medium"}</span></li>' for o in OBS)}</ol>'''
    mp = f'''<div class="rp-h"><span class="gw-px" data-px="02" style="height:24px;color:var(--hco-signal)"></span><h2 class="gw-h2">Map</h2></div><p class="gw-body gw-muted" style="margin:8px 0 24px">Vegetation index from Flight 03, with the four observations.</p>
      <div class="rp-map" data-theme="dark"><div class="gw-map" data-fieldmap data-layer="vigour" data-legend="#rp-leg"></div><div class="rp-map__foot"><div class="gw-legend" id="rp-leg" style="width:280px"></div><div class="ds-stamp" style="position:static"><span>Flight 03 · 9 Sep 2026</span><span>Mavic 3 Multispectral · 8 m cells</span></div></div></div>'''
    obs = f'''<div class="rp-h"><span class="gw-px" data-px="03" style="height:24px;color:var(--hco-signal)"></span><h2 class="gw-h2">Observations</h2></div>
      {"".join(f'<article class="rp-obs"><span class="gw-marker"><span data-px="{o["n"]}"></span></span><div><div class="gw-label gw-muted">{e(o["kind"])} · {e(o["block"])}</div><h3 class="gw-h4" style="margin:6px 0 8px">{e(o["title"])}</h3><p class="gw-body" style="margin:0">{e(o["text"])}</p><div class="gw-caption gw-subtle" style="margin-top:8px">Location: cell {o["x"]}, {o["y"]} · Evidence: vegetation and red-edge layers, Flight 03</div></div><span class="gw-priority" data-level="{o["priority"]}"><i><b></b><b></b><b></b></i>{"High" if o["priority"] == 1 else "Medium"}</span></article>' for o in OBS)}'''
    blocks = "".join(f'<tr><td><b>{s["id"]}</b> · {e(s["name"])}</td><td>{e(s["crop"])}</td><td class="is-num">{s["area_ha"]:.1f}</td><td class="is-num">{s["ndvi"]:.2f}</td><td class="is-num">{s["low_pct"]:.0f}%</td></tr>' for s in ST)
    res = f'''<div class="rp-h"><span class="gw-px" data-px="04" style="height:24px;color:var(--hco-signal)"></span><h2 class="gw-h2">Blocks</h2></div>
      <div class="gw-table-wrap"><table class="gw-table"><thead><tr><th>Block</th><th>Crop</th><th class="is-num">Area, ha</th><th class="is-num">Mean index</th><th class="is-num">Below 0.50</th></tr></thead><tbody>{blocks}</tbody></table></div>
      <div style="margin-top:32px">{trend()}</div>'''
    meth = f'''<div class="rp-h"><span class="gw-px" data-px="05" style="height:24px;color:var(--hco-signal)"></span><h2 class="gw-h2">Method and limits</h2></div>
      <div class="rp-cols"><div><h3 class="gw-h4">Capture</h3><p class="gw-body gw-muted">Flown with a DJI Mavic 3 Multispectral: an RGB camera and four multispectral bands (green 560 nm, red 650 nm, red edge 730 nm, near infrared 860 nm), with a sunlight sensor and RTK positioning.</p>
      <h3 class="gw-h4">Indices</h3><p class="gw-body gw-muted">Vegetation index = (NIR − Red) / (NIR + Red). Red-edge index = (NIR − Red edge) / (NIR + Red edge). Values are relative: compare within a field and between flights.</p></div>
      <div><h3 class="gw-h4">Limits</h3><p class="gw-body gw-muted">Observations are based on imagery and index values. Confirm them on the ground before acting. This report is not a survey, an agronomic prescription or legal advice.</p>
      <h3 class="gw-h4">Data</h3><p class="gw-body gw-muted">This template uses illustrative, procedural data. No real property, client or result is shown.</p></div></div>'''
    body = (f'<div class="rp-doc">{cover}{pg(2, "Summary", summ)}{pg(3, "Map", mp)}{pg(4, "Observations", obs)}{pg(5, "Blocks", res)}{pg(6, "Method", meth)}</div>'
            f'<div class="rp-print"><button class="gw-btn gw-btn--primary" onclick="window.print()">{ic("print")}Print or save as PDF · A4</button></div>')
    return tpl("report.html", "Field report", body, theme="light", js=("assets/data/ridges.js", "assets/js/ridges.js", "assets/data/field.js", "assets/js/fieldmap.js"), bodycls="tpl-report")

def app():
    def phone(label, inner, nav=0):
        tabs = "".join(f'<span class="ap-tab{" is-on" if i == nav else ""}">{ic(n)}<small>{t}</small></span>' for i, (n, t) in enumerate((("home", "Today"), ("map", "Map"), ("plus", "Add"), ("flag", "Notes"))))
        return f'<figure class="ap-phone"><div class="ap-screen" data-theme="dark"><div class="ap-status"><span>9:41</span><span>{ic("signal", size=16)}{ic("battery", size=16)}</span></div><div class="ap-body">{inner}</div><nav class="ap-tabs">{tabs}</nav></div><figcaption class="gw-label">{label}</figcaption></figure>'
    today = f'''<div class="ap-head"><div><div class="gw-label gw-muted">Sample property</div><div class="gw-h3">Today</div></div><span class="gw-avatar">PL</span></div>
      <div class="gw-card" style="padding:16px"><div class="gw-label gw-muted">Next flight</div><div class="gw-h4">Flight 05 · to be scheduled</div><div class="gw-body-sm gw-muted">Plan when wind and light suit; batteries charged.</div><button class="gw-btn gw-btn--primary" style="width:100%">{ic("calendar")}Plan flight</button></div>
      <div class="gw-label gw-muted" style="margin-top:8px">Open observations</div>{obs_item(OBS[0])}{obs_item(OBS[3])}{obs_item(OBS[1])}'''
    mapv = f'''<div class="ap-head"><div><div class="gw-label gw-muted">Flight 03 · Vigour</div><div class="gw-h3">Map</div></div><button class="gw-btn gw-btn--secondary gw-btn--icon gw-btn--s" aria-label="Layers">{ic("layers")}</button></div>
      <div class="gw-map ap-map" data-fieldmap data-layer="vigour"></div><div style="display:flex;gap:6px;flex-wrap:wrap"><button class="gw-chip" aria-pressed="true">Vigour</button><button class="gw-chip" aria-pressed="false">Red edge</button><button class="gw-chip" aria-pressed="false">Land</button></div>
      <div class="ap-sheet"><div class="ap-sheet__grip"></div><div style="display:flex;gap:12px;align-items:flex-start"><span class="gw-marker gw-marker--s"><span data-px="04"></span></span><div><b>{e(OBS[3]["title"])}</b><div class="gw-body-sm gw-muted">{e(OBS[3]["block"])} · 120 m away</div></div></div><button class="gw-btn gw-btn--secondary gw-btn--s" style="width:100%">{ic("arrow-right")}Navigate</button></div>'''
    add = f'''<div class="ap-head"><div><div class="gw-label gw-muted">New observation</div><div class="gw-h3">What did you see?</div></div><button class="gw-btn gw-btn--ghost gw-btn--icon gw-btn--s" aria-label="Close">{ic("close")}</button></div>
      <div class="gw-dropzone" style="padding:24px 12px">{ic("camera", size=48)}<strong>Add photos</strong></div>
      <div style="display:flex;gap:6px;flex-wrap:wrap" data-single><button class="gw-chip" aria-pressed="true">{ic("water")}Drainage</button><button class="gw-chip" aria-pressed="false">{ic("sprout")}Crop</button><button class="gw-chip" aria-pressed="false">{ic("fence")}Fence</button><button class="gw-chip" aria-pressed="false">{ic("pivot")}Irrigation</button></div>
      <div class="gw-field"><span class="gw-field__label">Priority</span><div class="gw-segmented" data-single style="width:100%"><button aria-pressed="true" style="flex:1">High</button><button aria-pressed="false" style="flex:1">Medium</button><button aria-pressed="false" style="flex:1">Low</button></div></div>
      <label class="gw-field"><span class="gw-field__label">Note</span><textarea class="gw-textarea" style="min-height:80px">Water lying along the lower boundary after rain.</textarea></label>
      <div class="gw-body-sm gw-muted" style="display:flex;gap:8px;align-items:center">{ic("location")}Using location · South flats</div><button class="gw-btn gw-btn--primary gw-btn--l" style="width:100%" data-toast="Observation saved" data-toast-body="It will sync when you have signal.">Save observation</button>'''
    o = OBS[0]
    det = f'''<div class="ap-head"><button class="gw-btn gw-btn--ghost gw-btn--icon gw-btn--s" aria-label="Back">{ic("arrow-left")}</button><span class="gw-tag gw-tag--observation">Observation {o["n"]}</span></div>
      <div class="ap-photo"><img src="assets/img/map-tile.png" alt="" class="pix"><span class="gw-marker gw-marker--s" style="position:absolute;left:40%;top:38%"><span data-px="01"></span></span></div>
      <div><div class="gw-label gw-muted">{e(o["kind"])} · {e(o["block"])}</div><div class="gw-h3" style="margin-top:6px">{e(o["title"])}</div></div><p class="gw-body-sm gw-muted" style="margin:0">{e(o["text"])}</p>
      <div class="gw-table-wrap"><table class="gw-table"><tbody><tr><td>Vegetation index</td><td class="is-num">0.31</td></tr><tr><td>Block mean</td><td class="is-num">0.68</td></tr></tbody></table></div>
      <div style="display:flex;gap:8px"><button class="gw-btn gw-btn--secondary" style="flex:1">{ic("map")}Map</button><button class="gw-btn gw-btn--primary" style="flex:1" data-toast="Marked as resolved">{ic("check")}Resolve</button></div>'''
    body = f'''<main class="ap-wrap"><header class="ap-intro"><div class="gw-label" style="color:var(--hco-signal)">Template · Field app</div><h1 class="gw-h1" style="margin:16px 0 0">In the paddock, on a phone.</h1>
      <p class="gw-body-lg gw-muted" style="margin:16px 0 0;max-width:56ch">Large targets, high contrast and offline-first notes. The same markers, numbers and words as the report.</p></header>
      <div class="ap-row">{phone("01 · Today", today, 0)}{phone("02 · Map", mapv, 1)}{phone("03 · New observation", add, 2)}{phone("04 · Observation", det, 3)}</div></main>'''
    return tpl("app.html", "Field app", body, js=("assets/data/field.js", "assets/js/fieldmap.js"), bodycls="tpl-app")

def website():
    srv1 = [("sliders", "Regulatory and compliance", "Agriculture, land use, environmental, food and operating requirements."), ("index", "Business decisions", "Expansion, equipment purchases, new revenue opportunities and partnerships."),
            ("report", "Contracts and vendors", "Pricing, obligations, terms and risks."), ("share", "Markets and supply chains", "Buyers, suppliers, distribution, pricing and weak points.")]
    srv2 = [("drone", "Drone mapping", "High-resolution and multispectral imagery."), ("sprout", "Crop health and problem areas", "Index maps and field imagery to prioritise scouting."),
            ("fence", "Farm and ranch mapping", "Irrigation, fences, roads, drainage and facilities."), ("repeat", "Repeat monitoring", "The same fields, flown again, compared fairly."), ("flag", "Clear reports", "Maps, observations, priority areas and practical next steps.")]
    def srv(items): return "".join(f'<li>{ic(i)}<div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in items)
    steps = [("We show up", "On the property, at the operation, in person."), ("Learn the operation", "How it runs, what matters, what has been tried."), ("Identify the issue", "From the ground and from the air, with evidence."), ("Give you options", "Practical options for what to do next, in plain words.")]
    vals = ["We actually show up.", "Your operation comes first.", "Practical. Not theory.", "Start with the problem."]
    body = f'''<div class="ws" data-theme="dark"><header class="ws-nav"><a href="#" aria-label="HCO home">{logo(22)}</a><nav class="ws-nav__links"><a href="#approach">Approach</a><a href="#services">Services</a><a href="#field">Field intelligence</a><a href="#contact">Contact</a></nav>
      <a class="gw-btn gw-btn--primary gw-btn--s" href="#contact">Start with the problem</a><button class="gw-btn gw-btn--ghost gw-btn--icon ws-nav__menu" aria-label="Menu">{ic("menu")}</button></header>
      <section class="ws-hero"><canvas data-ridges data-b0=".40" data-amp=".40" aria-hidden="true"></canvas><div class="ws-hero__in"><div class="gw-label" style="color:var(--hco-signal)">Agriculture · Ranching · Rural business · Field intelligence</div>
        <h1 class="gw-display-xl ws-hero__h">Understand systems.<br>Protect people.</h1><p class="gw-body-lg ws-hero__p">HCO helps farmers, ranchers and agricultural businesses solve business, regulatory and field problems. We show up, learn the operation, identify the issue and give you practical options for what to do next.</p>
        <div class="gw-btn-group"><a class="gw-btn gw-btn--primary gw-btn--l" href="#contact">Start with the problem {ic("arrow-right", "gw-btn__arrow")}</a><a class="gw-btn gw-btn--secondary gw-btn--l" href="#approach">How we work</a></div></div>
        <div class="ws-vals">{"".join(f'<div>{px(f"0{i + 1}", 16)}<span>{v}</span></div>' for i, v in enumerate(vals))}</div></section>
      <section class="ws-sec" id="services"><div class="ws-sec__head"><div class="gw-label" style="color:var(--hco-signal)">What we do</div><h2 class="gw-h1">Two kinds of problem. One way of working.</h2></div>
        <div class="ws-two"><div><h3 class="gw-h3">Business and operations</h3><ul class="ws-srv">{srv(srv1)}</ul></div><div><h3 class="gw-h3">Field and property intelligence</h3><ul class="ws-srv">{srv(srv2)}</ul></div></div></section>
      <section class="ws-sec ws-sec--rule" id="approach"><div class="ws-sec__head"><div class="gw-label" style="color:var(--hco-signal)">How we work</div><h2 class="gw-h1">Start with the problem.</h2></div>
        <ol class="ws-steps">{"".join(f'<li><span class="gw-px" data-px="0{i + 1}" style="height:40px;color:var(--hco-signal)"></span><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate(steps))}</ol></section>
      <section class="ws-sec ws-field" id="field"><div class="ws-field__copy"><div class="gw-label" style="color:var(--hco-signal)">Field intelligence</div><h2 class="gw-h1">See what the eye can’t.</h2>
        <p class="gw-body-lg gw-muted">We fly a multispectral drone that reads four narrow bands of light, including near infrared, which the eye cannot see. The result is a map of where the crop is thriving and where it needs a look, with numbered observations and next steps.</p>
        <ul class="ws-get">{"".join(f"<li>{ic('check')}{t}</li>" for t in ("Maps you can read on a phone", "Numbered observations, located", "Priority areas, ranked", "Practical next steps"))}</ul></div>
        <div class="ws-field__fig"><div class="gw-map" data-fieldmap data-layer="vigour"></div><div class="ws-field__bands">{spectrum_svg()}</div></div></section>
      <section class="ws-sec ws-cta" id="contact"><div><div class="gw-label" style="color:var(--hco-signal)">Contact</div><h2 class="gw-display" style="margin:16px 0 0">Start with<br>the problem.</h2><p class="gw-body-lg gw-muted" style="max-width:40ch">Tell us what is happening on the operation. We will come back with a plain next step.</p></div>
        <form class="ws-form" onsubmit="event.preventDefault();GW.toast('Preview only',{{body:'This form is a design preview and does not send.',icon:'info',tone:'info'}})">
          <label class="gw-field"><span class="gw-field__label">Name</span><span class="gw-input gw-input--l"><input autocomplete="name"></span></label><label class="gw-field"><span class="gw-field__label">Email</span><span class="gw-input gw-input--l"><input type="email" autocomplete="email"></span></label>
          <label class="gw-field"><span class="gw-field__label">Operation <small>Optional</small></span><span class="gw-input gw-input--l"><input placeholder="Farm, ranch or business"></span></label>
          <label class="gw-field"><span class="gw-field__label">What’s the problem?</span><textarea class="gw-textarea"></textarea></label><button class="gw-btn gw-btn--primary gw-btn--l">Send {ic("arrow-right", "gw-btn__arrow")}</button>
          <p class="gw-caption gw-subtle" style="margin:0">Design preview: this form does not send. Contact details to be confirmed.</p></form></section>
      <footer class="ws-foot"><div>{logo(28)}<p class="gw-body-sm gw-muted" style="margin:16px 0 0">High Country Observations</p></div><nav><a href="#approach">Approach</a><a href="#services">Services</a><a href="#field">Field intelligence</a><a href="#contact">Contact</a></nav>
        <p class="gw-caption gw-subtle">[Contact details to be confirmed] · © HCO</p></footer></div>'''
    return tpl("website.html", "Website", body, js=("assets/data/ridges.js", "assets/js/ridges.js", "assets/data/field.js", "assets/js/fieldmap.js"), bodycls="tpl-site")

def email():
    hi = [o for o in OBS if o["priority"] == 1]
    body = f'''<main class="em-wrap"><div class="em-meta"><div><span class="gw-label gw-muted">From</span> HCO reports &lt;[reports address]&gt;</div><div><span class="gw-label gw-muted">Subject</span> Your Flight 03 report is ready: 2 high-priority observations</div></div>
      <div class="em" data-theme="light"><div class="em-head" data-theme="dark">{logo(20)}<span class="gw-label gw-muted">Flight 03 · 9 Sep 2026</span></div>
      <div class="em-body"><h1 class="gw-h2" style="margin:0">Your Flight 03 report is ready.</h1><p class="gw-body-lg gw-muted" style="margin:16px 0 0">Most of Sample property is growing evenly. Two areas need attention before the next irrigation cycle.</p>
      <div class="em-kpis"><div><span class="gw-label gw-muted">Area</span><b><span data-px="65.5" style="height:28px"></span><small>ha</small></b></div><div><span class="gw-label gw-muted">Observations</span><b><span data-px="4" style="height:28px"></span></b></div><div><span class="gw-label gw-muted">High priority</span><b><span data-px="2" style="height:28px"></span></b></div></div>
      {"".join(f'<div class="em-obs"><span class="gw-marker gw-marker--s"><span data-px="{o["n"]}"></span></span><div><b>{e(o["title"])}</b><span>{e(o["block"])} · {e(o["text"].split(". ")[-1])}</span></div></div>' for o in hi)}
      <a class="gw-btn gw-btn--primary gw-btn--l" href="report.html" style="margin-top:24px">Open the report {ic("arrow-right")}</a></div>
      <div class="em-foot">You are receiving this because [Client name] is set up for reports on Sample property. <a href="#">Manage emails</a></div></div>
      <p class="gw-caption gw-subtle em-note">Design preview. Production emails use table-based layout with inline styles; this page shows the design.</p></main>'''
    return tpl("email.html", "Email", body, theme="dark", bodycls="tpl-email")
