"""Check every internal href/src in review/hco resolves (files and #anchors)."""
import re, os, html
ROOT = "../../review/hco/"
pages = [f for f in os.listdir(ROOT) if f.endswith(".html")]
ids = {p: set(re.findall(r'\sid="([^"]+)"', open(ROOT + p).read())) for p in pages}
bad = []; n = 0
for p in pages:
    s = open(ROOT + p).read()
    for attr, url in re.findall(r'\s(href|src)="([^"]+)"', s):
        url = html.unescape(url)
        if url.startswith(("http", "mailto:", "data:", "javascript:")): continue
        n += 1
        if url.startswith("#"):
            if url == "#": continue
            if url[1:] not in ids[p] and not url.startswith("#i-"): bad.append((p, url))
            continue
        f, _, a = url.partition("#")
        if not os.path.exists(ROOT + f): bad.append((p, url)); continue
        if a and f.endswith(".html") and a not in ids.get(f, set()): bad.append((p, url))
# sprite ids
sprite = open(ROOT + "assets/icons/sprite.svg").read(); sids = set(re.findall(r'id="(i-[^"]+)"', sprite))
uses = set()
for p in pages: uses |= set(re.findall(r'href="#(i-[a-z0-9-]+)"', open(ROOT + p).read()))
for js in ("assets/js/groundwork.js", "assets/js/fieldmap.js"):
    uses |= set("i-" + m for m in re.findall(r'#i-"\s*\+\s*"?([a-z-]*)', open(ROOT + js).read()) if m)
missing = sorted(u for u in uses if u not in sids)
print(f"{n} internal links checked; broken: {len(bad)}"); [print("  ", b) for b in bad[:40]]
print("icons used:", len(uses), "missing from sprite:", missing)
