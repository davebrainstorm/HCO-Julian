"""Read font metadata (not filenames) for every font in the standard font
locations reachable from this environment. Writes JSON + Markdown inventory."""
import json, os, sys, glob
from fontTools.ttLib import TTFont, TTCollection

ROOTS = ["/usr/share/fonts", "/usr/local/share/fonts",
         os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts")]
# macOS locations named in the brief — checked for existence only
MAC = ["~/Library/Fonts", "/Library/Fonts", "/System/Library/Fonts"]
PREMIUM = ["Söhne", "Sohne", "GT America", "Graphik", "Neue Haas", "Suisse",
           "Founders Grotesk", "Tiempos", "Suisse Works"]

def name(tt, nid):
    n = tt["name"].getName(nid, 3, 1, 0x409) or tt["name"].getName(nid, 1, 0, 0)
    return str(n) if n else None

def describe(tt, path, idx=None):
    fam = name(tt, 16) or name(tt, 1)
    sub = name(tt, 17) or name(tt, 2)
    os2 = tt["OS/2"] if "OS/2" in tt else None
    axes = [f"{a.axisTag} {a.minValue:g}-{a.maxValue:g}" for a in tt["fvar"].axes] if "fvar" in tt else []
    feats = sorted({fr.FeatureTag for fr in tt["GSUB"].table.FeatureList.FeatureRecord}) if "GSUB" in tt and tt["GSUB"].table.FeatureList else []
    return {"family": fam, "style": sub, "full_name": name(tt, 4),
            "weight_class": os2.usWeightClass if os2 else None,
            "italic": bool(os2.fsSelection & 1) if os2 else None,
            "variable_axes": axes, "gsub_features": feats,
            "glyphs": len(tt.getGlyphOrder()), "source": path + (f"#{idx}" if idx is not None else "")}

rows = []
for root in ROOTS:
    for p in glob.glob(os.path.join(root, "**", "*"), recursive=True):
        ext = p.lower().rsplit(".", 1)[-1]
        try:
            if ext in ("ttf", "otf"):
                rows.append(describe(TTFont(p, lazy=True), p))
            elif ext in ("ttc", "otc"):
                for i, t in enumerate(TTCollection(p).fonts):
                    rows.append(describe(t, p, i))
            elif ext in ("pfb", "pfa"):
                rows.append({"family": None, "style": None, "full_name": os.path.basename(p),
                             "note": "Type 1 (PostScript) — legacy, not usable for modern PDF/web",
                             "source": p})
        except Exception as e:
            rows.append({"source": p, "error": str(e)})

mac = {m: os.path.isdir(os.path.expanduser(m)) for m in MAC}
hits = [r for r in rows if r.get("family") and any(k.lower() in r["family"].lower() for k in PREMIUM)]
json.dump({"environment": "remote Linux container (Ubuntu 24.04) — not the client/designer's computer",
           "mac_locations_present": mac, "premium_candidates_found": hits, "fonts": rows},
          open("system-font-inventory.json", "w"), indent=2, ensure_ascii=False)
print("mac dirs:", mac)
print("premium hits:", hits)
fams = {}
for r in rows:
    if r.get("family"):
        fams.setdefault(r["family"], []).append(r)
for f, rs in sorted(fams.items()):
    print(f"{f}: " + ", ".join(sorted({'%s(%s)' % (x['style'], x['weight_class']) for x in rs})))
