"""Boards 18–24: report, stationery, website, field kit, observation marker, posters, decisions."""
import json, numpy as np
from base import *
SEC = json.load(open("assets/section.json"))
SH = "box-shadow:0 1px 2px rgba(14,36,35,.08),0 12px 32px rgba(14,36,35,.10)"
def page(x, y, w, h, inner, bg=CHALK, extra=""):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};overflow:hidden;{SH};{extra}">{inner}</div>'
def rel(x, y, inner, w=None, h=None, style=""):
    return f'<div class="abs" style="left:{x}px;top:{y}px;{f"width:{w}px;" if w else ""}{f"height:{h}px;" if h else ""}{style}">{inner}</div>'
def svgbox(w, h, inner):
    return f'<svg class="abs" style="left:0;top:0;overflow:visible" width="{w}" height="{h}">{inner}</svg>'
def profile_px(x0, y0, w, rows, p, mono=None, light=False):
    """Section A–A with the 2-px pen. Returns rects in local coords; baseline at y0."""
    prof = np.array(SEC["profile"]); cols = int(w // p)
    lv = np.round(np.interp(np.linspace(0, 95, cols), np.arange(96), prof) * (rows - 2)).astype(int); o = []
    for i, l in enumerate(lv):
        lo = l - 1
        for nb in (i - 1, i + 1):
            if 0 <= nb < cols and lv[nb] < lo: lo = lv[nb]
        for r in range(lo, l + 1):
            c = mono or E[min(4, max(0, r * 5 // rows))]
            o.append(rect(x0 + i * p, y0 - (r + 1) * p, p, p, c))
    return "".join(o)
def flagmark(x, y, n, s=32):
    return rect(x, y, s, s, FLAG) + pnum(n, x + s * 0.18, y + s * 0.31, s * 0.375, BASALT)

def b18(D):
    W, Hh = 464, 656
    cover = (crop("assets/ridges-tall.png", 1200, 1680, 0, 0, W / 1200, 0, 96, W, Hh - 96)
        + rel(32, 32, mkw("primary-colour", 168))
        + rel(32, 136, f'<div class="lab ac">Field observations report</div><div style="font-weight:600;font-size:32px;line-height:40px;letter-spacing:-.02em;color:{CHALK};margin-top:16px">[Property name]</div>'
              f'<div class="s" style="color:{INK2};margin-top:8px">[Season · year]</div>', w=W - 64)
        + rel(0, Hh - 64, f'<div style="display:flex;justify-content:space-between;padding:24px 32px 0" class="cap"><span style="color:{INK2}">Prepared for [Client name]</span><span style="color:{INK2}">[Date]</span></div>', w=W, h=64, style=f"background:{BASALT}"))
    mt = 24; cs = 400 / mt; flags = [("01", 5, 17), ("02", 14, 9), ("03", 19, 15)]
    left = (rel(32, 32, f'<div class="lab" style="color:{STONE}">HCO · Field observations · [Property]</div>', w=400)
        + svgbox(W, Hh, pnum("02", 32, 72, 40, BASALT) + "".join(flagmark(32 + i * cs, 200 + j * cs, n, cs * 2) for n, i, j in flags)
                 + pnum("06", W - 32, Hh - 44, 12, STONE, "end"))
        + rel(104, 80, f'<div class="lab">Observations</div>', w=300)
        + rel(32, 128, '<div class="h3" style="font-size:22px">Three areas to look at first.</div>', w=400)
        + rel(32, 200, img("assets/map-tile.png", 0, 0, 400, 400, cls="pix"), w=400, h=400)
        + rel(32, 616, f'<p class="cap" style="color:{STONE}">Map 1 · Illustrative terrain model, 24 × 24 cells. Not survey data.</p>', w=400))
    left = left.replace(svgbox(W, Hh, ""), "")
    left = (rel(32, 32, f'<div class="lab" style="color:{STONE}">HCO · Field observations · [Property]</div>', w=400)
        + rel(32, 200, img("assets/map-tile.png", 0, 0, 400, 400, cls="pix"), w=400, h=400)
        + svgbox(W, Hh, pnum("02", 32, 72, 40, BASALT) + "".join(flagmark(32 + i * cs, 200 + j * cs, n, cs * 2) for n, i, j in flags) + pnum("06", W - 32, Hh - 44, 12, STONE, "end"))
        + rel(104, 82, f'<div class="lab">Observations</div>', w=300)
        + rel(32, 136, '<div style="font-weight:600;font-size:22px;line-height:32px;letter-spacing:-.01em">Three areas to look at first.</div>', w=400)
        + rel(32, 616, f'<p class="cap" style="color:{STONE}">Map 1 · Illustrative terrain model, 24 × 24 cells. Not survey data.</p>', w=400))
    obs = [("01", "Standing water after rain", "Lower boundary. Check the drainage line before the next irrigation cycle."),
           ("02", "Uneven growth, north-east block", "Patchy canopy on the upper slope. Scout on foot to confirm the cause."),
           ("03", "Gap in the fence line", "At the eastern gate. Repair before stock are moved.")]
    items = "".join(f'<div style="display:flex;gap:16px;padding:16px 0;border-top:1px solid rgba(14,36,35,.14)"><svg width="32" height="32" style="flex:none">{flagmark(0, 0, n)}</svg>'
                    f'<div><div style="font-weight:600;font-size:16px;line-height:24px">{t}</div><p class="s" style="color:{STONE}">{d}</p></div></div>' for n, t, d in obs)
    right = (rel(32, 32, f'<div class="lab" style="color:{STONE}">Section A–A</div>', w=400)
        + svgbox(W, Hh, profile_px(32, 232, 400, 18, 8, mono=MOSS) + ln(32, 236, 432, 236, BASALT, 1, None, .25) + pnum("07", W - 32, Hh - 44, 12, STONE, "end"))
        + rel(32, 264, items, w=400)
        + rel(32, Hh - 48, f'<span class="cap" style="color:{STONE}">Sample content for layout only</span>', w=300))
    body = (head("Applications", "Field report: cover and spread.", cs=8, n="12")
        + at(X(9), Y(0) + 8, f'<p class="cap mu">Sample content for layout only. The map, profile and observations are illustrative; no client, property or result is depicted.</p>', w=WD(3))
        + page(X(0), Y(1), W, Hh, cover, BASALT)
        + page(X(4), Y(1), W, Hh, left) + page(X(4) + W, Y(1), W, Hh, right)
        + at(X(4) + W - 1, Y(1), "", w=2, h=Hh, style="background:linear-gradient(90deg,rgba(14,36,35,.10),rgba(14,36,35,0))"))
    D.add(18, body, "Applications", "st")

def bars(x, y, w, n, gap=16, h=6, last=0.6):
    return "".join(rect(x, y + i * gap, w * (last if i == n - 1 else 1), h, BASALT, op=.10) for i in range(n))
def b19(D):
    W, Hh = 464, 656
    letter = (rel(40, 40, mkw("primary-basalt", 168))
        + rel(W - 40 - 160, 44, f'<p class="cap" style="color:{STONE};text-align:right">[Address line 1]<br>[Address line 2]</p>', w=160)
        + rel(40, 168, f'<p class="cap" style="color:{STONE}">[Date]</p><p class="cap" style="margin-top:16px">[Recipient name]<br>[Organisation]</p><p class="s" style="margin-top:32px">Dear [Name],</p>', w=300)
        + svgbox(W, Hh, bars(40, 312, 384, 6) + bars(40, 424, 384, 5) + bars(40, 520, 384, 3, last=.4)
                 + profile_px(0, Hh - 40, W, 10, 4, mono=SAGE))
        + rel(40, Hh - 32, f'<p class="cap" style="color:{STONE}">[Phone] · [Email] · [Website]</p>', w=384))
    cw, ch = 464, 300
    front = rel(40, ch - 40 - 240 * 1237 / 4800, mkw("primary-colour", 240))
    back = (svgbox(cw, ch, sym(40, 40, 6, mono=BASALT))
        + rel(40, 120, f'<div style="font-weight:600;font-size:24px;line-height:32px;letter-spacing:-.01em">[Name]</div><div class="s" style="color:{STONE}">[Role]</div>', w=380)
        + rel(40, ch - 40 - 64, f'<p class="cap" style="line-height:20px">[Phone]<br>[Email]<br>[Website]</p>', w=300)
        + rel(cw - 40 - 200, ch - 40 - 16, f'<div class="lab" style="color:{STONE};text-align:right">High Country Observations</div>', w=200))
    sig_w, sig_h = WD(8), 312
    sig = (rel(0, 0, f'<div style="height:40px;background:#E6E8E2;display:flex;align-items:center;gap:8px;padding:0 16px">'
               + "".join(f'<span style="width:10px;height:10px;border-radius:5px;background:{c}"></span>' for c in ("#C8CCC6", "#C8CCC6", "#C8CCC6")) + '<span class="cap" style="margin-left:16px;color:' + STONE + '">New message</span></div>', w=sig_w)
        + rel(32, 56, f'<p class="cap" style="color:{STONE}">To<span style="display:inline-block;width:8px"></span>[Recipient]</p><div style="border-top:1px solid rgba(14,36,35,.10);margin-top:8px"></div><p class="cap" style="color:{STONE};margin-top:8px">Subject<span style="display:inline-block;width:8px"></span>[Subject]</p>', w=sig_w - 64)
        + svgbox(sig_w, sig_h, bars(32, 128, 520, 2, last=.5))
        + rel(32, 176, f'<div style="border-top:1px solid rgba(14,36,35,.14);padding-top:16px;display:flex;gap:32px;align-items:flex-start">'
              f'<div>{mkw("compact-basalt", 120)}</div><div><div style="font-weight:600;font-size:14px;line-height:24px">[Name]</div><div class="cap" style="color:{STONE}">[Role] · High Country Observations</div>'
              f'<div class="cap" style="color:{STONE};margin-top:8px">[Phone] · [Email] · [Website]</div></div></div>', w=sig_w - 64))
    body = (head("Applications", "Stationery: letter, cards, signature.", cs=8, n="12")
        + at(X(9), Y(0) + 8, '<p class="cap mu">Placeholders in brackets. No contact details are invented; real details are added once confirmed.</p>', w=WD(3))
        + page(X(0), Y(1), W, Hh, letter)
        + page(X(4), Y(1), cw, ch, front, BASALT) + page(X(8), Y(1), cw, ch, back)
        + at(X(4), Y(1) + ch + 12, '<span class="cap mu">Card · 85 × 55 mm · front</span>') + at(X(8), Y(1) + ch + 12, '<span class="cap mu">Back</span>')
        + page(X(4), Y(1) + Hh - sig_h, sig_w, sig_h, sig, "#FFFFFF"))
    D.add(19, body, "Applications", "st")

def btn(t, bg=LICHEN, fg=BASALT, pad="12px 20px"):
    return f'<span style="display:inline-block;background:{bg};color:{fg};font-weight:600;font-size:14px;line-height:24px;padding:{pad}">{t}</span>'
def b20(D):
    W, Hh = WD(9), 600; top = 32
    vals = ["We actually show up.", "Your operation comes first.", "Practical. Not theory.", "Start with the problem."]
    nav = "".join(f'<span class="s" style="color:{CHALK}">{t}</span>' for t in ("Approach", "Field intelligence", "Business &amp; operations", "About"))
    site = (img("assets/bg-ridges.png", 300, top - 40, 960, 600)
        + rel(0, 0, f'<div style="height:{top}px;background:#081716;display:flex;align-items:center;gap:8px;padding:0 16px">'
              + "".join('<span style="width:10px;height:10px;border-radius:5px;background:#2E4B43"></span>' for _ in range(3))
              + f'<span class="cap" style="margin-left:24px;background:#132A28;color:{INK2};padding:2px 16px">[domain]</span></div>', w=W)
        + rel(40, top + 28, mkw("compact-colour", 120))
        + rel(W - 40 - 640, top + 24, f'<div style="display:flex;gap:32px;align-items:center;justify-content:flex-end">{nav}{btn("Contact", pad="4px 16px")}</div>', w=640)
        + rel(40, top + 128, f'<div class="lab ac">Agriculture · Ranching · Rural business · Field intelligence</div>'
              f'<div style="font-weight:600;font-size:64px;line-height:64px;letter-spacing:-.03em;color:{CHALK};margin-top:24px">Understand systems.<br>Protect people.</div>'
              f'<p class="b" style="color:{INK2};margin-top:24px;max-width:440px">HCO helps farmers, ranchers, and agricultural businesses solve business, regulatory, and field problems.</p>'
              f'<div style="margin-top:32px;display:flex;gap:24px;align-items:center">{btn("Start with the problem")}<span class="s" style="color:{CHALK}">How we work →</span></div>', w=620)
        + rel(0, Hh - 96, '<div style="display:grid;grid-template-columns:repeat(4,1fr);height:96px;background:' + BASALT + ';border-top:1px solid rgba(244,245,239,.14)">'
              + "".join(f'<div style="padding:20px 24px;border-left:{"0" if i == 0 else "1px solid rgba(244,245,239,.14)"}"><svg width="40" height="16" style="display:block">{pnum(f"0{i + 1}", 0, 0, 16, LICHEN)}</svg><div class="s" style="color:{CHALK};margin-top:12px">{v}</div></div>' for i, v in enumerate(vals))
              + '</div>', w=W))
    pw, ph = 320, 672
    phone = (rel(0, 0, f'<div style="height:40px;display:flex;justify-content:space-between;align-items:center;padding:0 24px" class="cap"><span style="color:{CHALK}">9:41</span><span style="display:flex;gap:3px">' + "".join(f'<i style="width:5px;height:5px;border-radius:3px;background:{CHALK}"></i>' for _ in range(3)) + '</span></div>', w=pw)
        + rel(24, 56, mkw("compact-colour", 96))
        + svgbox(pw, ph, "".join(rect(pw - 24 - 20, 60 + k * 7, 20, 3, CHALK) for k in range(3)))
        + crop("assets/bg-ridges.png", 1920, 1200, 1050, 0, 0.36, 0, 104, pw, 232)
        + rel(24, 352, f'<div class="lab ac">Field intelligence</div><div style="font-weight:600;font-size:32px;line-height:36px;letter-spacing:-.02em;color:{CHALK};margin-top:16px">Understand systems. Protect people.</div>'
              f'<p class="s" style="color:{INK2};margin-top:16px">We show up, learn the operation, identify the issue, and give you practical options.</p>'
              f'<div style="margin-top:24px">{btn("Start with the problem", pad="12px 16px")}</div>', w=pw - 48))
    body = (head("Applications", "Website: desktop and mobile.", cs=8, n="12", dark=True)
        + at(X(9), Y(0) + 8, '<p class="cap mu">Headline uses the optional line “Understand systems. Protect people.” Body copy and values are taken from the client’s flyer.</p>', w=WD(3))
        + page(X(0), Y(1), W, Hh, site, BASALT, "outline:1px solid rgba(244,245,239,.14)")
        + page(X(9) + 11, Y(1), pw, ph, phone, BASALT, "border-radius:36px;outline:8px solid #050E0D")
        + at(X(0), Y(1) + Hh + 16, '<span class="cap mu">Desktop · 1440 px design width, shown at 75%</span>'))
    D.add(20, body, "Applications", "dk")

def b21(D):
    dx, dy = X(0) + 24, Y(1) + 8
    door = "M24,520 Q8,520 8,500 L4,232 Q4,214 16,200 L196,28 Q214,12 238,12 L812,8 Q836,8 836,32 L844,496 Q844,520 820,520 Z"
    glass = "M40,212 L210,52 Q222,40 240,40 L800,38 L806,212 Z"
    art = (f'<g transform="translate({dx + 40},{dy})"><rect x="-56" y="176" width="76" height="52" rx="10" fill="#1B2A29"/>'
           f'<path d="{door}" fill="#F7F8F5" stroke="#C3C9C2" stroke-width="2"/>'
           f'<path d="{glass}" fill="#1B2A29"/><path d="M540,39 L610,39 L452,212 L382,212 Z" fill="#FFFFFF" fill-opacity=".05"/>'
           f'<path d="M8,300 L842,292" stroke="#D5D9D3" stroke-width="2"/>'
           f'<rect x="708" y="244" width="96" height="20" rx="10" fill="#D5D9D3"/></g>')
    lk_w = 432; lk_h = lk_w * 1237 / 4800
    body = (head("Applications", "Field kit: vehicle, workwear, equipment.", cs=8, n="12")
        + svgl(art, z=1) + at(dx + 120, dy + 336, mkw("primary-basalt", lk_w), style="z-index:2")
        + at(dx + 120, dy + 336 + lk_h + 32, f'<span class="lab" style="color:{STONE}">[Website]</span>', style="z-index:2")
        + at(X(0), Y(5) - 16, '<div class="rule" style="padding-top:8px"><div class="lab">Vehicle door</div><p class="s mu" style="margin-top:4px">One-colour Basalt on light paint; the full-colour signature only on dark paint. Lockup about 600 mm wide on a 1 m door, clear of handles and seams.</p></div>', w=WD(7))
        + at(X(8), Y(1), "", w=WD(4), h=HT(2), style=f"background:{BASALT};border-radius:20px;box-shadow:inset 0 0 0 6px {MOSS},inset 0 0 0 8px {mix(MOSS, BASALT, .5)}")
        + mkw("compact-colour", 280, X(8) + (WD(4) - 280) / 2, Y(1) + (HT(2) - 280 * 1000 / 4800) / 2)
        + at(X(8), Y(3) - 8, '<div class="rule" style="padding-top:8px"><div class="lab">Embroidered patch</div><p class="s mu" style="margin-top:4px">76 × 48 mm. Five thread colours on Basalt twill; descriptor omitted at this size.</p></div>', w=WD(4))
        + page(X(8), Y(4) - 24, WD(4), 200, svgbox(WD(4), 200, sym(24, 24, 6, mono=BASALT) + wm(80, 24, 30, BASALT) + profile_px(0, 200, WD(4), 8, 4, mono=SAGE))
               + rel(24, 72, f'<div class="lab" style="color:{STONE}">Asset</div><div style="font-weight:600;font-size:32px;line-height:40px;letter-spacing:-.02em">[Asset no.]</div><p class="cap" style="color:{STONE};margin-top:4px">If found, please call [Phone]</p>', w=WD(4) - 48))
        + at(X(8), Y(5) + 48, '<div class="rule" style="padding-top:8px"><div class="lab">Equipment label</div><p class="s mu" style="margin-top:4px">For drone cases and field kit. Vinyl, 90 × 50 mm.</p></div>', w=WD(4)))
    D.add(21, body, "Applications", "st")

def b22(D):
    L, T = 1100 - 1344, 440 - 36
    sx, sy = 1100, 440; fh = 160; fw = 240
    art = (rect(sx - 3, sy - 330, 6, 330, CHALK) + rect(sx + 3, sy - 330, fw, fh, FLAG)
           + pnum("03", sx + 3 + 28, sy - 330 + 32, 64, BASALT) + sym(sx + 3 + fw - 28 - 64, sy - 330 + fh - 24 - 40, 8, mono=BASALT)
           + rect(sx - 12, sy - 6, 24, 24, FLAG))
    m_w = WD(3); cs = m_w / 24
    inset = (img("assets/map-tile.png", X(0), Y(3) + 24, m_w, m_w, cls="pix")
             + svgl(flagmark(X(0) + 19 * cs, Y(3) + 24 + 15 * cs, "03", cs * 2) + ln(X(0), Y(3) + 24 + m_w + 16, X(0) + m_w, Y(3) + 24 + m_w + 16, CHALK, 1, None, .2)))
    body = (img("assets/bg-ridges.png", L, T, 1920, 1200)
        + at(0, 0, "", w=760, h=1000, style=f"background:linear-gradient(90deg,{BASALT} 55%,rgba(14,36,35,0))")
        + svgl(art)
        + head("Applications", "The flag on the map is the flag in the field.", cs=4, n="12", dark=True)
        + para(0, Y(2) - 8, 3, "Observation markers carry the number used in the report, so a client can walk from the page to the place. Flag is reserved for this one job.", "b mu")
        + inset
        + at(X(0), Y(3) + 24 + m_w + 24, '<span class="cap mu">Map 1 · observation 03</span>')
        + at(sx + 3, sy - 330 + fh + 16, '<span class="cap" style="color:%s">Marker flag · 300 × 200 mm, on a 1 m stake</span>' % CHALK, w=WD(2)))
    D.add(22, body, "Applications", "dk", folio=CHALK)

def b23(D):
    W, Hh = 464, 656
    p1 = (crop("assets/ridges-tall.png", 1200, 1680, 0, 0, W / 1200, 0, 112, W, Hh - 112)
        + rel(32, 40, f'<div style="font-weight:600;font-size:56px;line-height:56px;letter-spacing:-.035em;color:{CHALK}">We actually<br>show up.</div>', w=W - 64)
        + rel(32, Hh - 32 - 54, mkw("primary-colour", 208)))
    p2 = (svgbox(W, Hh, pnum("01", 32, 40, 80, BASALT) + sym(32, Hh - 32 - 5 * 30, 30, mono=BASALT))
        + rel(32, 168, f'<div style="font-weight:600;font-size:56px;line-height:56px;letter-spacing:-.035em;color:{BASALT}">Start with<br>the problem.</div>', w=W - 64))
    ms = 400; cs = ms / 24
    p3 = (rel(32, 32, f'<div style="font-weight:600;font-size:56px;line-height:56px;letter-spacing:-.035em;color:{BASALT}">Practical.<br>Not theory.</div>', w=W - 64)
        + rel(32, 176, img("assets/map-tile.png", 0, 0, ms, 352, cls="pix", style="object-fit:cover;object-position:top"), w=ms, h=352, style="overflow:hidden")
        + svgbox(W, Hh, flagmark(32 + 14 * cs, 176 + 9 * cs, "02", cs * 2))
        + rel(32, Hh - 32 - 54, mkw("primary-basalt", 208)))
    body = (head("Applications", "Posters, in the client’s own words.", cs=8, n="12")
        + at(X(9), Y(0) + 8, '<p class="cap mu">Lines from the existing flyer. Pixel ridgelines, the symbol at scale, and a map with an observation.</p>', w=WD(3))
        + page(X(0), Y(1), W, Hh, p1, BASALT) + page(X(4), Y(1), W, Hh, p2, LICHEN) + page(X(8), Y(1), W, Hh, p3, CHALK))
    D.add(23, body, "Applications", "st")

def b24(D):
    dec = [("Approve the direction", "Ridgeline symbol, pixel HCO and pixel numerals, for refinement in Stage 2."),
           ("Confirm the trading name", "The old logo says “Group”; the flyer says “Consulting”. The descriptor shows High Country Observations only until this is settled."),
           ("Choose the typeface", "Instrument Sans (open licence, no cost) or a licensed commercial grotesk. Licence terms are checked before release; no font files are distributed."),
           ("Decide on terrain data", "Keep the illustrative model, or supply a real area and licensed elevation data. Imagery is never presented as survey output."),
           ("Check the name and mark", "“High Country” is also used by others, including a Chevrolet Silverado trim and an outdoor retailer. Clearance needs a qualified trademark adviser."),
           ("Review resemblance", "Pixel wordmarks are common in technology brands. A resemblance search on the final artwork is part of Stage 2; it is not legal clearance.")]
    rows = "".join(f'<div class="rule" style="display:flex;gap:24px;padding:16px 0 16px"><svg width="{COLW}" height="20" style="flex:none">{pnum(f"0{i + 1}", 0, 0, 20, BASALT)}</svg>'
                   f'<div style="flex:1"><div class="h3" style="font-size:20px;line-height:24px">{h}</div><p class="s mu" style="margin-top:4px">{t}</p></div></div>' for i, (h, t) in enumerate(dec))
    st2 = ["Five-page identity summary, A4 landscape PDF", "HCO-Brand-System.zip", "logos/ — SVG, PDF and PNG, all versions", "icons/ — 16, 32, 180 and 512 px",
           "source/ — master artwork and build scripts", "system/ — colour and type tokens, CSS and JSON", "previews/ and README.md"]
    body = (head("Decisions", "Six decisions before Stage 2.", cs=8, n="13")
        + at(X(0), Y(1), rows, w=WD(8))
        + at(X(9), Y(1), '<div class="lab" style="margin-bottom:16px">Stage 2 delivers</div>' + "".join(f'<div class="rule s" style="padding:8px 0">{e(t)}</div>' for t in st2), w=WD(3))
        + mkw("primary-basalt", WD(3), X(9), 920 - WD(3) * 1237 / 4800))
    D.add(24, body, "Decisions")
