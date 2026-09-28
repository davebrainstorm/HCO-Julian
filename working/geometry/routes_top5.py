"""Artwork for the two additional concepts in the top-five set:
r4 Ground Truth (ground-control target) and r5 Horizon Line (evolution).
Outlined SVG only; written next to the Stage-1 marks in ../concepts/marks/."""
from routes import svg, save, F, INS, shape
INK, WHITE = "#111111", "#FFFFFF"
import json

SERIF = F + "sourceserif4/SourceSerif4[opsz,wght].ttf"

def ground_truth(S=1000):
    h = S / 2
    return f'M0 0H{h}V{h}H0Z M{h} {h}H{S}V{S}H{h}Z'

if __name__ == "__main__":
    meta = {}
    # ---------------------------------------------------------- r4 Ground Truth
    gt = ground_truth()
    save("r4-symbol-black", svg(1000, 1000, f'<path d="{gt}" fill="{INK}"/>'))
    save("r4-symbol-white", svg(1000, 1000, f'<path d="{gt}" fill="{WHITE}"/>'))
    # HCO cap height 640 hung from the symbol top; descriptor on the symbol baseline
    _, _, _, cap100 = shape(INS, "H", 100, {"wght": 600, "wdth": 100})
    fsH = 640 / (cap100 / 100)
    wm, wmw, _, _ = shape(INS, "HCO", fsH, {"wght": 600, "wdth": 100}, tracking=0.012)
    ds, dsw, _, _ = shape(INS, "High Country Observations", 150, {"wght": 500, "wdth": 100})
    x = 1000 + 200
    body = (f'<path d="{gt}" fill="{{c}}"/>'
            f'<g transform="translate({x},640)"><path d="{wm}" fill="{{c}}"/></g>'
            f'<g transform="translate({x + 6},1000)"><path d="{ds}" fill="{{c}}"/></g>')
    W4 = x + max(wmw, dsw)
    save("r4-lockup-black", svg(W4, 1040, body.format(c=INK)))
    save("r4-lockup-white", svg(W4, 1040, body.format(c=WHITE)))
    meta["r4"] = {"lock_w": W4}

    # ---------------------------------------------------------- r5 Horizon Line
    capS = shape(SERIF, "H", 100, {"wght": 620, "opsz": 60})[3] / 100
    fs = 1000 / capS
    wm, wmw, _, _ = shape(SERIF, "HCO", fs, {"wght": 620, "opsz": 60}, tracking=0.03)
    line_t, gap = 58, 210
    base = line_t + gap + 1000          # HCO baseline (y-down)
    # descriptor: two lines of capitals under the extended horizon, standing on HCO's baseline
    dfs = 225
    d1, d1w, _, dcap = shape(SERIF, "HIGH COUNTRY", dfs, {"wght": 560, "opsz": 20}, tracking=0.07)
    d2, d2w, _, _ = shape(SERIF, "OBSERVATIONS", dfs, {"wght": 560, "opsz": 20}, tracking=0.07)
    xd = wmw + 190
    W5 = xd + max(d1w, d2w)
    body = (f'<rect x="0" y="0" width="{W5:.1f}" height="{line_t}" fill="{{c}}"/>'
            f'<g transform="translate(0,{base})"><path d="{wm}" fill="{{c}}"/></g>'
            f'<g transform="translate({xd:.1f},{base - dfs * 1.3:.1f})"><path d="{d1}" fill="{{c}}"/></g>'
            f'<g transform="translate({xd:.1f},{base})"><path d="{d2}" fill="{{c}}"/></g>')
    save("r5-lockup-black", svg(W5, base + 20, body.format(c=INK)))
    # name only (no line) for layouts where the horizon runs to the format edge
    body_n = body.split("/>", 1)[1]
    save("r5-name-black", svg(W5, base + 20, body_n.format(c=INK)))
    save("r5-lockup-white", svg(W5, base + 20, body.format(c=WHITE)))
    # wordmark only (line + HCO) and compact (line + H)
    bodyw = (f'<rect x="0" y="0" width="{wmw * 1.0:.1f}" height="{line_t}" fill="{{c}}"/>'
             f'<g transform="translate(0,{base})"><path d="{wm}" fill="{{c}}"/></g>')
    save("r5-wordmark-black", svg(wmw, base + 20, bodyw.format(c=INK)))
    h, hw, _, _ = shape(SERIF, "H", fs, {"wght": 660, "opsz": 60})
    lt = 90
    bodyc = (f'<rect x="0" y="0" width="{hw:.1f}" height="{lt}" fill="{{c}}"/>'
             f'<g transform="translate(0,{lt + 170 + 1000})"><path d="{h}" fill="{{c}}"/></g>')
    save("r5-compact-black", svg(hw, lt + 170 + 1000 + 10, bodyc.format(c=INK)))
    save("r5-compact-white", svg(hw, lt + 170 + 1000 + 10, bodyc.format(c=WHITE)))
    meta["r5"] = {"lock_w": W5, "word_w": wmw}
    json.dump(meta, open("../concepts/marks/meta-top5.json", "w"), indent=1)
    print(meta)
