# HCO identity — internal working notes

_Working folder only. Nothing here goes into the client handover ZIP._
_Stage 1 (exploration) — 28 September 2026. Round 3 identity system — 2 October 2026._

## Status

| Stage | State |
|---|---|
| 1 · Concept routes and type directions | **Presented for approval**: `concepts/HCO-Concept-Review.pdf` (11 pages, three routes and type directions) and `concepts/HCO-Top-5-Concepts.pdf` (8 pages, five concepts ranked). Previews are in `concepts/review-png/` and `concepts/top5-png/` |
| Round 3 · Identity system presentation | **Presented for review**: `round-3/HCO-Identity-Round-3.pdf` (24 boards). Pixel HCO, Ridgeline symbol, pixel numerals, imagery and applications. |
| 2 · Identity system, five-page pack, exports and QA | **Not started.** Waiting for direction, type and naming decisions. The brief says not to finalise the book around an unapproved logo. |

## Round 3 — identity system, pixel direction (2 October 2026)

`working/round-3/HCO-Identity-Round-3.pdf` contains 24 boards at 1600 × 1000 px. PNGs at 1920 × 1200 are in `round-3/boards/`.

**Brief for this round.** The user said Round 2 "looks like a €2k design" and asked for €50k craft: everything gridded and aligned, "a masterclass in branding design". Mid-round they added a third-party reference: a pixel wordmark (KURATE). It is monoline, the stroke is two pixels, and curves step in one-pixel stairs. The instruction was to replicate that pixel style for the mountain terrain and the HCO text.
- The reference was shared as an image in the conversation and is not stored in the repo. It is internal inspiration only and is not shown in the client deck.
- Only the technique is borrowed. The HCO letterforms are drawn from scratch on HCO's own module.
- This reverses the Round 2 rejection of "W2 grid-built", which was judged to read as a game face. The difference now is a finer stair logic, integer proportions, and a calm uppercase descriptor in Instrument Sans.

**Mark (master files in `round-3/marks/`, built by `marks.py` from `mark.py` and `pixel.py`).**
- **Symbol: Ridgeline, unchanged in idea.**
  - Eight samples of a measured section, heights 0 1 1 2 3 4 3 2, one cell per sample, on an 8 × 5 module grid. The cell gap is 0.1M.
  - The section is now real within the model. `voxel.py` uses SEC = row 224, x 1560–1655 of seed-11 terrain. Its interval means × 4 are 0.17 0.72 1.12 1.75 2.77 3.75 2.79 1.68, which round to the symbol (`assets/section.json`).
- **Wordmark: pixel HCO (`pixel.py`, `FINAL`).**
  - Letter-pixel p = M/2 = 100 units. The stroke is 2 px = 1M, and the cap height is 10 px = 5M.
  - Widths: H 8 px, C 9 px, O 10 px.
  - Corners have 2-stair outer and 1-stair inner steps, so the 45° stroke stays close to the straight-stroke weight.
  - Spacing is H–C 2 px and C–O 1 px. The total is 30 px = **15M exactly**.
  - The crossbar sits in rows 2–3 from the top (High Bar retained). The C's aperture runs 400–700 units from the top, so the C's upper jaw ends on the same line as the crossbar: one horizon at 0.6 of the cap height.
  - Pixels have no overshoot.
- **Signature: 24 × 5 modules.** It reads symbol 8M, gap 1M, wordmark 15M.
  - The descriptor is "HIGH COUNTRY OBSERVATIONS" in Instrument Sans Medium, uppercase, tracked +0.04 em and outlined.
  - It is scaled so its *ink* spans exactly the ink of HCO, and its cap top hangs one letter-pixel (0.5M) below the baseline.
  - Descriptor treatments compared are in `explore/desc-test*.png`.
- **Stacked version:** the symbol is centred over the wordmark.
- **Pixel numerals:** 0–9, tabular, 8 × 10 px, in the same pen (`pixel.py`, `DIGITS`). They are for section numbers, observation markers and key figures, never running text.
- **Explorations:**
  - `explore/pixel-wordmarks*.png`: variants A–F and A1–R2. A = M/2 with 2-stair corners was chosen. B is too square; C is diamond-like; D–F are smoother but read as octagons and lose the pixel character.
  - R1/R2 tested the ridgeline as a continuous 2-px stroke. That was kept for imagery and charts, not the symbol, because a stepped mountain line is close to stock pixel-mountain icons.
- **Fixed defect:** Round 2 and early Round 3 lockup SVGs used a viewBox starting at y = 0, which clipped the −12-unit overshoot of the drawn O and C by 0.6% of the cap height. The Round 2 files are superseded and left as they were. Pixel letters have no overshoot, and `mark.svg()` now takes an explicit y0.

**Minimum sizes (computed).**

| Version | Screen | Print | Basis |
|---|---|---|---|
| Primary | 200 px | 45 mm | Descriptor cap 135 units, so 200 px gives a 9.5 px descriptor and 45 mm gives about 6 pt |
| Compact | 96 px | 20 mm | — |
| Symbol | 16 px | 6 mm | Pixel-snapped favicons below 48 px |

**Imagery.** All imagery comes from one illustrative dataset: seed-11 procedural terrain, not a real place.
- `voxel.py`: isometric block model, cut along section A–A.
- `assets.py`: pixel map, dot matrix and report map tile.
- `ridges.py`: new pixel ridgelines. These are stacked profiles drawn with the wordmark's pen (2-px stroke, 1-px stairs, 12 px cells), with nearer lines occluding farther ones.
- Colour is by elevation percentile, so Basalt dominates and the signal colours appear only on the top few percent.

**Deck system.** 1600 × 1000 boards on a 12-column grid (margin 80, column 98, gutter 24) with 6 rows of 120 (gutter 24) and an 8 px baseline.
- Type scale: Display 112/112, H1 72/72, H2 40/48, H3 24/32, Body L 20/32, Body 16/24, Label 12/16 (condensed caps), Caption 12/16.
- Construction drawings use Flag dimension lines with architectural ticks.
- Applications: report cover and spread, stationery, website (desktop and mobile), vehicle door, patch, equipment label, observation marker, posters.
- All contact details are bracketed placeholders. Sample report content is labelled as such, and copy lines come from the client's flyer.

**Fonts.**
- `tools/static_fonts.py` builds static instances of Instrument Sans (OFL 1.1, no Reserved Font Name) into the git-ignored `fonts-static/`. They are named "Instrument Sans Static …", so the PDF's embedded font list names the real typeface. The CSS alias in the deck is `HCO Sans`.
- Glyphs missing from Instrument Sans (½ ≥ ● and the en space) were removed from the copy, so the PDF embeds no fallback fonts.
- Verified: only Instrument Sans subsets are embedded, and `deck.html` contains no absolute paths.

**Rebuild.** Needs numpy and the OFL fonts fetched into `fonts-ofl/`.

```bash
python3 tools/static_fonts.py
cd round-2 && python3 backgrounds.py 11          # writes the git-ignored assets/dem1920-11.npy
cd ../round-3 && python3 voxel.py && python3 assets.py && python3 ridges.py && python3 marks.py
python3 build_deck.py && node ../tools/pages.mjs deck.html boards board 1.2 HCO-Identity-Round-3.pdf
```

**Still open with the user/client.**
- Approval of the pixel direction.
- Trading name: Group or Consulting.
- Typeface: Instrument Sans or a licensed alternative.
- Terrain: a real area and licensed DEM, or keep the illustrative model.
- A naming and trademark check by a qualified adviser.
- A resemblance search on the final pixel wordmark. Pixel wordmarks are common in technology brands, and the KURATE reference itself should be compared against.
- The Brace screenshot, if it is still relevant.

## Round 2 — logo design (2 October 2026)

`working/round-2/HCO-Logo-Round-2.pdf` contains 16 boards at 1600 × 1000 px. PNGs at 1920 × 1200 are in `round-2/boards/`.

- **Defaults taken because the brief's open questions are unanswered:** illustrative procedural terrain (no region confirmed); HCO and High Country Observations as the names; both wordmark options tested.
- **Palette changes from brief v2, measured:**
  - Lichen moves from #D6E65D (Study 01) to a mineral #C9D36E: 10.06:1 on Basalt, 1.47:1 on Chalk. This addresses the "volt" trend risk.
  - Sage moves from #6F8E7A to #72907C: 4.63:1 on Basalt. The old value was 4.498:1, which displayed as 4.50 but failed AA.
- **Process:**
  - 2,379 candidates were sampled from terrain (580 plan rasters, 497 ridge profiles, 1,302 contour rings) and filtered against the brief.
  - 25 were drawn by hand, and 3 studies went forward: S1 Massif (plan raster), S2 Observation (plan raster with a Flag cell) and S3 Ridgeline (profile line).
  - Contour rings were rejected because they read as eyes or Pac-Man, which the brief rules out.
  - The brief's plan-view hypothesis was revised: a profile survives the traps once it plots the surface line instead of the mass.
- **Recommendation:** S3 Ridgeline with W1 High Bar.
  - Module M = 200 units = one cell = one stem. Cap height = 5M.
  - The crossbar fills row 4 of 5 (centre 70%, thickness 164). The H is 4M wide.
  - The gap between symbol and wordmark is 1M. The symbol is 8 × 5 cells and stands on the baseline.
  - The descriptor is set to the width of HCO, with its baseline 1.5M below. Clear space is 2M.
  - W2 (grid-built) is rejected because it reads as a game or display face.
- **Resemblance search** (recorded; not trademark clearance):
  - Stock "pixel mountain" logos are common, e.g. logomood.com/downloads/pixel-mountain and vecteezy pixel-mountain. This weighs against S1 and S2.
  - No close match was found for a single-cell pixel ridgeline.
  - Naming flag: "High Country" is also a Chevrolet Silverado trim and the name of High Country Outfitters (an outdoor retailer). Check the name before release.
- **Artwork:** `round-2/marks/`
  - outlined SVG symbols, lockups (with descriptor / compact), stacked versions (S3) and wordmarks
  - pixel-perfect favicons on a Basalt tile at 16/24/32/180/512 px (integer cell sizes)
  - These are review artwork, not the final export set.
- **Rebuild:** `cd working/round-2`, then run each in turn: `python3 terrain.py`, `python3 backgrounds.py 11`, `python3 explore.py`, `python3 explore_contour.py`, `python3 marks.py`, `python3 build_deck.py`, then `node ../tools/pages.mjs deck.html boards board 1.2 HCO-Logo-Round-2.pdf`. Needs numpy and the fonts in `working/fonts-ofl`.
- **Next, on approval:** refine the chosen artwork, build the full logo family and exports, then write the five-page identity pack.

## Logo brief v2 — “The mountain, measured” (2 October 2026)

The user asked for a new round: a coloured or conceptual background, the palette inside the logo, digitised mountains as background imagery, and a minimalist pixel-style symbol of data mapped onto terrain. The brief is in `brief-v2/`:

- `HCO-Logo-Brief-v2.pdf` (9 pages) and `HCO-Logo-Brief-v2.md` (the same content, agent-readable). Both are generated from `content.py` by `build_brief.py`. The diagrams come from `diagrams.py`, using seeded procedural terrain that is illustrative, not real elevation data.
- References are in `brief-v2/refs/`: third-party work, kept for internal discussion only. Refs 2–5 were Display-P3 screenshots and are converted to sRGB for display (`assets/ref*-display.png`). Study 01 is sRGB, and its measured colours are lime #D6E65D, field #0C2425 and wordmark #F5F6EE.
- `logosystem.co/logo/brace` is blocked by this environment's network policy; a screenshot has been requested.
- Key findings: (1) sampled side-on, a mountain becomes a ziggurat or a bar chart, so sample from above; (2) Study 01's symbol has a 0.8 px module at 16 px; (3) Lichen on Chalk measures 1.25:1, so the full-colour symbol must sit on Basalt; (4) Flag was nudged to #EC5D2F to reach 4.77:1 on Basalt.
- Rebuild: `cd working/brief-v2 && python3 diagrams.py && python3 build_brief.py && node ../tools/pages.mjs brief.html brief-png brief 1.6 HCO-Logo-Brief-v2.pdf` (needs numpy).

## Source material

The client's two references arrived as images in the conversation. They were not saved into the repository, so they are described here.

- **Existing logo.** Gold on black. A sketchy three-peak mountain line drawing with horizontal rules either side, over “HCO” set in a classical high-contrast serif, with “HIGH COUNTRY OBSERVATIONS GROUP” in spaced capitals beneath.
- **Flyer.** Generated photography (farmer with tablet, drone, mountains, crop rows, tractor, pickup), dark green and gold, distressed condensed headlines and a stock icon set. Its copy is the most useful input:
  - Intro: “HCO helps farmers, ranchers, and agricultural businesses solve business, regulatory, and field problems. We show up, learn the operation, identify the issue, and give you practical options for what to do next.”
  - **Business & operations:** Regulatory & compliance (agriculture, land use, environmental, food and operating requirements); Business decisions (expansion, equipment purchases, new revenue opportunities, partnerships); Contracts & vendors (pricing, obligations, terms, risks); Markets & supply chains (buyers, suppliers, distribution, pricing, weak points).
  - **Field & property intelligence:** Drone mapping (“high-resolution and multispectral imagery”); Crop health & problem areas (“NDVI/NDRE and field imagery to prioritize scouting”); Farm & ranch mapping (irrigation, fences, roads, drainage, facilities); Repeat monitoring; Clear reports (maps, observations, priority areas, practical next steps).
  - Values: “We actually show up.” · “Your operation comes first.” · “Practical. Not theory.” · “Start with the problem.”
  - Line: “Understand systems. Protect people.”
  - Footer: “HCO CONSULTING — Agriculture • Ranching • Rural Business • Field Intelligence”, plus a phone number and email address.

## Items that need confirmation before release

1. **Name.** The logo says “High Country Observations **Group**”; the flyer says “High Country Observations **Consulting**” and “HCO Consulting”. Working assumption: **HCO** (principal), **High Country Observations** (expanded), **Consulting** (optional descriptor). No parent company, subsidiaries or legal entity name has been invented.
2. **Contact details.** The flyer's phone number and email are deliberately **not used** in any design work. The email is on a default Microsoft 365 tenant domain (`…onmicrosoft.com`); a branded domain is worth setting up before release. None has been invented.
3. **Location.** Nothing in the brief states one, so no location is used or implied. The 720 area code on the flyer is not treated as evidence of a service area.
4. **Capabilities.** “Multispectral”, “NDVI/NDRE” and “mapping” are used only as working vocabulary. Nothing implies licensed surveying, agronomy credentials, legal representation or certifications.
5. **Tagline.** “Understand systems. Protect people.” is kept as an optional communications line, not fixed to any logo. “Grounded intelligence” is the internal territory, not a public line.
6. **Fonts.** See `font-audit/font-inventory.md`. Premium families are not reachable from this environment. Direction A uses open-licence Instrument Sans, pending approval.

## Concept routes — summary

| Route | Idea | Chief weakness | Artwork |
|---|---|---|---|
| **1 · High Bar** (custom typographic) — *recommended* | Custom-drawn HCO whose H crossbar sits high (centre at 71.5% of cap height): the horizon seen from high ground. The same proportion becomes the layout rule, 28.5% from the top of any format. | The idea lives in one detail and needs the system to be noticed; any higher and it becomes an Art Deco mannerism. | `concepts/marks/r1-*` |
| **2 · Rise** (land and observation) | One bent line that reads as a field boundary from above and as ground rising to high country from the side: plan and section. | Can read as a step chart or stair; rising-line marks are common in consulting. | `concepts/marks/r2-*` |
| **3 · The Point** (alternative) | HCO's product is clarity. A serif name closed by a square point, which also marks observations on maps and flags next steps. | Full-stop wordmarks are familiar; the compact “H.” is weak at 16 px. | `concepts/marks/r3-*` |

### Top five, ranked (`concepts/HCO-Top-5-Concepts.pdf`)

1. **High Bar** (21/25): recommended.
2. **Ground Truth** (19/25, new). The two-square ground-control target used in drone mapping to pin aerial imagery to real positions, paired with Instrument Sans HCO. It is the best at 16 px, but the geometry is common. Risks: a racing flag if repeated; implied surveying services HCO does not offer. Artwork: `concepts/marks/r4-*`.
3. **Rise** (17/25).
4. **Horizon Line** (14/25, new). The evolution route: the horizon kept, the peak and gold dropped, and a sturdy serif HCO in Source Serif 4 under one line that runs to the format edge. It is the least distinctive. Artwork: `concepts/marks/r5-*`.
5. **The Point** (13/25).

Ratings are designer judgement from the artwork and pixel tests, not measured data. Rebuild with `python3 geometry/routes_top5.py`, then `python3 concepts/px_tests.py`, then `python3 concepts/build_top5.py`, then `node tools/pages.mjs concepts/top5-concepts.html concepts/top5-png top5 1.6 concepts/HCO-Top-5-Concepts.pdf`. Run each from its own folder, as with Stage 1.

**Rejected in exploration** (see `sketches/`): square or horizon icons (they read as UI window icons); circle-in-square “pivot” (reads as a lens or target, which the brief rules out); ox-turn/boustrophedon line (reads as “2” or the CJK character 己); stacked soil-horizon bands (a hamburger/layers icon); high-bar H inside a square (a hospital or helipad sign).

An idea kept for Stage 2 copy, not the logo: in FAO soil description, **H, O and C are all soil-horizon designations**. It is a genuine double meaning of “horizon” — the skyline and the layers underfoot. It is not used literally, because the H–C–O order is not a real soil profile. Verify against the FAO Guidelines for Soil Description before any public use.

## Route 1 geometry (current state)

Built parametrically in `geometry/routes.py`. Units: cap height = 1000.

- H: width 820, stem 194, crossbar 138 thick, centred at 715.
- C: width 880, sides 200, top/bottom 160, overshoot 12, aperture cut 290–715.
- O: width 935, sides 204, top/bottom 160, Bézier handle ratios 0.61 outer / 0.64 inner.
- Spacing: H–C 94, C–O 62. The outline has 65 points (clean Bézier, no tracing).
- Lockup: “High Country / Observations” in Instrument Sans 560, outlined. It hangs from the underside of the crossbar (y = 646) and stands on the baseline.

Refinement still needed if approved: optical overshoot check on C/O, C terminal angle and aperture, contrast at the H joins, a small-size cut of the compact H, and spacing reviewed at 16–32 px.

## Resemblance check

Not yet done. It will be carried out on the approved mark in Stage 2, and the references reviewed will be listed. This is not trademark clearance.

## Rebuilding Stage 1

```bash
cd working/fonts-ofl && ./fetch.sh schibstedgrotesk sourceserif4 hankengrotesk instrumentsans monasans archivo hostgrotesk familjengrotesk newsreader sourceserif4 literata besley ibmplexsans ibmplexmono chivo chivomono publicsans atkinsonhyperlegiblenext atkinsonhyperlegiblemono barlow barlowsemicondensed intertight geist geistmono redhattext redhatmono
pip install fonttools uharfbuzz skia-pathops cairosvg pillow pymupdf
cd ../geometry && python3 routes.py            # outlined SVG marks → concepts/marks/
cd ../concepts && python3 px_tests.py          # true-pixel tests → concepts/px/
python3 build_review.py                        # → concept-review.html
node ../tools/pages.mjs concept-review.html review-png review 1.6 HCO-Concept-Review.pdf
```

Requires Node with Playwright and Chromium (`/opt/node22/lib/node_modules/playwright` in this environment; adjust the path in `tools/*.mjs` elsewhere).
