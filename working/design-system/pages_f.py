"""Pages: voice and words, tokens and downloads."""
from site_base import *
import re

def content():
    voice = [("We actually show up.", "Write like you were there.", "Say what was seen, where and when. Specific beats general.", "Water lies along the lower boundary of the south flats after rain.", "Drainage issues were identified in some areas."),
             ("Your operation comes first.", "Lead with their decision.", "Open with what it means for the client, then the evidence.", "Fix the drainage line before the next irrigation cycle.", "Our advanced analysis has revealed several insights."),
             ("Practical. Not theory.", "Plain words, next steps.", "Short sentences. Every finding ends with something to do.", "Check nozzles and pressure on the last span.", "Irrigation efficiency could potentially be optimised."),
             ("Start with the problem.", "Problem first, method last.", "Method and equipment belong at the end, for those who want them.", "Two areas need attention. Here is where, and why.", "Using state-of-the-art multispectral sensing, we…")]
    vb = "".join(f'''<article class="ds-voice"><div class="ds-voice__q">{px(f"0{i + 1}", 20)}<b>{q}</b></div><div><h3 style="margin:0 0 8px">{t}</h3><p class="ds-p">{d}</p>
        <div class="ds-dodont" style="margin-top:12px"><div class="ds-do"><span class="gw-label">Write</span><p>{y}</p></div><div class="ds-dont"><span class="gw-label">Not</span><p>{n}</p></div></div></div></article>''' for i, (q, t, d, y, n) in enumerate(voice))
    formula = f'''<div class="ds-formula"><div class="gw-label">The observation sentence</div><div class="ds-formula__f" style="font-size:22px;line-height:32px">[What we saw] <span>+</span> [where] <span>+</span> [what to do next]</div>
      <p class="ds-p" style="margin-top:16px">“Patchy canopy on the upper slope of the north-east block. Scout on foot to confirm the cause.”</p></div>'''
    words = table(["Use", "Instead of", "Why"], [["observation", "issue, problem, defect", "Neutral and specific; it is what HCO does."], ["vigour", "health (unqualified)", "An index measures vigour, not health."],
        ["map", "survey", "HCO maps are not cadastral or engineering surveys."], ["next step", "recommendation, prescription", "Practical, and not agronomic or legal advice."], ["flight", "mission, sortie", "Plain and accurate."], ["we", "HCO Group, the company", "Warm and direct; the trading name is still to be confirmed."]])
    never = f'''<ul class="ds-checks ds-checks--x">{"".join(f"<li>{ic('close')}<span>{t}</span></li>" for t in (
        "Claim licences, certifications or accreditations that have not been confirmed.", "Describe maps as surveys, or offer legal, agronomic or financial advice.",
        "Present sample, modelled or illustrative data as a client result.", "Quote equipment specifications as HCO performance; name the source.", "Use “AI-powered”, “revolutionary”, “cutting-edge” or “solutions”."))}</ul>'''
    fmt = table(["Thing", "Style", "Example"], [["Headings", "Sentence case, no full stop on labels", "Three areas to look at first"], ["Dates", "Day month year", "9 September 2026; 9 Sep 2026 in tables"], ["Units", "Space before, abbreviated", "65.5 ha · 860 nm · 43 min"],
        ["Numbers", "Figures for 10 and over; always figures with units", "Four flights; 4 ha"], ["Placeholders", "Square brackets", "[Client name] · [Phone]"], ["Observations", "Two-digit number", "Observation 03"]])
    secs = [("voice", "Voice", ("HCO’s own four lines, from the existing flyer, are the voice. Each becomes a writing rule.", vb)), ("formula", "Writing observations", formula),
            ("words", "Words", words), ("never", "Never", ("Claims that could mislead a client or overstate what HCO does.", never)), ("format", "Formatting", fmt)]
    return page("content.html", "Voice and words", "How HCO sounds: specific, practical and plain. Four rules from the client’s own words, an observation formula and the claims we never make.", "06", "Content", secs,
                meta=("4 voice rules", "Plain English", "UK spelling"))

def tokens():
    TT = T
    css_n = len(set(re.findall(r"(--hco-[a-z0-9-]+)\s*:", open(OUT + "assets/tokens/tokens.css").read())))
    dl = [("assets/tokens/tokens.css", "tokens.css", "CSS custom properties, both themes", "css"), ("assets/tokens/tokens.json", "tokens.json", "Design Tokens format (W3C draft)", "json"),
          ("assets/icons/sprite.svg", "sprite.svg", f"{len(ICONS)} icons as an SVG sprite", "svg"), ("assets/css/groundwork.css", "groundwork.css", "Component styles", "css"),
          ("assets/js/groundwork.js", "groundwork.js", "Pixel figures, tabs, switches, dialogs, toasts", "js"), ("assets/logos/primary-colour.svg", "Logos", "SVG artwork: 18 files in assets/logos", "svg")]
    dlr = "".join(f'<a class="ds-dl" href="{u}" download><span class="ds-dl__ext">{x}</span><div><b>{n}</b><span>{d}</span></div>{ic("download")}</a>' for u, n, d, x in dl)
    use = codeblock('''<link rel="stylesheet" href="assets/tokens/tokens.css">
<link rel="stylesheet" href="assets/css/groundwork.css">
<html data-theme="dark"> … </html>   <!-- or data-theme="light" -->

.my-panel {
  background: var(--hco-surface-raised);
  border: 1px solid var(--hco-border);
  padding: var(--hco-space-5);
  color: var(--hco-text);
}''')
    def colour_rows(prefix, d): return [[f"<code>--hco-{prefix}{k}</code>", f'<span class="sw" style="background:{v}"></span> <span class="gw-num">{v}</span>'] for k, v in d.items()]
    core = table(["Token", "Value"], colour_rows("", TT["core"]) + colour_rows("stone-", TT["stone"]))
    data = table(["Token", "Value"], [[f"<code>--hco-e{i}</code>", f'<span class="sw" style="background:{c}"></span> {c}'] for i, c in enumerate(TT["elevation"])] + [[f"<code>--hco-vigour-{i}</code>", f'<span class="sw" style="background:{c}"></span> {c}'] for i, c in enumerate(TT["vigour"])]
                 + [[f"<code>--hco-terrain-{i}</code>", f'<span class="sw" style="background:{c}"></span> {c}'] for i, c in enumerate(TT["terrain"])] + [[f"<code>--hco-cat-{k}</code>", f'<span class="sw" style="background:{c}"></span> {c}'] for k, c in TT["categorical"].items()]
                 + [[f"<code>--hco-band-{k}</code>", f'<span class="sw" style="background:{b["colour"]}"></span> {b["colour"]} · {b["name"]} {b["centre"]} ± {b["half"]} nm'] for k, b in TT["bands"].items()])
    sem = table(["Token", "Dark", "Light"], [[f"<code>--hco-{k}</code>", f'<span class="sw" style="background:{TT["themes"]["dark"][k]}"></span> {TT["themes"]["dark"][k]}', f'<span class="sw" style="background:{TT["themes"]["light"][k]}"></span> {TT["themes"]["light"][k]}'] for k in TT["themes"]["dark"]])
    other = table(["Token", "Value"], [[f"<code>--hco-space-{k}</code>", f"{v} px"] for k, v in TT["space"].items()] + [[f"<code>--hco-type-{k}</code>", f"{w} {s}px/{l}px · {t}em"] for k, (s, l, t, w) in TT["type"].items()]
                  + [[f"<code>--hco-dur-{k}</code>", v] for k, v in TT["motion"].items()] + [[f"<code>--hco-ease-{k}</code>", f"<code>{v}</code>"] for k, v in TT["ease"].items()] + [[f"<code>--hco-z-{k}</code>", v] for k, v in TT["z"].items()])
    rel = table(["Version", "Date", "Changes"], [["0.1", "October 2026", "First review release: tokens, 82 icons, components, data styles and five templates. Built on the Round 3 identity (pixel HCO, Ridgeline symbol)."]])
    deps = table(["Dependency", "Detail"], [["Typeface", "Instrument Sans, loaded from Google Fonts (SIL Open Font License 1.1). Font files are not included. Final typeface to be confirmed at Stage 2."],
                                            ["Monospace", "The reader’s system monospace font. No download."], ["Browsers", "Current Chrome, Edge, Firefox and Safari. CSS <code>color-mix()</code> and <code>:has()</code> are used with plain fallbacks."], ["Build", "None. Static HTML, CSS and JavaScript."]])
    secs = [("downloads", "Downloads", f'<div class="ds-dls">{dlr}</div>'), ("use", "Using tokens", ("Load the tokens, set the theme on the root element, and refer to semantic tokens in your own CSS.", use)),
            ("colour", "Colour tokens", core), ("semantic", "Semantic tokens", sem), ("data", "Data tokens", data), ("scale", "Space, type, motion and layers", other),
            ("dependencies", "Dependencies", deps), ("release", "Release notes", rel)]
    return page("tokens.html", "Tokens and downloads", f"{css_n} design tokens as CSS and JSON, the icon sprite, component code and logo artwork, with the dependencies this release relies on.", "07", "Resources", secs,
                meta=(f"{css_n} tokens", "CSS · JSON", "v0.1"))
