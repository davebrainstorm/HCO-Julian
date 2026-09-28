# HCO identity — internal working notes

_Working folder only. Nothing here goes into the client handover ZIP._
_Stage 1 (exploration) — 28 September 2026._

## Status

| Stage | State |
|---|---|
| 1 · Concept routes and type directions | **Presented for approval**: `concepts/HCO-Concept-Review.pdf` (11 pages), previews in `concepts/review-png/` |
| 2 · Identity system, five-page pack, exports and QA | **Not started.** Waiting for route, type and naming decisions. The brief says not to finalise the book around an unapproved logo. |

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
cd working/fonts-ofl && ./fetch.sh schibstedgrotesk hankengrotesk instrumentsans monasans archivo hostgrotesk familjengrotesk newsreader sourceserif4 literata besley ibmplexsans ibmplexmono chivo chivomono publicsans atkinsonhyperlegiblenext atkinsonhyperlegiblemono barlow barlowsemicondensed intertight geist geistmono redhattext redhatmono
pip install fonttools uharfbuzz skia-pathops cairosvg pillow pymupdf
cd ../geometry && python3 routes.py            # outlined SVG marks → concepts/marks/
cd ../concepts && python3 px_tests.py          # true-pixel tests → concepts/px/
python3 build_review.py                        # → concept-review.html
node ../tools/pages.mjs concept-review.html review-png review 1.6 HCO-Concept-Review.pdf
```

Requires Node with Playwright and Chromium (`/opt/node22/lib/node_modules/playwright` in this environment; adjust the path in `tools/*.mjs` elsewhere).
