"""Page: components."""
from site_base import *
F = FIELD
COMPONENTS = []
def comp(id_, title, lead, demo, src, guide=""):
    COMPONENTS.append(title)
    return (id_, title, (lead, spec(title, demo, src=src) + guide))

def components():
    S = []
    # buttons
    demo = f'''<div style="display:grid;gap:24px"><div class="gw-btn-group"><button class="gw-btn gw-btn--primary">Start with the problem {ic("arrow-right", "gw-btn__arrow")}</button><button class="gw-btn gw-btn--secondary">{ic("download")}Download report</button>
      <button class="gw-btn gw-btn--ghost">Cancel</button><button class="gw-btn gw-btn--critical">{ic("trash")}Delete flight</button></div>
      <div class="gw-btn-group"><button class="gw-btn gw-btn--primary gw-btn--s">Small</button><button class="gw-btn gw-btn--primary">Medium</button><button class="gw-btn gw-btn--primary gw-btn--l">Large</button>
      <button class="gw-btn gw-btn--secondary gw-btn--icon" aria-label="Share">{ic("share")}</button><button class="gw-btn gw-btn--secondary" disabled>Disabled</button><button class="gw-btn gw-btn--primary" data-busy="Report generated">Generate report</button></div></div>'''
    src = '''<button class="gw-btn gw-btn--primary">Start with the problem <svg class="gw-icon gw-btn__arrow"><use href="#i-arrow-right"/></svg></button>
<button class="gw-btn gw-btn--secondary"><svg class="gw-icon"><use href="#i-download"/></svg>Download report</button>
<button class="gw-btn gw-btn--ghost">Cancel</button>
<button class="gw-btn gw-btn--critical">Delete flight</button>
<button class="gw-btn gw-btn--primary" aria-busy="true">Generate report</button>'''
    guide = table(["Variant", "Use"], [["Primary", "The one next step on a screen. Lichen on dark, Basalt on light."], ["Secondary", "Alternatives and downloads."], ["Ghost", "Low-emphasis actions: cancel, dismiss."], ["Critical", "Destructive actions, always confirmed."]]) + dodont("Write the action: “Download report”, “Mark as resolved”.", "Use “OK”, “Submit” or “Click here”.")
    S.append(comp("buttons", "Buttons", "Three sizes, four variants. Click “Generate report” to see the busy state: the samples fill in steps.", demo, src, guide))
    # fields
    demo = f'''<div class="ds-grid ds-grid--2" style="gap:24px 32px">
      <label class="gw-field"><span class="gw-field__label">Property name</span><span class="gw-input"><input value="Sample property"></span><span class="gw-field__hint">As it appears on the report cover.</span></label>
      <label class="gw-field"><span class="gw-field__label">Area <small>Optional</small></span><span class="gw-input"><input inputmode="decimal" value="65.5"><span class="gw-input__suffix">ha</span></span><span class="gw-field__hint">Leave blank and we will measure it from the flight.</span></label>
      <label class="gw-field gw-field--invalid"><span class="gw-field__label">Email</span><span class="gw-input gw-input--invalid"><input value="name@" aria-invalid="true"></span><span class="gw-field__hint">{ic("error")}Enter an email address like name@example.com.</span></label>
      <label class="gw-field"><span class="gw-field__label">Block</span><span class="gw-input gw-input--select"><select><option>North paddock</option><option>North-east block</option><option>South flats</option><option>Pivot 1</option></select></span></label>
      <label class="gw-field"><span class="gw-field__label">Search observations</span><span class="gw-input">{ic("search")}<input type="search" placeholder="Drainage, fence, pivot…"></span></label>
      <label class="gw-field"><span class="gw-field__label">Disabled</span><span class="gw-input" aria-disabled="true"><input disabled value="Flight 04"></span></label>
      <label class="gw-field" style="grid-column:1/-1"><span class="gw-field__label">Note</span><textarea class="gw-textarea">Water sits after rain along the lower boundary.</textarea></label></div>'''
    src = '''<label class="gw-field">
  <span class="gw-field__label">Area <small>Optional</small></span>
  <span class="gw-input"><input inputmode="decimal" value="65.5"><span class="gw-input__suffix">ha</span></span>
  <span class="gw-field__hint">Leave blank and we will measure it from the flight.</span>
</label>'''
    guide = dodont("Put the label above the field and the unit inside it. Explain errors in a sentence that says how to fix them.", "Use placeholder text as the label, or show errors in colour alone.")
    S.append(comp("fields", "Text fields", "Labels above, hints below, units inside. Errors say what to do next.", demo, src, guide))
    # selection
    demo = f'''<div class="ds-grid ds-grid--2" style="gap:32px">
      <div style="display:grid;gap:16px"><label class="gw-check"><input type="checkbox" checked><span class="gw-check__box"></span><span>Include red-edge layer<small>Adds an NDRE map to the report.</small></span></label>
        <label class="gw-check"><input type="checkbox"><span class="gw-check__box"></span><span>Email me when processing finishes</span></label>
        <label class="gw-radio"><input type="radio" name="u" checked><span class="gw-radio__box"></span><span>Hectares</span></label><label class="gw-radio"><input type="radio" name="u"><span class="gw-radio__box"></span><span>Acres</span></label></div>
      <div style="display:grid;gap:20px;align-content:start"><button class="gw-switch" aria-checked="true"><span class="gw-switch__track"></span><span>Show observations</span></button>
        <div class="gw-segmented" data-single><button aria-pressed="true">Vigour</button><button aria-pressed="false">Red edge</button><button aria-pressed="false">Elevation</button></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap"><button class="gw-chip" aria-pressed="true">{ic("water")}Drainage</button><button class="gw-chip" aria-pressed="false">{ic("sprout")}Crop health</button><button class="gw-chip" aria-pressed="false">{ic("fence")}Fences</button></div>
        <label class="gw-field" for="cmp-r"><span class="gw-field__label">Threshold <output class="gw-num">0.55</output></span><input class="gw-range" id="cmp-r" type="range" min="0.3" max="0.8" step="0.01" value="0.55"></label></div></div>'''
    src = '''<label class="gw-check"><input type="checkbox" checked><span class="gw-check__box"></span><span>Include red-edge layer</span></label>
<label class="gw-radio"><input type="radio" name="units" checked><span class="gw-radio__box"></span><span>Hectares</span></label>
<button class="gw-switch" aria-checked="true"><span class="gw-switch__track"></span><span>Show observations</span></button>
<div class="gw-segmented" data-single><button aria-pressed="true">Vigour</button><button aria-pressed="false">Red edge</button></div>'''
    S.append(comp("selection", "Selection", "Checkboxes are squares, radios are octagons, switches move in steps. Everything is drawn with the 2 px pen.", demo, src))
    # tags
    demo = f'''<div style="display:grid;gap:20px"><div style="display:flex;flex-wrap:wrap;gap:8px"><span class="gw-tag gw-tag--positive">Processed</span><span class="gw-tag gw-tag--info">Processing</span><span class="gw-tag gw-tag--caution">Check</span><span class="gw-tag gw-tag--critical">Action needed</span><span class="gw-tag gw-tag--observation">Observation 02</span><span class="gw-tag">Draft</span><span class="gw-tag gw-tag--plain">Sample data</span></div>
      <div style="display:flex;flex-wrap:wrap;gap:32px;align-items:center"><span class="gw-priority" data-level="1"><i><b></b><b></b><b></b></i>High priority</span><span class="gw-priority" data-level="2"><i><b></b><b></b><b></b></i>Medium</span><span class="gw-priority" data-level="3"><i><b></b><b></b><b></b></i>Low</span>
      <span class="gw-marker"><span data-px="01"></span></span><span class="gw-marker gw-marker--l"><span data-px="04"></span></span></div></div>'''
    src = '''<span class="gw-tag gw-tag--positive">Processed</span>
<span class="gw-priority" data-level="1"><i><b></b><b></b><b></b></i>High priority</span>
<span class="gw-marker"><span data-px="01"></span></span>'''
    S.append(comp("status", "Tags, priority and markers", "Status is a word plus a colour, priority is counted in samples, and observations get a numbered Flag marker.", demo, src))
    # navigation
    demo = f'''<div style="display:grid;gap:32px"><div class="gw-tabs" role="tablist"><button role="tab" aria-selected="true" aria-controls="tp1">Overview</button><button role="tab" aria-selected="false" aria-controls="tp2">Observations <span class="gw-count">4</span></button><button role="tab" aria-selected="false" aria-controls="tp3">Flights <span class="gw-count">4</span></button><button role="tab" aria-selected="false" aria-controls="tp4">Reports</button></div>
      <div id="tp1" class="ds-p">Season so far: four flights, four open observations.</div><div id="tp2" class="ds-p" hidden>Two high priority, two medium.</div><div id="tp3" class="ds-p" hidden>Flight 04 is processing.</div><div id="tp4" class="ds-p" hidden>The season report is in draft.</div>
      <ol class="gw-crumbs"><li><a href="#">Properties</a></li><li><a href="#">Sample property</a></li><li aria-current="page">Flight 03</li></ol>
      <div class="gw-pagination"><button aria-label="Previous">{ic("chevron-left")}</button><button>1</button><button aria-current="page">2</button><button>3</button><button aria-label="Next">{ic("chevron-right")}</button></div></div>'''
    src = '''<div class="gw-tabs" role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Overview</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Observations <span class="gw-count">4</span></button>
</div>
<ol class="gw-crumbs"><li><a href="#">Properties</a></li><li aria-current="page">Flight 03</li></ol>'''
    S.append(comp("navigation", "Navigation", "Tabs underline the current view with one signal line; arrow keys move between tabs.", demo, src))
    # cards
    o = F["observations"]
    demo = f'''<div class="ds-grid ds-grid--2">{"".join(f"""<article class="gw-card gw-card--link"><div class="gw-card__head"><span class="gw-marker gw-marker--s"><span data-px="{x['n']}"></span></span><span class="gw-priority" data-level="{x['priority']}"><i><b></b><b></b><b></b></i>{'High' if x['priority'] == 1 else 'Medium'}</span></div>
      <div><div class="gw-label gw-muted">{x['kind']} · {x['block']}</div><div class="gw-h4" style="margin-top:8px">{x['title']}</div></div><p class="gw-body-sm gw-muted" style="margin:0">{x['text']}</p>
      <div style="display:flex;gap:8px"><button class="gw-btn gw-btn--secondary gw-btn--s">View on map</button><button class="gw-btn gw-btn--ghost gw-btn--s" data-toast="Marked as resolved" data-toast-body="Observation {x['n']} moves to the season history.">Resolve</button></div></article>""" for x in o[:2])}</div>'''
    src = '''<article class="gw-card">
  <div class="gw-card__head"><span class="gw-marker gw-marker--s"><span data-px="01"></span></span>
    <span class="gw-priority" data-level="1"><i><b></b><b></b><b></b></i>High</span></div>
  <div class="gw-h4">Standing water after rain</div>
  <p class="gw-body-sm gw-muted">Low vigour where water sits after rain…</p>
</article>'''
    S.append(comp("cards", "Cards", "One observation, one card, one next step.", demo, src))
    # stats
    st = F["stats"]
    demo = f'''<div class="ds-grid ds-grid--4">
      <div class="gw-stat"><span class="gw-label gw-muted">Area mapped</span><span class="gw-stat__value"><span data-px="65.5"></span><span class="gw-stat__unit">ha</span></span><span class="gw-caption gw-subtle">Flight 03</span></div>
      <div class="gw-stat"><span class="gw-label gw-muted">Flights this season</span><span class="gw-stat__value"><span data-px="4"></span></span><div class="gw-spark">{"".join(f'<i style="height:{h}px"></i>' for h in (12, 16, 18, 24))}</div></div>
      <div class="gw-stat"><span class="gw-label gw-muted">Open observations</span><span class="gw-stat__value"><span data-px="4"></span></span><span class="gw-stat__delta gw-stat__delta--down">{ic("arrow-up")}2 since Flight 02</span></div>
      <div class="gw-stat"><span class="gw-label gw-muted">Mean vigour</span><span class="gw-stat__value"><span data-px="0.70"></span></span><span class="gw-stat__delta gw-stat__delta--up">{ic("arrow-up")}0.03 since Flight 02</span></div></div>'''
    src = '''<div class="gw-stat">
  <span class="gw-label gw-muted">Area mapped</span>
  <span class="gw-stat__value"><span data-px="65.5"></span><span class="gw-stat__unit">ha</span></span>
</div>'''
    S.append(comp("stats", "Key figures", "Pixel figures for the number, Instrument Sans for the words, and a change line that says compared with what.", demo, src))
    # table
    rows = "".join(f'<tr><td><b>{s["id"]}</b> · {e(s["name"])}</td><td>{e(s["crop"])}</td><td class="is-num">{s["area_ha"]:.1f}</td><td class="is-num">{s["ndvi"]:.2f}</td><td class="is-num">{s["low_pct"]:.0f}%</td><td><div class="gw-spark" style="height:20px">{"".join(f"<i style=height:{int((v - 0.5) * 60)}px></i>" for v in s["trend"])}</div></td></tr>' for s in st)
    demo = f'''<div class="gw-table-wrap"><table class="gw-table"><thead><tr><th><button>Block {ic("chevron-down")}</button></th><th>Crop</th><th class="is-num">Area, ha</th><th class="is-num">Mean index</th><th class="is-num">Below 0.50</th><th>Four flights</th></tr></thead><tbody>{rows}</tbody></table></div>'''
    src = '''<div class="gw-table-wrap"><table class="gw-table">
  <thead><tr><th>Block</th><th class="is-num">Area, ha</th><th class="is-num">Mean index</th></tr></thead>
  <tbody><tr><td>A · North paddock</td><td class="is-num">13.6</td><td class="is-num">0.71</td></tr></tbody>
</table></div>'''
    S.append(comp("tables", "Tables", "Numbers right-aligned and tabular, units in the header, a spark of samples for trends.", demo, src))
    # lists, accordion, timeline
    fl = F["flights"]
    tl = "".join(f'<li class="{"is-done" if f["status"] == "Processed" else "is-current"}"><div style="display:flex;justify-content:space-between;gap:12px"><b>Flight {f["n"]}</b><span class="gw-tag gw-tag--{"positive" if f["status"] == "Processed" else "info"}">{f["status"]}</span></div><div class="gw-body-sm gw-muted">{d(f["date"])} · {f["images"]:,} images · {f["area_ha"]} ha</div></li>' for f in fl)
    demo = f'''<div class="ds-grid ds-grid--2" style="gap:40px"><ol class="gw-timeline">{tl}</ol>
      <div class="gw-accordion"><details open><summary>What does the vegetation index show?</summary><div>How strongly the crop reflects near-infrared light compared with red. Higher values usually mean more vigorous growth. Compare within a field, not between crops.</div></details>
      <details><summary>How often should a field be flown?</summary><div>It depends on the crop and the question. Repeat flights at the same time of day make comparisons fair.</div></details><details><summary>Is this a survey?</summary><div>No. Maps are for observation and planning. They are not a cadastral or engineering survey.</div></details></div></div>'''
    src = '''<ol class="gw-timeline">
  <li class="is-done"><b>Flight 01</b> …</li>
  <li class="is-current"><b>Flight 04</b> …</li>
</ol>
<div class="gw-accordion"><details open><summary>What does the vegetation index show?</summary><div>…</div></details></div>'''
    S.append(comp("lists", "Timelines and accordions", "Flights stack as samples on a 2 px line. Questions open with a pixel plus.", demo, src))
    # feedback
    demo = f'''<div style="display:grid;gap:16px">
      <div class="gw-alert gw-alert--positive">{ic("success")}<div><div class="gw-alert__title">Flight 03 processed</div><div class="gw-alert__body">1,231 images. Index layers and the draft report are ready.</div></div><button class="gw-btn gw-btn--ghost gw-btn--s">Open</button></div>
      <div class="gw-alert gw-alert--caution">{ic("warning")}<div><div class="gw-alert__title">Wind above the planned limit</div><div class="gw-alert__body">Images from the last two passes may be blurred. We will check them before processing.</div></div></div>
      <div class="gw-alert gw-alert--info">{ic("info")}<div><div class="gw-alert__title">Processing Flight 04</div><div class="gw-alert__body">Usually ready within a day.</div></div></div>
      <div class="gw-banner">{ic("info")}<span>Sample data: this property is illustrative.</span><a href="#">Learn more</a></div>
      <div style="display:flex;gap:12px;flex-wrap:wrap"><button class="gw-btn gw-btn--secondary" data-toast="Link copied" data-toast-body="Anyone with the link can view this report for 14 days.">Show a toast</button><button class="gw-btn gw-btn--secondary" data-toast="Upload failed" data-toast-body="Two images had no location data." data-tone="critical" data-icon="error">Show an error toast</button></div></div>'''
    src = '''<div class="gw-alert gw-alert--positive">
  <svg class="gw-icon"><use href="#i-success"/></svg>
  <div><div class="gw-alert__title">Flight 03 processed</div><div class="gw-alert__body">1,231 images…</div></div>
</div>
<script>GW.toast("Link copied", { body: "Anyone with the link can view this report." })</script>'''
    S.append(comp("feedback", "Alerts and toasts", "Inline alerts for things that stay; toasts for things that just happened, with a timer drawn in samples.", demo, src))
    # progress
    cells = "".join(f'<i class="{"is-on" if k < 17 else ""}"></i>' for k in range(24))
    demo = f'''<div class="ds-grid ds-grid--2" style="gap:40px;align-items:center"><div style="display:grid;gap:24px"><div class="gw-progress"><div class="gw-progress__meta"><span>Uploading Flight 04</span><span>71%</span></div><div class="gw-progress__cells">{cells}</div></div>
      <div style="display:grid;gap:8px"><div class="gw-skeleton" style="height:16px;width:60%"></div><div class="gw-skeleton" style="height:16px"></div><div class="gw-skeleton" style="height:16px;width:80%"></div></div></div>
      <div style="display:flex;gap:40px;align-items:flex-end;justify-content:center"><span class="gw-loader"></span><span class="gw-loader" style="--u:10px"></span><span class="gw-loader" data-mono="1" style="--u:6px;color:var(--hco-text-muted)"></span></div></div>'''
    src = '''<div class="gw-progress"><div class="gw-progress__meta"><span>Uploading</span><span>71%</span></div>
  <div class="gw-progress__cells"><i class="is-on"></i>… 24 cells</div></div>
<span class="gw-loader"></span>'''
    S.append(comp("progress", "Progress and loading", "Progress fills in samples; the loader builds the symbol; skeletons sweep in steps.", demo, src))
    # overlays
    demo = f'''<div style="display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start"><button class="gw-btn gw-btn--critical" data-open="dlg1">{ic("trash")}Delete flight</button>
      <span class="gw-tip"><button class="gw-btn gw-btn--secondary gw-btn--icon" aria-label="What is NDRE?">{ic("help")}</button><span class="gw-tip__bubble" role="tooltip">Red-edge index: (NIR − RE) / (NIR + RE)</span></span>
      <div class="gw-menu" role="menu"><button role="menuitem">{ic("download")}Download PDF<kbd>⌘D</kbd></button><button role="menuitem">{ic("share")}Share link</button><button role="menuitem">{ic("print")}Print</button><hr><button role="menuitem" style="color:var(--hco-critical)">{ic("trash")}Delete</button></div></div>
      <div class="gw-scrim" id="dlg1" role="dialog" aria-modal="true" aria-labelledby="dlg1t"><div class="gw-dialog"><div class="gw-dialog__head"><b id="dlg1t" class="gw-h4">Delete Flight 04?</b><button class="gw-btn gw-btn--ghost gw-btn--icon" data-close aria-label="Close">{ic("close")}</button></div>
      <div class="gw-dialog__body">1,226 images and their index layers will be deleted. Reports that use this flight will keep their exported PDFs. This cannot be undone.</div>
      <div class="gw-dialog__foot"><button class="gw-btn gw-btn--ghost" data-close>Keep flight</button><button class="gw-btn gw-btn--critical" data-close data-toast="Flight 04 deleted" data-tone="critical" data-icon="trash">Delete flight</button></div></div></div>'''
    src = '''<button class="gw-btn gw-btn--critical" data-open="confirm">Delete flight</button>
<div class="gw-scrim" id="confirm" role="dialog" aria-modal="true">
  <div class="gw-dialog">…<button class="gw-btn gw-btn--ghost" data-close>Keep flight</button></div>
</div>'''
    S.append(comp("overlays", "Dialogs, tooltips and menus", "Overlays are the only things with a shadow. Destructive dialogs say exactly what will be lost.", demo, src))
    # upload + avatar + empty
    demo = f'''<div class="ds-grid ds-grid--2" style="gap:24px"><div class="gw-dropzone" tabindex="0">{ic("upload", size=48)}<div><strong>Drop flight images here</strong><br><span class="gw-body-sm">or <a href="#">browse</a>. JPG and TIF, with location data.</span></div></div>
      <div class="gw-empty">{ic("flag", size=48)}<div class="gw-h4">No open observations</div><p class="gw-body-sm gw-muted" style="margin:0;max-width:32ch">Nothing needs attention after Flight 03. We will check again on the next flight.</p><button class="gw-btn gw-btn--secondary gw-btn--s">View history</button></div>
      <ul class="gw-list" style="grid-column:1/-1">{"".join(f'<li><span class="gw-avatar">{i}</span><div style="flex:1"><b>{n}</b><div class="gw-body-sm gw-muted">{r}</div></div><span class="gw-tag gw-tag--plain">{t}</span></li>' for i, n, r, t in (("PL", "[Pilot name]", "Flights and processing", "HCO"), ("CL", "[Client name]", "Owner, Sample property", "Client")))}</ul></div>'''
    src = '''<div class="gw-dropzone" tabindex="0"><svg class="gw-icon gw-icon--48"><use href="#i-upload"/></svg>
  <strong>Drop flight images here</strong></div>
<div class="gw-empty">…</div>'''
    S.append(comp("upload", "Upload, empty states and people", "Drop zones dash in samples. Empty states say why it is empty and what happens next.", demo, src))
    lead_intro = f"{len(S)} component families, every one live on this page. Each uses semantic tokens only, so it works in both themes; use the moon button on any example to check."
    return page("components.html", "Components", "Square-cornered, token-driven components for HCO’s portal, reports, field app and website. Plain HTML and CSS, no framework required.", "04", "Components",
                [("intro", "How components are built", (lead_intro, table(["Rule", "Detail"], [["Tokens only", "Components reference <code>--hco-*</code> semantic tokens, never raw hex."], ["Prefix", "Classes start with <code>gw-</code>; modifiers use <code>--</code>."],
                   ["States", "Hover, focus-visible, disabled and busy are designed for every interactive part."], ["Accessible by default", "Native elements first; ARIA only where a native element does not exist."], ["No dependencies", "<code>groundwork.css</code> and <code>groundwork.js</code>, nothing else."]])))] + S,
                meta=(f"{len(S)} families", "Contrast-checked", "No framework"))
