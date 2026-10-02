# Groundwork — HCO design system (v0.1, for review)

A static review site for the HCO design system. It has no build step and no framework: plain HTML, CSS and JavaScript.

## Publishing on the review site

1. Upload the contents of this folder to a path of its own, for example `/hco/`. Keep the folder structure: every link is relative.
2. The entry point is `index.html`.
3. Every page carries `<meta name="robots" content="noindex, nofollow">`. The site is a working draft for review and is not for public release.

## Pages

**Documentation:** Overview, Principles, Brand, Colour, Typography, Layout and space, Motion, Icons, Maps and charts, Capture and bands, Components, Voice and words, Tokens and downloads.

**Templates:** `portal.html` (client portal), `report.html` (field report, which prints to A4), `app.html` (field app), `website.html` and `email.html`.

## Dependencies

- **Typeface.** Instrument Sans, loaded from Google Fonts (SIL Open Font License 1.1). No font files are included in this folder.
- **Monospace text.** Uses the reader's own system font; nothing is downloaded.
- **Browsers.** Current Chrome, Edge, Firefox and Safari.
- **External services.** None other than Google Fonts. Forms in the templates do not send anything.

## Data

All maps, figures, flights and observations are illustrative and procedurally generated. No client, property or result is depicted. Contact details are bracketed placeholders.

## Files

- `assets/tokens/tokens.css`, `tokens.json`: design tokens.
- `assets/css/groundwork.css`: components. `docs.css` and `templates.css` style this site.
- `assets/js/groundwork.js`: pixel figures, tabs, switches, dialogs and toasts.
- `assets/js/fieldmap.js`, `ridges.js`: the map and ridgeline canvases.
- `assets/icons/`: 82 icons, as `sprite.svg` and as individual SVGs.
- `assets/logos/`: signature artwork (SVG).
- `assets/data/`: illustrative datasets, in both JSON and JS form.

The site is generated from the HCO project repository (`working/design-system/`). See the project notes there for how to rebuild it.
