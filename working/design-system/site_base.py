"""Groundwork site builder: shared shell and helpers. Pages register themselves in PAGES."""
import html, json, re, os, sys
sys.path.insert(0, "../round-3"); sys.path.insert(0, "../geometry")
OUT = "../../review/hco/"
T = json.load(open("build/tokens.json"))
ICONS = json.load(open("build/icons.json"))
SPRITE = open(OUT + "assets/icons/sprite.svg").read().replace('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">', '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">')
FIELD = json.load(open(OUT + "assets/data/field.json"))
VERSION = "0.1"
def e(s): return html.escape(str(s), quote=True)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def d(iso, long=False):
    y, m, dd = (int(x) for x in iso.split("-"))
    full = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{dd} {(full if long else MONTHS)[m - 1]} {y}"

# ---------- logo (inline, theme-aware: colour symbol on dark, one colour on light) ----------
from mark import symbol_rects, M, CAP
from pixel import wordmark as _pwm, FINAL
from glyphs import svg_d
_WM = svg_d(_pwm(**FINAL)[0], cap=CAP)
def logo(h=20, cls="hco-logo", wordmark=True):
    g = 0.10 * M; cells = []
    from palette import E
    for i, hh in enumerate([0, 1, 1, 2, 3, 4, 3, 2]):
        cells.append(f'<rect class="s" style="--c:{E[hh]}" x="{i * M + g / 2:.0f}" y="{(4 - hh) * M + g / 2:.0f}" width="{M - g:.0f}" height="{M - g:.0f}"/>')
    W = 4800 if wordmark else 1600
    wm = f'<path transform="translate({9 * M},0)" d="{_WM}" fill="currentColor"/>' if wordmark else ""
    return f'<svg class="{cls}" viewBox="0 0 {W} 1000" style="height:{h}px;width:auto" role="img" aria-label="HCO"><g>{"".join(cells)}</g>{wm}</svg>'

def ic(name, cls="", size=None, label=None):
    st = f' style="width:{size}px;height:{size}px"' if size else ""
    aria = f' role="img" aria-label="{e(label)}"' if label else ' aria-hidden="true"'
    return f'<svg class="gw-icon {cls}"{st}{aria}><use href="#i-{name}"/></svg>'
def px(v, h=None, cls=""):
    st = f' style="height:{h}px"' if h else ""
    return f'<span class="gw-px {cls}" data-px="{e(v)}"{st}></span>'
def trace(heights=(0, 1, 1, 2, 3, 4, 3, 2), u=10, cls="", style=""):
    n = len(heights); rows = max(heights) + 1
    y = lambda h: (rows - 1 - h) * u + u / 2
    pts = [(0, y(heights[0]))] + [(i * u + u / 2, y(h)) for i, h in enumerate(heights)] + [(n * u, y(heights[-1]))]
    d = "".join(("L" if i else "M") + f"{a:g} {b:g}" for i, (a, b) in enumerate(pts))
    return f'<svg class="{cls}" style="{style}" viewBox="0 {-u / 2:g} {n * u} {rows * u + u:g}" fill="none" stroke="currentColor" stroke-width="{u}" stroke-linejoin="miter" stroke-miterlimit="10" aria-hidden="true"><path d="{d}"/></svg>'

# ---------- code formatting ----------
def code(src, lang="html"):
    s = html.escape(src.strip("\n"))
    if lang == "html":
        s = re.sub(r"(&lt;/?)([a-z0-9-]+)", r'\1<span class="t">\2</span>', s)
        s = re.sub(r'([a-z-]+)=(&quot;.*?&quot;)', r'<span class="a">\1</span>=<span class="s">\2</span>', s)
    elif lang == "css":
        s = re.sub(r"(--[a-z0-9-]+)", r'<span class="a">\1</span>', s)
    return s
def codeblock(src, lang="html"):
    return f'<div class="ds-code-block"><button class="ds-copy" data-copy>Copy</button><pre class="ds-code"><code>{code(src, lang)}</code></pre></div>'
def spec(label, stage, src=None, cap=None, stage_cls="", lang="html", grid=True, theme=True, style=""):
    acts = []
    if grid: acts.append(f'<button type="button" data-spec-grid aria-pressed="false" title="Show the 8 px grid">{ic("grid")}</button>')
    if theme: acts.append(f'<button type="button" data-spec-theme aria-pressed="false" title="Switch theme for this example">{ic("moon")}</button>')
    if src: acts.append(f'<button type="button" data-spec-code aria-pressed="false" title="Show code">{ic("list")}</button>')
    pre = f'<pre class="ds-code" hidden><button class="ds-copy" data-copy>Copy</button><code>{code(src, lang)}</code></pre>' if src else ""
    capb = f'<div class="ds-spec__cap">{cap}</div>' if cap else ""
    return (f'<figure class="ds-spec" data-grid="off"><figcaption class="ds-spec__bar"><span class="gw-label">{e(label)}</span><span class="ds-spec__actions">{"".join(acts)}</span></figcaption>'
            f'<div class="ds-spec__stage {stage_cls}" style="{style}">{stage}</div>{pre}{capb}</figure>')
def sec(id_, title, body, lead=None):
    ld = f'<p class="ds-lead">{lead}</p>' if lead else ""
    return f'<section class="ds-sec"><h2 id="{id_}">{e(title)} <a href="#{id_}" aria-label="Link to {e(title)}">#</a></h2>{ld}{body}</section>'
def note(text, icon="info"): return f'<div class="ds-note">{ic(icon)}<div>{text}</div></div>'
def dodont(do, dont):
    return f'<div class="ds-dodont"><div class="ds-do"><span class="gw-label">Do</span><p>{do}</p></div><div class="ds-dont"><span class="gw-label">Don’t</span><p>{dont}</p></div></div>'
def table(head, rows, cls="ds-tt"):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div style="overflow-x:auto"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

# ---------- navigation ----------
NAV = [("Start", "01", [("index.html", "Overview"), ("principles.html", "Principles")]),
       ("Foundations", "02", [("brand.html", "Brand"), ("colour.html", "Colour"), ("typography.html", "Typography"), ("layout.html", "Layout and space"), ("motion.html", "Motion"), ("icons.html", "Icons")]),
       ("Data", "03", [("data.html", "Maps and charts"), ("capture.html", "Capture and bands")]),
       ("Components", "04", [("components.html", "All components")]),
       ("Templates", "05", [("portal.html", "Client portal"), ("report.html", "Field report"), ("app.html", "Field app"), ("website.html", "Website"), ("email.html", "Email")]),
       ("Content", "06", [("content.html", "Voice and words")]),
       ("Resources", "07", [("tokens.html", "Tokens and downloads")])]
TEMPLATES = {"portal.html", "report.html", "app.html", "website.html", "email.html"}
PAGES = {}       # file -> dict(title, sections=[(id,title)], keywords)
INDEX = []
def side(cur):
    out = []
    for g, n, items in NAV:
        links = "".join(f'<a href="{u}"{" aria-current=page" if u == cur else ""}>{e(t)}{"<span class=ds-side__tag>Template</span>" if u in TEMPLATES else ""}</a>' for u, t in items)
        out.append(f'<div class="ds-side__group"><div class="ds-side__label">{px(n, 10)}<span>{e(g)}</span></div>{links}</div>')
    return f'<nav class="ds-side" aria-label="Groundwork">{"".join(out)}</nav>'
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wdth,wght@0,75..100,400..700;1,75..100,400..700&display=swap">'
def THEME_BOOT(key="gw-theme"):
    return "<script>try{var t=localStorage.getItem('" + key + "');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"
def head(title, desc, css="docs.css", extra="", key="gw-theme"):
    return (f'<!doctype html><html lang="en-IE" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(title)} · Groundwork · HCO</title><meta name="description" content="{e(desc)}"><meta name="robots" content="noindex, nofollow">'
            f'<meta name="theme-color" content="#0E2423"><link rel="icon" href="assets/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="assets/img/favicon-180.png">'
            f'{FONT}<link rel="stylesheet" href="assets/css/{css}">{extra}{THEME_BOOT(key)}</head>')
def top():
    return (f'<header class="ds-top"><button class="gw-btn gw-btn--ghost gw-btn--icon ds-menu" aria-label="Open navigation" aria-expanded="false">{ic("menu")}</button>'
            f'<a class="ds-brand" href="index.html" aria-label="Groundwork home">{logo(20)}<span class="ds-brand__rule"></span><span class="ds-brand__sys">Groundwork</span></a>'
            f'<span class="ds-ver">v{VERSION} · For review</span>'
            f'<div class="ds-top__right"><button class="ds-search" data-search aria-label="Search the system">{ic("search")}<span>Search the system</span><kbd>⌘K</kbd></button>'
            f'<button class="gw-btn gw-btn--ghost gw-btn--icon" data-theme-toggle aria-label="Switch light or dark theme">{ic("sun", "ds-ic-sun")}{ic("moon", "ds-ic-moon")}</button>'
            f'<a class="gw-btn gw-btn--secondary gw-btn--s ds-hide-s" href="tokens.html">{ic("download")}Tokens</a></div></header>')
FIND = (f'<div class="ds-find" role="dialog" aria-modal="true" aria-label="Search"><div class="ds-find__box"><div class="ds-find__in">{ic("search")}<input type="search" placeholder="Search pages, components and tokens" aria-label="Search"><kbd class="gw-mono" style="font-size:11px;color:var(--hco-text-subtle)">Esc</kbd></div>'
        f'<ul class="ds-find__list"></ul></div></div>')
def foot():
    return (f'<footer class="ds-foot"><span>Groundwork v{VERSION} · HCO design system · Working draft for review, not for public release.</span>'
            f'<span>Illustrative data throughout. No client, property or result is depicted. <a href="tokens.html">Tokens and downloads</a></span></footer>')
def scripts(extra=()):
    s = [f"<script>window.GW_INDEX={json.dumps(INDEX, separators=(',', ':'))};</script>", '<script src="assets/js/groundwork.js" data-sprite=""></script>', '<script src="assets/js/docs.js"></script>']
    for x in extra: s.append(f'<script src="{x}"></script>')
    return "".join(s)
def page(fname, title, lead, eyebrow_n, eyebrow, sections, desc=None, meta=(), extra_js=(), hero_extra="", hero_cls="", show_trace=True):
    """sections: list of (id, title, html) — h2 sections in order."""
    PAGES[fname] = dict(title=title, sections=[(i, t) for i, t, _ in sections])
    body = "".join(sec(i, t, h) if not isinstance(h, tuple) else sec(i, t, h[1], lead=h[0]) for i, t, h in sections)
    chips = "".join(f'<span class="gw-tag gw-tag--plain">{e(m)}</span>' for m in meta)
    tr = trace(u=10, cls="ds-hero__trace") if show_trace else ""
    html_ = (head(title, desc or lead) + f'<body>{SPRITE}<a class="ds-skip" href="#main">Skip to content</a>{top()}<div class="ds-shell">{side(fname)}<main class="ds-main" id="main">'
             f'<header class="ds-hero {hero_cls}">{tr}<div class="ds-hero__eyebrow">{px(eyebrow_n, 20)}<span>{e(eyebrow)}</span></div><h1>{title}</h1><p class="ds-hero__lead">{lead}</p>'
             f'{"<div class=ds-hero__meta>" + chips + "</div>" if chips else ""}{hero_extra}</header>'
             f'<div class="ds-body"><div class="ds-content">{body}</div><aside class="ds-toc" aria-label="On this page"><div class="ds-toc__label">On this page</div><nav></nav></aside></div>{foot()}</main></div>'
             f'{FIND}<div class="gw-toast-region" aria-live="polite"></div>{scripts(extra_js)}</body></html>')
    return html_
def register_index():
    INDEX.clear()
    group_of = {u: g for g, _, items in NAV for u, _ in items}
    for f, p in PAGES.items():
        INDEX.append(dict(t=re.sub("<.*?>", "", p["title"]), s=group_of.get(f, ""), u=f))
        for i, t in p["sections"]: INDEX.append(dict(t=t, s=re.sub("<.*?>", "", p["title"]), u=f"{f}#{i}"))
