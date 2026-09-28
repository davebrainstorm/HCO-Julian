"""Parametric construction of the custom HCO letterforms.
Units: cap height = 1000, y-up (font convention). Rounds are drawn as
4-segment cubic Béziers (type-design style extrema + handles), then combined
with skia-pathops booleans, so exported logos are clean outlined vectors with
a small number of points."""
import pathops

def oval(cx, cy, rx, ry, k=0.56, kx=None, ky=None):
    """Closed Bézier oval. k≈0.552 is a circle; larger k = squarer shoulders.
    kx/ky set the handle ratio on the horizontal / vertical extrema separately."""
    kx = k if kx is None else kx
    ky = k if ky is None else ky
    p = pathops.Path()
    p.moveTo(cx + rx, cy)
    p.cubicTo(cx + rx, cy + ky * ry, cx + kx * rx, cy + ry, cx, cy + ry)
    p.cubicTo(cx - kx * rx, cy + ry, cx - rx, cy + ky * ry, cx - rx, cy)
    p.cubicTo(cx - rx, cy - ky * ry, cx - kx * rx, cy - ry, cx, cy - ry)
    p.cubicTo(cx + kx * rx, cy - ry, cx + rx, cy - ky * ry, cx + rx, cy)
    p.close()
    return p

def rect(x, y, w, h):
    p = pathops.Path()
    p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y + h); p.lineTo(x, y + h); p.close()
    return p

def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p

def union(*ps):
    out = ps[0]
    for p in ps[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out

def diff(a, *bs):
    for b in bs:
        a = pathops.op(a, b, pathops.PathOp.DIFFERENCE)
    return a

def translate(path, dx, dy):
    out = pathops.Path()
    pen = out.getPen()
    path.draw(_Shift(pen, dx, dy))
    return out

class _Shift:
    def __init__(self, pen, dx, dy): self.pen, self.dx, self.dy = pen, dx, dy
    def _t(self, pts): return [(x + self.dx, y + self.dy) for x, y in pts]
    def moveTo(self, p): self.pen.moveTo(*self._t([p]))
    def lineTo(self, p): self.pen.lineTo(*self._t([p]))
    def curveTo(self, *ps): self.pen.curveTo(*self._t(ps))
    def qCurveTo(self, *ps): self.pen.qCurveTo(*self._t(ps))
    def closePath(self): self.pen.closePath()
    def endPath(self): self.pen.endPath()

def svg_d(path, cap=1000.0, scale=1.0, dx=0.0, dy=0.0, nd=2):
    """SVG path data, flipping y (cap height at top). Rounded to nd decimals."""
    f = lambda x, y: f"{round(x*scale+dx, nd):g} {round((cap-y)*scale+dy, nd):g}"
    d = []
    V = pathops.PathVerb
    for verb, pts in path:
        if verb == V.MOVE: d.append("M" + f(*pts[0]))
        elif verb == V.LINE: d.append("L" + f(*pts[0]))
        elif verb == V.CUBIC: d.append("C" + " ".join(f(*p) for p in pts))
        elif verb == V.QUAD: d.append("Q" + " ".join(f(*p) for p in pts))
        elif verb == V.CLOSE: d.append("Z")
        else: raise ValueError(verb)
    return "".join(d)

def count_points(path):
    return sum(len(pts) for _, pts in path)
