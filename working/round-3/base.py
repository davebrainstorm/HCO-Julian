"""Round 3 deck engine: 1600×1000 boards, 12×6 field grid, 8 px baseline."""
import re, html
from palette import E, BASALT, CHALK, LICHEN, FLAG, MOSS, SAGE, STONE, INK2, mix, contrast
F = "../fonts-static/"
COLW, GUT, MX, MY, ROWH = 98, 24, 80, 80, 120
def X(c): return MX + c * (COLW + GUT)
def WD(n): return n * COLW + (n - 1) * GUT
def Y(r): return MY + r * (ROWH + GUT)
def HT(n): return n * ROWH + (n - 1) * GUT
def e(t): return html.escape(t, quote=False)
def box(c, r, cs, rs, inner="", style="", cls=""):
    return f'<div class="abs {cls}" style="left:{X(c)}px;top:{Y(r)}px;width:{WD(cs)}px;height:{HT(rs)}px;{style}">{inner}</div>'
def at(x, y, inner, w=None, h=None, style="", cls=""):
    return f'<div class="abs {cls}" style="left:{x}px;top:{y}px;{f"width:{w}px;" if w else ""}{f"height:{h}px;" if h else ""}{style}">{inner}</div>'
def mk(name, w=None, h=None, style=""):
    s = open(f"marks/{name}.svg").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r'^<svg[^>]*>|</svg>$', '', s)
    size = (f"width:{w}px;" if w else "") + (f"height:{h}px;" if h else "") + ("height:auto;" if w and not h else "") + ("width:auto;" if h and not w else "")
    return f'<svg viewBox="{vb}" style="display:block;{size}{style}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def vb(name):
    v = re.search(r'viewBox="([^"]+)"', open(f"marks/{name}.svg").read()).group(1).split(); return [float(x) for x in v]

CSS = f"""
@font-face{{font-family:'HCO Sans';src:url('{F}InstrumentSans-Regular.ttf');font-weight:400}}
@font-face{{font-family:'HCO Sans';src:url('{F}InstrumentSans-Italic.ttf');font-weight:400;font-style:italic}}
@font-face{{font-family:'HCO Sans';src:url('{F}InstrumentSans-Medium.ttf');font-weight:500}}
@font-face{{font-family:'HCO Sans';src:url('{F}InstrumentSans-SemiBold.ttf');font-weight:600}}
@font-face{{font-family:'HCO Sans';src:url('{F}InstrumentSans-Bold.ttf');font-weight:700}}
@font-face{{font-family:'HCO Cond';src:url('{F}InstrumentSans-CondMedium.ttf');font-weight:500}}
@font-face{{font-family:'HCO Cond';src:url('{F}InstrumentSans-CondSemiBold.ttf');font-weight:600}}
@page{{size:1600px 1000px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#c7ccc8}}
body{{font-family:'HCO Sans';-webkit-font-smoothing:antialiased;font-kerning:normal;font-feature-settings:'kern' 1}}
.page{{width:1600px;height:1000px;position:relative;overflow:hidden;break-after:page;background:{CHALK};color:{BASALT}}}
@media screen{{.page{{margin:0 auto 24px}}}}
.dk{{background:{BASALT};color:{CHALK}}} .ms{{background:{mix(BASALT, MOSS, 0.55)};color:{CHALK}}} .st{{background:#E6E8E2;color:{BASALT}}}
.abs{{position:absolute}}
.d1{{font-weight:600;font-size:112px;line-height:112px;letter-spacing:-.035em}}
.h1{{font-weight:600;font-size:72px;line-height:72px;letter-spacing:-.03em}}
.h2{{font-weight:600;font-size:40px;line-height:48px;letter-spacing:-.02em}}
.h3{{font-weight:600;font-size:24px;line-height:32px;letter-spacing:-.01em}}
.bl{{font-size:20px;line-height:32px;letter-spacing:-.005em}}
.b{{font-size:16px;line-height:24px}}
.s{{font-size:14px;line-height:24px}}
.lab{{font-family:'HCO Cond';font-weight:600;font-size:12px;line-height:16px;letter-spacing:.11em;text-transform:uppercase}}
.cap{{font-size:12px;line-height:16px;letter-spacing:.01em}}
.num{{font-variant-numeric:tabular-nums lining-nums}}
.mu{{color:{STONE}}} .dk .mu,.ms .mu{{color:{INK2}}}
.ac{{color:{LICHEN}}}
.rule{{border-top:1px solid rgba(14,36,35,.18)}} .dk .rule,.ms .rule{{border-top:1px solid rgba(244,245,239,.16)}}
.chrome{{position:absolute;top:32px;left:80px;right:80px;display:flex;justify-content:space-between;z-index:9}}
.folio{{position:absolute;bottom:32px;right:80px;z-index:9}}
.pix{{image-rendering:pixelated;display:block}}
"""
class Deck:
    def __init__(self, total): self.pages = []; self.total = total
    def add(self, n, body, section, cls="", chrome=True, folio=None):
        ch = (f'<div class="chrome"><span class="lab mu">HCO — Identity System</span><span class="lab mu">{section}</span></div>'
              + svgl(pnum(f"{n:02d}", 1520, 948, 20, folio or (INK2 if ("dk" in cls or "ms" in cls) else STONE), "end"))) if chrome else ""
        self.pages.append((n, f'<section class="page {cls}">{ch}{body}</section>'))
    def html(self, title):
        return f"<!doctype html><html lang='en'><meta charset='utf-8'><title>{title}</title><style>{CSS}</style><body>{''.join(h for _, h in sorted(self.pages))}</body></html>"
def gridlines(show=False):
    """Debug overlay of the 12×6 field grid."""
    if not show: return ""
    cols = "".join(f'<div class="abs" style="left:{X(c)}px;top:{MY}px;width:{COLW}px;height:{HT(6)}px;background:rgba(236,93,47,.07)"></div>' for c in range(12))
    rows = "".join(f'<div class="abs" style="left:{MX}px;top:{Y(r)}px;width:{WD(12)}px;height:{ROWH}px;outline:1px solid rgba(236,93,47,.25)"></div>' for r in range(6))
    return cols + rows

# ---------- drawing primitives in page coordinates (px) ----------
def svgl(inner, z=6):
    return f'<svg class="abs" style="left:0;top:0;z-index:{z};overflow:visible" width="1600" height="1000" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def ln(x1, y1, x2, y2, col=FLAG, w=1, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-opacity="{op}"{d}/>'
def tx(x, y, s, col=BASALT, size=12, anchor="start", cond=True, weight=600, rot=None, ls=".08em", upper=True, op=1):
    fam = "HCO Cond" if cond else "HCO Sans"
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    tt = "text-transform:uppercase;" if upper else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" fill-opacity="{op}" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" style="{tt}font-variant-numeric:tabular-nums"{r}>{e(s)}</text>')
def tick(x, y, col=FLAG, w=1):          # architectural 45° tick
    return ln(x - 4, y + 4, x + 4, y - 4, col, w)
def hdim(x1, x2, y, label, col=FLAG, tcol=BASALT, above=True, ext=None):
    o = [ln(x1, y, x2, y, col), tick(x1, y, col), tick(x2, y, col)]
    if ext is not None:
        for x in (x1, x2): o.append(ln(x, ext, x, y + (-8 if ext > y else 8), col, 1, None, .55))
    o.append(tx((x1 + x2) / 2, y - 8 if above else y + 18, label, tcol, anchor="middle"))
    return "".join(o)
def vdim(x, y1, y2, label, col=FLAG, tcol=BASALT, left=True, ext=None):
    o = [ln(x, y1, x, y2, col), tick(x, y1, col), tick(x, y2, col)]
    if ext is not None:
        for y in (y1, y2): o.append(ln(ext, y, x + (-8 if ext > x else 8), y, col, 1, None, .55))
    xx = x - 10 if left else x + 18
    o.append(tx(xx, (y1 + y2) / 2, label, tcol, anchor="middle", rot=-90))
    return "".join(o)
def rect(x, y, w, h, fill="none", stroke=None, sw=1, dash=None, op=1, rx=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{s}{d}/>'
def img(src, x, y, w, h, style="", cls=""):
    return f'<img class="abs {cls}" src="{src}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">'
def crop(src, sw, sh, sx, sy, scale, x, y, w, h, style="", cls=""):
    """Window (x,y,w,h) on the page showing image src (sw×sh) scaled by `scale`, with source point (sx,sy) at the window's top-left."""
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;{style}">'
            f'<img class="{cls}" src="{src}" style="position:absolute;left:{-sx * scale:.1f}px;top:{-sy * scale:.1f}px;width:{sw * scale:.1f}px;height:{sh * scale:.1f}px"></div>')
def head(label, title, c=0, r=0, cs=3, dark=False, size="h2", n=None):
    num = f'<svg width="{pnum_w(n, 20) + 14:.0f}" height="20" style="display:inline-block;vertical-align:top;overflow:visible">{pnum(n, 0, 0, 20, LICHEN if dark else BASALT)}</svg>' if n else ""
    return (box(c, r, cs, 1, f'<div class="lab {"ac" if dark else ""}" style="{"" if dark else "color:" + BASALT};display:flex;align-items:center">{num}<span>{e(label)}</span></div>'
            f'<div class="{size}" style="margin-top:24px">{title}</div>', "height:auto"))
def para(c, y, cs, text, cls="b", style=""):
    return at(X(c), y, f'<p class="{cls}" style="{style}">{text}</p>', w=WD(cs))
SPACER = '<span style="display:inline-block;width:8px"></span>'
def notes(c, y, cs, items, dark=False, num=True, start=1):
    """Numbered notes, each with a hairline above."""
    out = []
    for i, (h, t) in enumerate(items):
        out.append(f'<div class="rule" style="padding-top:8px;margin-top:{0 if i == 0 else 16}px"><div class="lab {"ac" if dark else ""}" style="{"" if dark else "color:" + BASALT}">'
                   f'{(f"{i + start:02d}" + SPACER) if num else ""}{e(h)}</div><div class="s mu" style="margin-top:8px">{t}</div></div>')
    return at(X(c), y, "".join(out), w=WD(cs))

def mkw(name, w, x=None, y=None, style=""):
    _, _, W, H = vb(name); h = w * H / W
    s = mk(name, w=w, h=round(h, 2), style=style)
    return s if x is None else at(x, y, s, w=w, h=round(h, 2))
def mkh(name, h, x=None, y=None, style=""):
    _, _, W, H = vb(name); w = h * W / H
    s = mk(name, w=round(w, 2), h=h, style=style)
    return s if x is None else at(x, y, s, w=round(w, 2), h=h)
from mark import HEIGHTS
def sym(x, y, m, gap=0.10, mono=None, heights=HEIGHTS, rx=0, stroke=None, colours=None):
    """Symbol in page px: top-left (x,y), module m. Stands on y + 5m."""
    g = gap * m; o = []
    for i, h in enumerate(heights):
        fill = mono or (colours[i] if colours else E[h])
        if stroke: o.append(rect(x + i * m + g / 2, y + (4 - h) * m + g / 2, m - g, m - g, "none", stroke, 1.5, rx=rx))
        else: o.append(rect(x + i * m + g / 2, y + (4 - h) * m + g / 2, m - g, m - g, fill, rx=rx))
    return "".join(o)

# ---------- pixel artwork in page px ----------
import sys as _s; _s.path.insert(0, "../geometry")
from glyphs import svg_d as _svgd
from pixel import number as _number, wordmark as _pwm, FINAL as _FINAL, DIGITS
from mark import CAP as _CAP, M as _M
_WM = _svgd(_pwm(**_FINAL)[0], cap=_CAP)
def wm(x, y, h, fill=CHALK):
    """Pixel HCO, cap height h px, top-left (x, y)."""
    k = h / _CAP
    return f'<path transform="translate({x:.2f},{y:.2f}) scale({k:.5f})" d="{_WM}" fill="{fill}"/>'
def pnum(s, x, y, h, fill=CHALK, anchor="start"):
    """Pixel numerals, height h px (10 letter-pixels)."""
    p, w = _number(s); k = h / _CAP; ww = w * k
    if anchor == "end": x -= ww
    elif anchor == "middle": x -= ww / 2
    return f'<path transform="translate({x:.2f},{y:.2f}) scale({k:.5f})" d="{_svgd(p, cap=_CAP)}" fill="{fill}"/>'
def pnum_w(s, h): return _number(s)[1] * h / _CAP
