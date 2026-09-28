"""Pixel-size tests: render compact marks and signatures at true pixel sizes,
plus nearest-neighbour enlargements for inspection."""
import cairosvg, re, io
from PIL import Image
def render(svgfile, box_w, box_h, out, pad=0):
    s = open(svgfile).read()
    w, h = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
    sc = min((box_w - 2*pad) / w, (box_h - 2*pad) / h)
    png = cairosvg.svg2png(bytestring=s.encode(), output_width=max(1, round(w*sc)), output_height=max(1, round(h*sc)))
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    canvas = Image.new("RGBA", (box_w, box_h), (255, 255, 255, 0))
    canvas.paste(im, ((box_w - im.width)//2, (box_h - im.height)//2), im)
    canvas.save(out); return canvas
def flat(im):
    bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im); return bg.convert("RGB")
for r, f in [("r1", "marks/r1-compact-black.svg"), ("r2", "marks/r2-symbol-black.svg"), ("r3", "marks/r3-compact-black.svg")]:
    for px in (16, 24, 32):
        im = render(f, px, px, f"px/{r}-compact-{px}.png", pad=1 if px < 24 else 2)
        flat(im).resize((px*6, px*6), Image.NEAREST).save(f"px/{r}-compact-{px}-x6.png")
for r, f in [("r1", "marks/r1-wordmark-black.svg"), ("r2", "marks/r2-lockup-black.svg"), ("r3", "marks/r3-wordmark-black.svg")]:
    for hpx in (20, 28):
        s = open(f).read(); w, h = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
        bw = round(w/h*hpx)
        im = render(f, bw, hpx, f"px/{r}-word-{hpx}.png")
        flat(im).resize((bw*4, hpx*4), Image.NEAREST).save(f"px/{r}-word-{hpx}-x4.png")
print("px ok")
