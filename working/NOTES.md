# HCO identity — internal working notes

_Working folder only. Nothing here goes into the client handover ZIP._
_Stage 1 (exploration) — 28 September 2026._

## Status

| Stage | State |
|---|---|
| 1 · Concept routes and type directions | **Presented for approval**: `concepts/HCO-Concept-Review.pdf` (11 pages, three routes and type directions) and `concepts/HCO-Top-5-Concepts.pdf` (8 pages, five concepts ranked). Previews are in `concepts/review-png/` and `concepts/top5-png/` |
| 2 · Identity system, five-page pack, exports and QA | **Not started.** Waiting for route, type and naming decisions. The brief says not to finalise the book around an unapproved logo. |

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
