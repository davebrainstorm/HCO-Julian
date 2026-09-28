"""Shape text with HarfBuzz (real kerning/features) and return outlined
SVG path data via fontTools — used so logo descriptors never depend on a font."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import functools, io

@functools.lru_cache(maxsize=None)
def _load(path, axes_items):
    axes = dict(axes_items)
    font = TTFont(path)
    if axes and "fvar" in font:
        font = instantiateVariableFont(font, axes, inplace=False)
    buf = io.BytesIO(); font.save(buf); data = buf.getvalue()
    return TTFont(io.BytesIO(data)), data

def shape(path, text, size, axes=None, features=None, tracking=0.0):
    """Return (svg_path_d, advance_width, upem_scale, cap_height) with the
    baseline at y=0 (SVG y-down). tracking in em units (e.g. 0.02)."""
    font, data = _load(path, tuple(sorted((axes or {}).items())))
    upem = font["head"].unitsPerEm
    face = hb.Face(data); hbfont = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, features or {"kern": True, "liga": True})
    gs = font.getGlyphSet(); order = font.getGlyphOrder()
    s = size / upem
    pen = SVGPathPen(gs)
    x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tp = TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s))
        gs[name].draw(tp)
        x += pos.x_advance * s + tracking * size
    x -= tracking * size
    cap = getattr(font["OS/2"], "sCapHeight", 0) * s
    return pen.getCommands(), x, s, cap
