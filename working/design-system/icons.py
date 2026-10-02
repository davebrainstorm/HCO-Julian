"""Groundwork pixel icons: 24 × 24 grid, 2-px pen, 45° stairs, no curves (curves become octagons, like the O in HCO).
Live area 2…21. Output: SVG sprite, individual SVGs, JSON (bitmaps) and a QA sheet."""
import math, json, os, sys
import numpy as np
N = 24
YY, XX = np.mgrid[0:N, 0:N]
def oct_mask(x0, y0, x1, y1, c):
    inside = (XX >= x0) & (XX <= x1) & (YY >= y0) & (YY <= y1)
    if c <= 0: return inside
    return inside & (np.minimum(XX - x0, x1 - XX) + np.minimum(YY - y0, y1 - YY) >= c)
class I:
    def __init__(s): s.g = np.zeros((N, N), bool)
    def f(s, x0, y0, x1, y1, v=True): s.g[y0:y1 + 1, x0:x1 + 1] = v; return s
    def h(s, x0, x1, y, t=2): return s.f(x0, y, x1, y + t - 1)
    def v(s, x, y0, y1, t=2): return s.f(x, y0, x + t - 1, y1)
    def p(s, x, y, v=True): s.g[y, x] = v; return s
    def ring(s, x0, y0, x1, y1, c=1, t=2, cin=None):
        cin = max(0, round(c - t * (2 - math.sqrt(2)))) if cin is None else cin
        s.g |= oct_mask(x0, y0, x1, y1, c) & ~oct_mask(x0 + t, y0 + t, x1 - t, y1 - t, cin); return s
    def disc(s, x0, y0, x1, y1, c=1, v=True):
        m = oct_mask(x0, y0, x1, y1, c)
        if v: s.g |= m
        else: s.g &= ~m
        return s
    def d(s, x, y, n, dx, dy, t=2):              # 45° stroke: n steps of a t×t brush
        for k in range(n): s.f(x + k * dx, y + k * dy, x + k * dx + t - 1, y + k * dy + t - 1)
        return s
    def clear(s, x0, y0, x1, y1): return s.f(x0, y0, x1, y1, False)

ICONS = {}
def icon(name, group):
    def deco(fn): ICONS[name] = (group, fn); return fn
    return deco

# ---------------- interface ----------------
@icon("plus", "Interface")
def _(): return I().h(4, 19, 11).v(11, 4, 19)
@icon("minus", "Interface")
def _(): return I().h(4, 19, 11)
@icon("close", "Interface")
def _(): return I().d(5, 5, 13, 1, 1).d(17, 5, 13, -1, 1)
@icon("check", "Interface")
def _(): return I().d(4, 11, 5, 1, 1).d(9, 15, 10, 1, -1)
@icon("chevron-right", "Interface")
def _(): return I().d(8, 5, 6, 1, 1).d(13, 11, 6, -1, 1).f(13, 10, 14, 13)
@icon("chevron-left", "Interface")
def _(): return I().d(14, 5, 6, -1, 1).d(9, 11, 6, 1, 1).f(9, 10, 10, 13)
@icon("chevron-down", "Interface")
def _(): return I().d(5, 8, 6, 1, 1).d(11, 13, 6, 1, -1).f(10, 13, 13, 14)
@icon("chevron-up", "Interface")
def _(): return I().d(5, 14, 6, 1, -1).d(11, 9, 6, 1, 1).f(10, 9, 13, 10)
@icon("arrow-right", "Interface")
def _(): return I().h(3, 19, 11).d(13, 5, 7, 1, 1).d(13, 17, 7, 1, -1)
@icon("arrow-left", "Interface")
def _(): return I().h(4, 20, 11).d(9, 5, 7, -1, 1).d(9, 17, 7, -1, -1)
@icon("arrow-up", "Interface")
def _(): return I().v(11, 4, 20).d(5, 9, 7, 1, -1).d(17, 9, 7, -1, -1)
@icon("arrow-down", "Interface")
def _(): return I().v(11, 3, 19).d(5, 13, 7, 1, 1).d(17, 13, 7, -1, 1)
@icon("external", "Interface")
def _(): return I().h(4, 11, 4).v(4, 4, 19).h(4, 19, 18).v(18, 12, 19).h(13, 19, 4).v(18, 4, 10).d(10, 12, 8, 1, -1)
@icon("menu", "Interface")
def _(): return I().h(3, 20, 5).h(3, 20, 11).h(3, 20, 17)
@icon("more", "Interface")
def _(): return I().f(4, 10, 6, 12).f(10, 10, 13, 12).f(17, 10, 19, 12)
@icon("search", "Interface")
def _(): return I().ring(3, 3, 16, 16, c=4).d(14, 14, 7, 1, 1)
@icon("filter", "Interface")
def _(): return I().h(3, 20, 4).d(3, 5, 7, 1, 1).d(19, 5, 7, -1, 1).v(10, 11, 18).v(12, 11, 20).f(10, 18, 13, 20)
@icon("sliders", "Interface")
def _(): return I().h(3, 20, 6).h(3, 20, 16).f(14, 3, 17, 9).f(6, 13, 9, 19)
@icon("download", "Interface")
def _(): return I().v(11, 3, 15).d(5, 9, 6, 1, 1).d(17, 9, 6, -1, 1).h(3, 20, 19).v(3, 15, 20).v(19, 15, 20)
@icon("upload", "Interface")
def _(): return I().v(11, 5, 16).d(5, 9, 6, 1, -1).d(17, 9, 6, -1, -1).f(10, 4, 13, 5).h(3, 20, 19).v(3, 15, 20).v(19, 15, 20)
@icon("share", "Interface")
def _(): return I().ring(3, 9, 8, 14, c=1).ring(15, 3, 20, 8, c=1).ring(15, 15, 20, 20, c=1).d(8, 10, 6, 1, -1).d(8, 12, 6, 1, 1)
@icon("link", "Interface")
def _(): return I().ring(2, 9, 12, 14, c=1).ring(11, 9, 21, 14, c=1).clear(10, 9, 12, 9).clear(10, 14, 12, 14)
@icon("copy", "Interface")
def _(): return I().ring(8, 8, 20, 20, c=1).h(3, 14, 3).v(3, 3, 15).h(3, 6, 14)
@icon("edit", "Interface")
def _(): return I().d(6, 15, 10, 1, -1).d(8, 17, 10, 1, -1).f(4, 18, 6, 20).f(15, 4, 19, 8).clear(17, 4, 19, 4).clear(19, 4, 19, 6)
@icon("trash", "Interface")
def _(): return I().h(3, 20, 5).h(9, 14, 2).ring(5, 7, 18, 21, c=1).v(9, 10, 17).v(13, 10, 17)
@icon("print", "Interface")
def _(): return I().ring(6, 2, 17, 8, c=0).ring(2, 7, 21, 17, c=1).ring(6, 13, 17, 21, c=0).f(16, 10, 18, 11)
@icon("lock", "Interface")
def _(): return I().ring(4, 10, 19, 21, c=1).ring(7, 2, 16, 12, c=3).clear(7, 10, 8, 11).clear(15, 10, 16, 11).f(10, 14, 13, 17)
@icon("eye", "Interface")
def _(): return I().ring(1, 6, 22, 17, c=5).f(9, 9, 14, 14).clear(9, 9, 9, 9).clear(14, 9, 14, 9).clear(9, 14, 9, 14).clear(14, 14, 14, 14)
@icon("bell", "Interface")
def _(): return I().ring(5, 3, 18, 18, c=4).clear(5, 15, 18, 18).h(3, 20, 16).f(10, 19, 13, 21).f(10, 1, 13, 3)
@icon("user", "Interface")
def _(): return I().ring(7, 2, 16, 11, c=3).ring(3, 13, 20, 24, c=4).clear(3, 22, 20, 23)
@icon("users", "Interface")
def _(): return I().ring(3, 5, 10, 12, c=2).ring(1, 14, 12, 24, c=3).clear(1, 22, 12, 23).ring(13, 3, 20, 10, c=2).h(14, 21, 12).v(20, 12, 20).h(14, 21, 19)
@icon("calendar", "Interface")
def _(): return I().ring(2, 4, 21, 21, c=1).h(2, 21, 9).v(7, 2, 6).v(15, 2, 6).f(6, 13, 8, 15).f(11, 13, 13, 15).f(16, 13, 18, 15).f(6, 17, 8, 18)
@icon("clock", "Interface")
def _(): return I().ring(2, 2, 21, 21, c=6).v(11, 6, 12).h(11, 16, 11)
@icon("mail", "Interface")
def _(): return I().ring(2, 4, 21, 19, c=1).d(4, 6, 8, 1, 1).d(18, 6, 8, -1, 1)
@icon("phone", "Interface")
def _(): return I().ring(6, 1, 17, 22, c=1).h(10, 13, 18)
@icon("chat", "Interface")
def _(): return I().ring(2, 3, 21, 16, c=1).f(5, 16, 8, 17).d(5, 17, 4, 0, 1).clear(6, 18, 7, 21).f(5, 17, 6, 20)
@icon("home", "Interface")
def _(): return I().d(2, 11, 10, 1, -1).d(11, 2, 10, 1, 1).v(5, 11, 20).v(17, 11, 20).h(5, 18, 19).f(10, 14, 13, 20)
@icon("grid", "Interface")
def _(): return I().f(3, 3, 10, 10).f(13, 3, 20, 10).f(3, 13, 10, 20).f(13, 13, 20, 20).clear(5, 5, 8, 8).clear(15, 5, 18, 8).clear(5, 15, 8, 18).clear(15, 15, 18, 18)
@icon("list", "Interface")
def _(): return I().f(3, 4, 5, 6).h(8, 20, 4).f(3, 10, 5, 12).h(8, 20, 10).f(3, 16, 5, 18).h(8, 20, 16)

# ---------------- status ----------------
@icon("info", "Status")
def _(): return I().ring(2, 2, 21, 21, c=6).f(11, 6, 12, 7).v(11, 10, 17)
@icon("warning", "Status")
def _():
    g = I()
    for k in range(10): g.f(11 - k, 2 + 2 * k, 12 + k, 3 + 2 * k)
    g.g &= ~(np.vstack([np.zeros((5, N), bool), I().g[5:]]) )
    inner = I()
    for k in range(7): inner.f(11 - k, 7 + 2 * k, 12 + k, 8 + 2 * k)
    g.g &= ~inner.g
    return g.v(11, 9, 14).f(11, 17, 12, 18)
@icon("error", "Status")
def _(): return I().ring(2, 2, 21, 21, c=6).d(8, 8, 7, 1, 1).d(14, 8, 7, -1, 1)
@icon("success", "Status")
def _(): return I().ring(2, 2, 21, 21, c=1).d(6, 11, 4, 1, 1).d(9, 14, 8, 1, -1)
@icon("sample", "Status")
def _(): return I().f(7, 7, 16, 16)
@icon("priority-1", "Status")
def _(): return I().f(3, 15, 7, 19).f(9, 15, 13, 19).f(15, 15, 19, 19)
@icon("flag", "Status")
def _(): return I().v(4, 2, 21).f(6, 3, 19, 12).clear(8, 5, 17, 10)

# ---------------- field ----------------
@icon("drone", "Field")
def _():
    g = I()
    for x0, y0 in ((1, 1), (15, 1), (1, 15), (15, 15)): g.ring(x0, y0, x0 + 7, y0 + 7, c=2)
    return g.d(7, 7, 4, 1, 1).d(15, 7, 4, -1, 1).d(7, 15, 4, 1, -1).d(15, 15, 4, -1, -1).f(9, 9, 14, 14)
@icon("flight-path", "Field")
def _(): return I().f(2, 18, 5, 21).h(4, 9, 19).d(9, 18, 5, 1, -1).h(13, 19, 14).v(18, 4, 15).f(16, 2, 21, 7).clear(18, 4, 19, 5)
@icon("camera", "Field")
def _(): return I().ring(2, 6, 21, 20, c=1).ring(7, 9, 16, 18, c=3).h(8, 15, 4).f(17, 9, 18, 10)
@icon("image", "Field")
def _(): return I().ring(2, 3, 21, 20, c=1).f(14, 6, 17, 9).d(4, 16, 5, 1, -1).d(8, 12, 7, 1, 1)
@icon("map", "Field")
def _(): return I().v(2, 4, 19).v(8, 2, 17).v(14, 6, 21).v(20, 4, 19).d(2, 4, 3, 1, -1).d(8, 2, 3, 1, 1).d(14, 6, 3, 1, -1).d(2, 19, 3, 1, -1).d(8, 17, 3, 1, 1).d(14, 21, 3, 1, -1).clear(0,0,0,0)
@icon("layers", "Field")
def _():
    g = I()
    for y in (3, 9):
        g.d(2, y + 5, 10, 1, -1 if False else 0) if False else None
    g.d(2, 8, 6, 1, -1).d(7, 3, 1, 1, 0).h(7, 16, 3).d(16, 3, 6, 1, 1).d(16, 13, 6, 1, -1).h(7, 16, 13).d(2, 8, 6, 1, 1)
    g.d(2, 14, 6, 1, 1).h(7, 16, 19).d(16, 19, 6, 1, -1)
    return g
@icon("field", "Field")
def _(): return I().ring(2, 2, 21, 21, c=1).v(11, 2, 21).h(2, 21, 11).f(14, 14, 18, 18)
@icon("pivot", "Field")
def _(): return I().ring(2, 2, 21, 21, c=6).f(10, 10, 13, 13).d(13, 10, 5, 1, -1)
@icon("water", "Field")
def _():
    g = I()
    for k in range(7): g.f(11 - k, 2 + k, 12 + k, 3 + k)
    g.disc(4, 8, 19, 21, c=4)
    g.disc(7, 11, 16, 18, c=2, v=False)
    for k in range(4): g.clear(11 - k, 6 + k, 12 + k, 6 + k)
    return g
@icon("fence", "Field")
def _(): return I().v(3, 4, 20).v(11, 4, 20).v(19, 4, 20).h(2, 21, 8).h(2, 21, 14).f(3, 3, 4, 3).f(11, 3, 12, 3).f(19, 3, 20, 3).clear(3,3,4,3).clear(11,3,12,3).clear(19,3,20,3)
@icon("track", "Field")
def _(): return I().d(3, 20, 8, 1, -1).d(12, 20, 8, 1, -1).v(11, 9, 11).v(11, 15, 17).d(10, 12, 0, 1, 1).h(10, 13, 3).h(19, 21, 3, t=0) if False else I().d(2, 20, 8, 1, -1).v(9, 2, 13).d(14, 20, 8, 1, -1).v(13, 2, 13).f(11, 4, 11, 5).f(11, 9, 11, 10).f(11, 15, 12, 16).clear(0, 0, 0, 0)
@icon("area", "Field")
def _(): return I().d(4, 8, 5, 1, -1).h(8, 17, 3).v(18, 3, 13).d(13, 18, 5, 1, -1).h(4, 14, 19).v(3, 8, 20).f(2, 7, 5, 10).f(16, 2, 19, 5).f(17, 12, 20, 15).f(2, 18, 5, 21)
@icon("measure", "Field")
def _(): return I().d(2, 18, 17, 1, -1).d(4, 20, 17, 1, -1).f(6, 16, 7, 17).f(9, 13, 10, 14).f(12, 10, 13, 11).f(15, 7, 16, 8)
@icon("terrain", "Field")
def _():
    g = I()
    for i, hgt in enumerate([0, 1, 1, 2, 3, 4, 3, 2]):
        x = 2 + i * 2 + (i // 1) * 0
        y = 18 - hgt * 3
        g.f(1 + i * 3 - (1 if i else 0) * 0, y, 1 + i * 3 + 1, y + 1)
    return g
@icon("sprout", "Field")
def _(): return I().v(11, 9, 21).d(10, 10, 6, -1, -1).ring(2, 2, 10, 9, c=2).d(12, 12, 5, 1, -1).ring(13, 5, 21, 12, c=2).clear(10, 9, 10, 10)
@icon("sun", "Field")
def _(): return I().ring(7, 7, 16, 16, c=3).v(11, 1, 4).v(11, 19, 22).h(1, 4, 11).h(19, 22, 11).d(3, 3, 3, 1, 1).d(19, 3, 3, -1, 1).d(3, 19, 3, 1, -1).d(19, 19, 3, -1, -1)
@icon("wind", "Field")
def _(): return I().h(2, 15, 7).h(2, 19, 12).h(2, 12, 17).f(15, 4, 17, 6).f(17, 7, 18, 8).clear(15,4,15,4).f(19, 13, 21, 15).f(12, 18, 14, 20).clear(0,0,0,0)
@icon("battery", "Field")
def _(): return I().ring(1, 6, 19, 17, c=1).f(20, 9, 22, 14).f(4, 9, 7, 14).f(9, 9, 12, 14)
@icon("signal", "Field")
def _(): return I().f(2, 17, 5, 21).f(8, 12, 11, 21).f(14, 7, 17, 21).f(20, 2, 21, 21)
@icon("target", "Field")
def _(): return I().ring(3, 3, 20, 20, c=5).f(10, 10, 13, 13).v(11, 0, 4).v(11, 19, 23).h(0, 4, 11).h(19, 23, 11)
@icon("compass", "Field")
def _():
    g = I().ring(2, 2, 21, 21, c=6)
    for k in range(5): g.f(11 - k // 2, 5 + k, 12 + k // 2, 5 + k)
    return g.f(11, 10, 12, 18)
@icon("spectrum", "Field")
def _(): return I().f(2, 12, 5, 21).f(7, 8, 10, 21).f(12, 4, 15, 21).f(17, 10, 21, 21).clear(18, 12, 20, 12).clear(18, 16, 20, 16).clear(19, 14, 19, 14).clear(19, 18, 19, 18)
@icon("index", "Field")
def _(): return I().ring(2, 2, 21, 21, c=1).f(5, 15, 7, 18).f(9, 12, 11, 18).f(13, 9, 15, 18).f(17, 5, 18, 18)
@icon("repeat", "Field")
def _(): return I().h(4, 17, 5).v(17, 5, 11).f(14, 9, 20, 10).clear(14, 10, 14, 10).clear(20, 10, 20, 10).f(15, 11, 19, 11).h(6, 19, 17).v(4, 12, 18).f(3, 13, 9, 14).clear(3, 13, 3, 13).clear(9, 13, 9, 13).f(4, 12, 8, 12).v(4, 5, 8).v(17, 15, 18)
@icon("report", "Field")
def _(): return I().ring(4, 2, 19, 21, c=1).h(8, 15, 7).h(8, 15, 11).h(8, 12, 15).clear(15, 2, 19, 5).d(15, 2, 4, 1, 1).v(14, 2, 6).h(14, 19, 6)
@icon("observation", "Field")
def _(): return I().f(4, 2, 19, 15).clear(6, 4, 17, 13).f(4, 16, 7, 19).f(4, 20, 5, 21).f(9, 7, 14, 10)


# ---------------- revisions (override earlier drafts; dict keeps original order) ----------------
def outline(mask, t=2):
    er = mask.copy()
    for _ in range(t):
        e = er.copy(); e[1:, :] &= er[:-1, :]; e[:-1, :] &= er[1:, :]; e[:, 1:] &= er[:, :-1]; e[:, :-1] &= er[:, 1:]
        e[0, :] = False; e[-1, :] = False; e[:, 0] = False; e[:, -1] = False; er = e
    return mask & ~er
def diamond(cx2, cy2, r):            # filled 45° diamond, centre at (cx2/2, cy2/2) in half-pixels
    return (np.abs(2 * XX + 1 - cx2) + np.abs(2 * YY + 1 - cy2)) <= 2 * r
@icon("link", "Interface")
def _():
    g = I().ring(2, 7, 14, 16, c=2).ring(9, 7, 21, 16, c=2)
    return g.clear(9, 7, 10, 8).clear(13, 15, 14, 16)
@icon("user", "Interface")
def _(): return I().ring(7, 2, 16, 11, c=3).ring(3, 13, 20, 21, c=4).clear(3, 20, 20, 21).h(3, 20, 20)
@icon("users", "Interface")
def _():
    g = I().ring(12, 2, 19, 9, c=2).ring(9, 11, 22, 19, c=3)
    g.g[:, :] &= ~oct_mask(1, 6, 13, 22, 0)
    return g.ring(3, 6, 10, 13, c=2).ring(0, 15, 13, 23, c=3).clear(0, 22, 13, 23).h(0, 13, 21).clear(0, 0, 0, 0)
@icon("chat", "Interface")
def _(): return I().ring(2, 3, 21, 16, c=1).f(5, 16, 9, 17).f(5, 18, 7, 19).f(5, 20, 5, 20).f(6, 20, 6, 20)
@icon("map", "Field")
def _(): return I().ring(2, 5, 8, 20, c=0).ring(8, 3, 15, 18, c=0).ring(15, 5, 21, 20, c=0)
@icon("layers", "Field")
def _():
    g = I()
    g.g |= outline(diamond(24, 14, 9) & (YY <= 15))
    lower = diamond(24, 24, 9) & ~diamond(24, 20, 9) & (YY >= 13)
    g.g |= lower
    return g
@icon("water", "Field")
def _():
    m = oct_mask(4, 9, 19, 21, 5)
    for k in range(8): m |= (YY == 2 + k) & (XX >= 11 - k) & (XX <= 12 + k)
    g = I(); g.g |= outline(m); return g
@icon("warning", "Status")
def _():
    m = np.zeros((N, N), bool)
    for k in range(10): m |= (YY >= 2 + 2 * k) & (YY <= 3 + 2 * k) & (XX >= 11 - k) & (XX <= 12 + k)
    m &= YY <= 21
    g = I(); g.g |= outline(m); return g.v(11, 9, 14).f(11, 17, 12, 18)
@icon("track", "Field")
def _(): return I().v(3, 2, 21).v(19, 2, 21).f(11, 2, 12, 5).f(11, 9, 12, 13).f(11, 17, 12, 21)
@icon("terrain", "Field")
def _(): return I().h(1, 4, 18).d(4, 18, 10, 1, -1).f(13, 8, 14, 9).d(14, 9, 7, 1, 1).h(20, 22, 15).clear(0, 0, 0, 0)
@icon("sprout", "Field")
def _():
    g = I().v(11, 11, 21)
    g.g |= diamond(14, 14, 5) & ~((XX > 7) & (YY > 7) & False)
    g.g |= diamond(34, 10, 5)
    return g.h(6, 17, 20)
@icon("wind", "Field")
def _(): return I().h(2, 14, 7).f(15, 4, 16, 6).h(13, 16, 3).h(2, 18, 12).f(19, 13, 20, 16).h(15, 20, 17).h(2, 11, 17).clear(15, 17, 20, 18).f(12, 18, 13, 20).h(9, 13, 21).clear(0, 0, 0, 0)
@icon("repeat", "Field")
def _():
    g = I().h(4, 17, 6).v(4, 6, 11).d(14, 3, 4, 1, 1).d(14, 9, 4, 1, -1)
    return g.h(6, 19, 17).v(18, 12, 18).d(9, 14, 4, -1, 1).d(9, 20, 4, -1, -1)
@icon("help", "Status")
def _(): return I().ring(2, 2, 21, 21, c=6).h(9, 14, 6).v(14, 6, 11).h(11, 14, 11).v(11, 11, 14).f(11, 16, 12, 17)
@icon("zoom-in", "Interface")
def _(): return I().ring(3, 3, 16, 16, c=4).d(14, 14, 7, 1, 1).h(7, 12, 9).v(9, 7, 12)
@icon("zoom-out", "Interface")
def _(): return I().ring(3, 3, 16, 16, c=4).d(14, 14, 7, 1, 1).h(7, 12, 9)
@icon("fullscreen", "Interface")
def _(): return I().h(2, 8, 2).v(2, 2, 8).h(15, 21, 2).v(20, 2, 8).h(2, 8, 20).v(2, 15, 21).h(15, 21, 20).v(20, 15, 21)
@icon("moon", "Interface")
def _():
    m = oct_mask(3, 3, 20, 20, 6) & ~oct_mask(9, 0, 23, 15, 5)
    g = I(); g.g |= outline(m); return g
@icon("play", "Interface")
def _():
    g = I()
    for k in range(9): g.f(6, 3 + k, 6 + k, 3 + k).f(6, 20 - k, 6 + k, 20 - k)
    return g
@icon("pause", "Interface")
def _(): return I().f(6, 4, 9, 19).f(14, 4, 17, 19)
@icon("folder", "Interface")
def _(): return I().ring(2, 6, 21, 20, c=1).h(2, 9, 3).v(2, 3, 7).d(9, 3, 3, 1, 1).h(11, 21, 6)
@icon("location", "Field")
def _(): return I().ring(5, 2, 18, 15, c=1).f(9, 6, 14, 11).f(5, 16, 8, 19).f(5, 20, 6, 21)
@icon("north", "Field")
def _():
    g = I()
    for k in range(10): g.f(11 - k // 2, 2 + k, 12 + k // 2, 2 + k)
    g.clear(11, 8, 12, 11)
    return g.v(5, 14, 21).v(16, 14, 21).d(7, 14, 8, 1, 1).clear(0, 0, 0, 0)

@icon("user", "Interface")
def _(): return I().ring(8, 2, 15, 9, c=2).ring(4, 12, 19, 27, c=5).clear(4, 22, 19, 23).h(4, 19, 20)
@icon("users", "Interface")
def _():
    back = I().ring(14, 3, 20, 9, c=2).ring(11, 12, 23, 27, c=4).clear(11, 22, 23, 23).h(11, 22, 20)
    front_area = oct_mask(2, 4, 12, 13, 2) | oct_mask(0, 13, 15, 27, 4)
    back.g &= ~front_area
    return back.ring(3, 5, 10, 12, c=2).ring(1, 14, 14, 27, c=4).clear(1, 22, 14, 23).h(1, 14, 20)
@icon("water", "Field")
def _():
    m = np.zeros((N, N), bool)
    for k in range(8): m |= (YY == 2 + k) & (XX >= 11 - k) & (XX <= 12 + k)
    body = (XX >= 4) & (XX <= 19) & (YY >= 9) & (YY <= 21) & ((np.minimum(XX - 4, 19 - XX) + (21 - YY)) >= 4)
    g = I(); g.g |= outline(m | body); return g
@icon("sprout", "Field")
def _():
    g = I().v(11, 9, 21)
    g.g |= diamond(13, 15, 4.5) | diamond(33, 11, 4.5)
    return g.f(10, 8, 11, 9).f(12, 6, 12, 9)

def svg_path(g, s=1):
    """Merge pixel runs into one path (row runs, then vertical merge of equal runs)."""
    runs = []
    for y in range(N):
        x = 0
        while x < N:
            if g[y, x]:
                x0 = x
                while x < N and g[y, x]: x += 1
                runs.append([x0, y, x - x0, 1])
            else: x += 1
    merged = []
    for r in runs:
        for m in merged:
            if m[0] == r[0] and m[2] == r[2] and m[1] + m[3] == r[1]: m[3] += 1; break
        else: merged.append(list(r))
    return "".join(f"M{x * s} {y * s}h{w * s}v{h * s}h-{w * s}z" for x, y, w, h in merged)

if __name__ == "__main__":
    out = "../../review/hco/assets/icons/"; os.makedirs(out, exist_ok=True)
    data = {}; sprite = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for name, (group, fn) in ICONS.items():
        g = fn().g; data[name] = {"group": group, "rows": ["".join("#" if v else "." for v in row) for row in g]}
        d = svg_path(g)
        open(f"{out}{name}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" shape-rendering="crispEdges"><path d="{d}" fill="currentColor"/></svg>\n')
        sprite.append(f'<symbol id="i-{name}" viewBox="0 0 24 24"><path d="{d}"/></symbol>')
    sprite.append("</svg>")
    open(f"{out}sprite.svg", "w").write("\n".join(sprite))
    os.makedirs("build", exist_ok=True); json.dump(data, open("build/icons.json", "w"))
    # QA sheet
    from PIL import Image, ImageDraw
    names = list(ICONS); cols = 10; cell = 24 * 5 + 40; rows = (len(names) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell, rows * (cell + 20)), (14, 36, 35)); dr = ImageDraw.Draw(im)
    for k, name in enumerate(names):
        g = ICONS[name][1]().g; ox = (k % cols) * cell + 20; oy = (k // cols) * (cell + 20) + 10
        for y in range(N):
            for x in range(N):
                c = (244, 245, 239) if g[y, x] else ((30, 52, 50) if (x + y) % 2 else (24, 46, 44))
                dr.rectangle([ox + x * 5, oy + y * 5, ox + x * 5 + 4, oy + y * 5 + 4], fill=c)
        dr.text((ox, oy + 24 * 5 + 4), name, fill=(149, 159, 154))
    im.save("build/icons-qa.png"); print(len(names), "icons")
