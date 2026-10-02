"""Static instances of Instrument Sans (SIL OFL 1.1, no Reserved Font Name) for PDF embedding.
Variable fonts embed as Type 3 in Chromium's PDF output; static instances embed as proper TrueType subsets.
Names are kept honest ("Instrument Sans Static …") so embedded font lists show the real typeface.
Output goes to working/fonts-static/, which is gitignored: font files are never committed or distributed.
Run from working/:  python3 tools/static_fonts.py"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
SRC = "fonts-ofl/instrumentsans/"
OUT = "fonts-static/"
FAM = "Instrument Sans Static"
INST = [("Regular", "InstrumentSans[wdth,wght].ttf", 100, 400), ("Medium", "InstrumentSans[wdth,wght].ttf", 100, 500),
        ("SemiBold", "InstrumentSans[wdth,wght].ttf", 100, 600), ("Bold", "InstrumentSans[wdth,wght].ttf", 100, 700),
        ("Italic", "InstrumentSans-Italic[wdth,wght].ttf", 100, 400),
        ("CondMedium", "InstrumentSans[wdth,wght].ttf", 75, 500), ("CondSemiBold", "InstrumentSans[wdth,wght].ttf", 75, 600)]
os.makedirs(OUT, exist_ok=True)
for style, src, wdth, wght in INST:
    f = instantiateVariableFont(TTFont(SRC + src), {"wdth": wdth, "wght": wght}, updateFontNames=False)
    cond = style.startswith("Cond"); sub = style[4:] if cond else style
    fam = FAM + (" Condensed" if cond else ""); full = f"{fam} {sub}"; ps = (fam + "-" + sub).replace(" ", "")
    n = f["name"]
    for rec in list(n.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 21, 22, 25): n.removeNames(nameID=rec.nameID)
    for nid, val in ((1, full if sub not in ("Regular", "Italic", "Bold") else fam), (2, sub if sub in ("Regular", "Italic", "Bold") else "Regular"),
                     (3, f"{ps};static"), (4, full), (6, ps), (16, fam), (17, sub)):
        n.setName(val, nid, 3, 1, 0x409)
    f["OS/2"].usWeightClass = wght; f["OS/2"].usWidthClass = 3 if cond else 5
    f.save(f"{OUT}InstrumentSans-{style}.ttf"); print(style, "→", ps)
