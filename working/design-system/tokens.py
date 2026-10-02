"""Groundwork design tokens. Run: python3 tokens.py  → review/hco/assets/tokens/{tokens.json,tokens.css} + build/tokens.json"""
import json, math, os
from colour import *

OUT = "../../review/hco/assets/tokens/"; os.makedirs(OUT, exist_ok=True); os.makedirs("build", exist_ok=True)

# ---------- 1 · core brand ----------
CORE = {"basalt": BASALT, "chalk": CHALK, "moss": MOSS, "sage": SAGE, "lichen": LICHEN, "flag": FLAG}

# ---------- 2 · stone neutrals: Basalt→Chalk in OKLab, brand anchors exact ----------
STEPS = [("975", -0.11), ("950", -0.055), ("900", 0.0), ("850", 0.06), ("800", 0.12), ("700", 0.22), ("600", 0.31),
         ("500", 0.40), ("400", 0.51), ("300", 0.62), ("200", 0.74), ("150", 0.83), ("100", 0.90), ("50", 1.0)]
def ext(t):
    A, B = to_oklab(BASALT), to_oklab(CHALK); return from_oklab(*(A[i] + (B[i] - A[i]) * t for i in range(3)))
STONE = {k: ext(t) for k, t in STEPS}
STONE["900"] = BASALT; STONE["50"] = CHALK
_L, _C, _h = lch(BASALT)
STONE["950"] = oklch(0.205, _C * 0.85, _h); STONE["975"] = oklch(0.165, _C * 0.7, _h)
STONE["25"] = mix(CHALK, "#FFFFFF", 0.55); STONE["0"] = "#FFFFFF"
ORDER = ["0", "25", "50", "100", "150", "200", "300", "400", "500", "600", "700", "800", "850", "900", "950", "975"]

# ---------- 3 · status + observation ----------
STATUS = {
    "dark": {"positive": LICHEN, "caution": oklch(0.84, 0.11, 85), "critical": oklch(0.72, 0.13, 12), "info": oklch(0.78, 0.08, 230), "observation": FLAG},
    "light": {"positive": oklch(0.47, 0.10, 138), "caution": oklch(0.52, 0.105, 70), "critical": oklch(0.505, 0.165, 18), "info": oklch(0.485, 0.095, 238), "observation": oklch(0.53, 0.165, 37)},
}

# ---------- 4 · data ramps ----------
def interp(stops, t):
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b + 1e-9: return mix(ca, cb, 0 if b == a else (t - a) / (b - a))
    return stops[-1][1]
TERRAIN_STOPS = [(0, mix(BASALT, MOSS, .55)), (.30, MOSS), (.50, E[0]), (.66, E[1]), (.80, E[2]), (.91, E[3]), (1.0, E[4])]
TERRAIN = [interp(TERRAIN_STOPS, i / 8) for i in range(9)]
VIGOUR = [oklch(0.36 + 0.54 * (i / 8), 0.048 + 0.045 * math.sin(math.pi * i / 8) + 0.045 * i / 8, 50 + 72 * (i / 8) ** 0.55) for i in range(9)]
def div(i):            # −4 … +4: Heather below the field mean, Lichen above, stone at the mean
    t = abs(i) / 4; L = 0.42 + 0.40 * t
    return oklch(L, 0.012 + 0.095 * t, 322) if i < 0 else oklch(L, 0.012 + (0.12 if i > 0 else 0) * t, 114) if i > 0 else oklch(0.42, 0.012, 180)
RELATIVE = [div(i) for i in range(-4, 5)]
CATEGORICAL = {"lichen": LICHEN, "sky": oklch(0.76, 0.07, 232), "chalk": CHALK, "ochre": oklch(0.70, 0.10, 88), "teal": oklch(0.58, 0.07, 200)}   # max-min ΔE under protan/deutan/tritan: 12.8
BANDS = {   # DJI Mavic 3 Multispectral, manufacturer specification
    "g":   {"name": "Green", "centre": 560, "half": 16, "colour": oklch(0.80, 0.16, 128)},
    "r":   {"name": "Red", "centre": 650, "half": 16, "colour": oklch(0.58, 0.19, 24)},
    "re":  {"name": "Red edge", "centre": 730, "half": 16, "colour": oklch(0.44, 0.14, 16)},
    "nir": {"name": "Near infrared", "centre": 860, "half": 26, "colour": oklch(0.62, 0.02, 300)},
}
MAP = {"water": oklch(0.50, 0.075, 236), "water-edge": oklch(0.68, 0.08, 232), "track": STONE["400"], "boundary": CHALK, "structure": STONE["300"], "canvas": STONE["950"]}

# visible spectrum (Bruton approximation), toned toward Basalt for print/screen restraint
def wl_rgb(w):
    if 380 <= w < 440: r, g, b = -(w - 440) / 60, 0, 1
    elif w < 490: r, g, b = 0, (w - 440) / 50, 1
    elif w < 510: r, g, b = 0, 1, -(w - 510) / 20
    elif w < 580: r, g, b = (w - 510) / 70, 1, 0
    elif w < 645: r, g, b = 1, -(w - 645) / 65, 0
    else: r, g, b = 1, 0, 0
    f = 0.3 + 0.7 * (w - 380) / 40 if w < 420 else 0.3 + 0.7 * (780 - w) / 80 if w > 700 else 1
    return rgb2hex(tuple((max(0, v) * f) ** 0.8 for v in (r, g, b)))
SPECTRUM = [(w, mix(wl_rgb(w), BASALT, 0.12)) for w in range(400, 701, 10)]

# ---------- 5 · semantic themes ----------
S = STONE
THEMES = {
  "dark": {"canvas": S["900"], "surface": S["900"], "surface-raised": S["850"], "surface-sunken": S["950"], "surface-overlay": S["850"], "surface-inverse": S["50"],
           "border": mix(S["900"], S["50"], .14), "border-strong": mix(S["900"], S["50"], .30), "text": S["50"], "text-muted": S["300"], "text-subtle": ext(0.575), "text-inverse": S["900"],
           "accent": LICHEN, "accent-hover": mix(LICHEN, CHALK, .35), "on-accent": S["900"], "signal": LICHEN, "focus": LICHEN, "link": LICHEN, "selection": mix(S["900"], LICHEN, .30),
           "map-canvas": S["950"]},
  "light": {"canvas": S["50"], "surface": S["0"], "surface-raised": S["0"], "surface-sunken": mix(S["50"], S["100"], .22), "surface-overlay": S["0"], "surface-inverse": S["900"],
           "border": mix(S["50"], S["900"], .13), "border-strong": mix(S["50"], S["900"], .32), "text": S["900"], "text-muted": S["600"], "text-subtle": S["500"], "text-inverse": S["50"],
           "accent": S["900"], "accent-hover": MOSS, "on-accent": S["50"], "signal": MOSS, "focus": S["900"], "link": MOSS, "selection": mix(S["50"], LICHEN, .55),
           "map-canvas": S["950"]},
}
for th in ("dark", "light"):
    base = THEMES[th]["canvas"]; tint = 0.16 if th == "dark" else 0.10
    for k, v in STATUS[th].items():
        THEMES[th][f"{k}"] = v
        THEMES[th][f"{k}-tint"] = mix(base if th == "dark" else S["0"], v if th == "dark" else STATUS["dark"][k] if k != "observation" else FLAG, tint)
        THEMES[th][f"{k}-border"] = mix(base, v, 0.45)
    THEMES[th]["observation-text"] = oklch(0.715, 0.15, 40) if th == "dark" else STATUS["light"]["observation"]

# ---------- 6 · type, space, shape, motion ----------
TYPE = {  # size / line-height / tracking / weight
  "display-xl": (112, 112, -0.035, 600), "display": (80, 80, -0.032, 600), "h1": (56, 56, -0.028, 600), "h2": (40, 48, -0.02, 600),
  "h3": (28, 32, -0.014, 600), "h4": (20, 28, -0.008, 600), "body-lg": (20, 32, -0.004, 400), "body": (16, 24, 0, 400),
  "body-sm": (14, 20, 0, 400), "label": (12, 16, 0.11, 600), "caption": (12, 16, 0.01, 400)}
SPACE = {"0": 0, "1": 4, "2": 8, "3": 12, "4": 16, "5": 24, "6": 32, "7": 40, "8": 48, "9": 64, "10": 80, "11": 96, "12": 128, "13": 160}
MOTION = {"instant": "80ms", "quick": "120ms", "base": "200ms", "slow": "320ms", "scan": "1200ms"}
EASE = {"settle": "cubic-bezier(0.2, 0, 0, 1)", "exit": "cubic-bezier(0.4, 0, 1, 1)", "step": "steps(5, end)", "linear": "linear"}
Z = {"base": 0, "raised": 10, "sticky": 100, "nav": 200, "overlay": 300, "modal": 400, "toast": 500, "tooltip": 600}
BREAK = {"sm": 480, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536}

# ---------- emit ----------
def tok(v, t): return {"$value": v, "$type": t}
J = {"color": {"core": {k: tok(v, "color") for k, v in CORE.items()}, "stone": {k: tok(STONE[k], "color") for k in ORDER},
               "elevation": {f"e{i}": tok(c, "color") for i, c in enumerate(E)},
               "terrain": {str(i): tok(c, "color") for i, c in enumerate(TERRAIN)}, "vigour": {str(i): tok(c, "color") for i, c in enumerate(VIGOUR)},
               "relative-vigour": {str(i - 4): tok(c, "color") for i, c in enumerate(RELATIVE)}, "categorical": {k: tok(v, "color") for k, v in CATEGORICAL.items()},
               "band": {k: dict(tok(v["colour"], "color"), **{"$description": f'{v["name"]} {v["centre"]} ± {v["half"]} nm'}) for k, v in BANDS.items()},
               "map": {k: tok(v, "color") for k, v in MAP.items()},
               "theme": {th: {k: tok(v, "color") for k, v in THEMES[th].items()} for th in THEMES}},
     "font": {"family": {"sans": tok("'Instrument Sans', 'Helvetica Neue', Arial, sans-serif", "fontFamily"), "mono": tok("ui-monospace, 'SF Mono', Menlo, Consolas, monospace", "fontFamily")},
              "style": {k: {"size": tok(f"{v[0]}px", "dimension"), "line-height": tok(f"{v[1]}px", "dimension"), "tracking": tok(f"{v[2]}em", "dimension"), "weight": tok(v[3], "fontWeight")} for k, v in TYPE.items()}},
     "space": {k: tok(f"{v}px", "dimension") for k, v in SPACE.items()},
     "shape": {"radius": tok("0px", "dimension"), "notch-sm": tok("4px", "dimension"), "notch-md": tok("8px", "dimension"), "border": tok("1px", "dimension"), "focus": tok("2px", "dimension")},
     "motion": {"duration": {k: tok(v, "duration") for k, v in MOTION.items()}, "easing": {k: tok(v, "cubicBezier" if "bezier" in v else "other") for k, v in EASE.items()}},
     "z": {k: tok(v, "number") for k, v in Z.items()}, "breakpoint": {k: tok(f"{v}px", "dimension") for k, v in BREAK.items()},
     "$description": "Groundwork — HCO design system tokens. Version 0.1, for review. Colours computed in OKLab; contrast per WCAG 2.2."}
json.dump(J, open(OUT + "tokens.json", "w"), indent=2)

css = ["/* Groundwork — HCO design system tokens · v0.1 for review · generated by tokens.py, do not edit by hand */", ":root {"]
for k, v in CORE.items(): css.append(f"  --hco-{k}: {v};")
for k in ORDER: css.append(f"  --hco-stone-{k}: {STONE[k]};")
for i, c in enumerate(E): css.append(f"  --hco-e{i}: {c};")
for i, c in enumerate(TERRAIN): css.append(f"  --hco-terrain-{i}: {c};")
for i, c in enumerate(VIGOUR): css.append(f"  --hco-vigour-{i}: {c};")
for i, c in enumerate(RELATIVE): css.append(f"  --hco-rel-{'m' if i < 4 else 'p' if i > 4 else ''}{abs(i - 4)}: {c};")
for k, v in CATEGORICAL.items(): css.append(f"  --hco-cat-{k}: {v};")
for k, v in BANDS.items(): css.append(f"  --hco-band-{k}: {v['colour']};")
for k, v in MAP.items(): css.append(f"  --hco-map-{k}: {v};")
css.append("  --hco-font-sans: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif;\n  --hco-font-mono: ui-monospace, 'SF Mono', Menlo, Consolas, monospace;")
for k, (sz, lh, tr, w) in TYPE.items(): css.append(f"  --hco-type-{k}: {w} {sz}px/{lh}px var(--hco-font-sans); --hco-track-{k}: {tr}em;")
for k, v in SPACE.items(): css.append(f"  --hco-space-{k}: {v}px;")
css.append("  --hco-radius: 0px; --hco-notch-sm: 4px; --hco-notch-md: 8px; --hco-border-width: 1px; --hco-focus-width: 2px;")
for k, v in MOTION.items(): css.append(f"  --hco-dur-{k}: {v};")
for k, v in EASE.items(): css.append(f"  --hco-ease-{k}: {v};")
for k, v in Z.items(): css.append(f"  --hco-z-{k}: {v};")
css.append("}")
for th, sel in (("dark", ":root, [data-theme=\"dark\"]"), ("light", "[data-theme=\"light\"]")):
    css.append(f"{sel} {{\n  color-scheme: {th};")
    for k, v in THEMES[th].items(): css.append(f"  --hco-{k}: {v};")
    css.append(f"  --hco-shadow-overlay: {'0 24px 64px rgba(2, 10, 10, .48), 0 2px 6px rgba(2, 10, 10, .32)' if th == 'dark' else '0 24px 64px rgba(14, 36, 35, .16), 0 2px 6px rgba(14, 36, 35, .10)'};")
    css.append("}")
css.append("/* component-level aliases */")
css.append(':root, [data-theme="dark"] { --hco-field-bg: var(--hco-stone-950); --hco-on-status: var(--hco-stone-900); }')
css.append('[data-theme="light"] { --hco-field-bg: var(--hco-stone-0); --hco-on-status: var(--hco-stone-50); }')
open(OUT + "tokens.css", "w").write("\n".join(css) + "\n")

# ---------- report for the documentation builder ----------
def C(a, b): return round(contrast(a, b), 2)
report = {"core": CORE, "stone": {k: STONE[k] for k in ORDER}, "status": STATUS, "themes": THEMES, "terrain": TERRAIN, "vigour": VIGOUR, "relative": RELATIVE,
          "categorical": CATEGORICAL, "bands": BANDS, "map": MAP, "spectrum": SPECTRUM, "type": TYPE, "space": SPACE, "motion": MOTION, "ease": EASE, "z": Z, "break": BREAK, "elevation": E}
checks = []
for th in ("dark", "light"):
    T = THEMES[th]
    for fg in ("text", "text-muted", "text-subtle", "link", "positive", "caution", "critical", "info", "observation-text"):
        for bg in ("canvas", "surface", "surface-raised", "surface-sunken"):
            checks.append({"theme": th, "fg": fg, "bg": bg, "ratio": C(T[fg], T[bg])})
    checks.append({"theme": th, "fg": "on-accent", "bg": "accent", "ratio": C(T["on-accent"], T["accent"])})
    checks.append({"theme": th, "fg": "focus", "bg": "canvas", "ratio": C(T["focus"], T["canvas"])})
    for k in ("positive", "caution", "critical", "info"):
        checks.append({"theme": th, "fg": k, "bg": f"{k}-tint", "ratio": C(T[k], T[f"{k}-tint"])})
report["checks"] = checks
report["cvd"] = {kind: {"terrain": [simulate(c, kind) for c in TERRAIN], "vigour": [simulate(c, kind) for c in VIGOUR], "relative": [simulate(c, kind) for c in RELATIVE],
                        "categorical": [simulate(c, kind) for c in CATEGORICAL.values()], "brand": [simulate(c, kind) for c in (LICHEN, FLAG, SAGE, MOSS)]}
                 for kind in ("protanopia", "deuteranopia", "tritanopia", "greyscale")}
report["L"] = {"terrain": [round(to_oklab(c)[0], 3) for c in TERRAIN], "vigour": [round(to_oklab(c)[0], 3) for c in VIGOUR], "relative": [round(to_oklab(c)[0], 3) for c in RELATIVE]}
# minimum pairwise ΔE of categorical colours under each simulation
cats = list(CATEGORICAL.values()); mins = {}
for kind in ("none", "protanopia", "deuteranopia", "tritanopia"):
    cs = cats if kind == "none" else [simulate(c, kind) for c in cats]
    mins[kind] = round(min(de(a, b) for i, a in enumerate(cs) for b in cs[i + 1:]), 1)
report["cat_min_de"] = mins
json.dump(report, open("build/tokens.json", "w"), indent=1)

if __name__ == "__main__":
    print("stone", {k: STONE[k] for k in ORDER})
    print("status", STATUS)
    print("L terrain", report["L"]["terrain"]); print("L vigour", report["L"]["vigour"], VIGOUR); print("L relative", report["L"]["relative"], RELATIVE)
    print("categorical min ΔE", mins)
    bad = [c for c in checks if c["fg"] not in ("text-subtle",) and c["ratio"] < 4.5 and c["fg"] not in ("focus",)]
    print("below 4.5:", [(c["theme"], c["fg"], c["bg"], c["ratio"]) for c in bad])
    print("focus", [(c["theme"], c["ratio"]) for c in checks if c["fg"] == "focus"], "on-accent", [(c["theme"], c["ratio"]) for c in checks if c["fg"] == "on-accent"])
    print("subtle", [(c["theme"], c["bg"], c["ratio"]) for c in checks if c["fg"] == "text-subtle"])
