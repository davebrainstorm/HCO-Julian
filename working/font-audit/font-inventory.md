# Font audit — HCO identity (internal working note)

_Not client-facing. Last run: 28 September 2026._

## 1. Where this work is running

| Item | Finding |
|---|---|
| Environment | **Remote** Claude Code session in a cloud Linux container (Ubuntu 24.04.4 LTS, x86_64). It is **not** the designer's computer. |
| macOS font folders named in the brief | `~/Library/Fonts`, `/Library/Fonts`, `/System/Library/Fonts` — **do not exist here**. Fonts installed on your Mac cannot be seen or used from this session. |
| Project font folder | None. The repository was empty when the session started. |
| Method | Every font file in `/usr/share/fonts`, `/usr/local/share/fonts`, `~/.fonts` and `~/.local/share/fonts` was opened with fontTools and its `name`, `OS/2`, `fvar` and `GSUB` tables were read (not file names). Script: `audit_fonts.py`; raw output: `system-font-inventory.json`. |

## 2. System fonts found

None of these is suitable for a premium identity. They are listed for completeness.

| Family | Styles (OS/2 weight) | Variable axes | Location |
|---|---|---|---|
| DejaVu Sans | Bold (700), Book (400) | — | `/usr/share/fonts/truetype/dejavu` |
| DejaVu Sans Mono | Bold (700), Bold Oblique (700), Book (400), Oblique (400) | — | `/usr/share/fonts/truetype/dejavu` |
| DejaVu Serif | Bold (700), Book (400) | — | `/usr/share/fonts/truetype/dejavu` |
| FreeMono | Bold (700), Bold Oblique (700), Oblique (400), Regular (400) | — | `/usr/share/fonts/truetype/freefont` |
| FreeSans | Bold (600), Bold Oblique (600), Oblique (400), Regular (400) | — | `/usr/share/fonts/truetype/freefont` |
| FreeSerif | Bold (700), Bold Italic (700), Italic (400), Regular (400) | — | `/usr/share/fonts/truetype/freefont` |
| IPAGothic | Regular (400) | — | `/usr/share/fonts/opentype/ipafont-gothic` |
| IPAPGothic | Regular (400) | — | `/usr/share/fonts/opentype/ipafont-gothic` |
| Liberation Mono | Bold (700), Bold Italic (700), Italic (400), Regular (400) | — | `/usr/share/fonts/truetype/liberation` |
| Liberation Sans | Bold (700), Bold Italic (700), Italic (400), Regular (400) | — | `/usr/share/fonts/truetype/liberation` |
| Liberation Serif | Bold (700), Bold Italic (700), Italic (400), Regular (400) | — | `/usr/share/fonts/truetype/liberation` |
| Loma | Bold (700), Bold Oblique (700), Oblique (400), Regular (400) | — | `/usr/share/fonts/opentype/tlwg` |
| Noto Color Emoji | Regular (400) | — | `/usr/share/fonts/truetype/noto` |
| OpenSymbol | Regular (400) | — | `/usr/share/fonts/truetype/libreoffice` |
| Unifont | Regular (400) | — | `/usr/share/fonts/opentype/unifont` |
| Unifont CSUR | Regular (400) | — | `/usr/share/fonts/opentype/unifont` |
| Unifont Sample | Regular (400) | — | `/usr/share/fonts/opentype/unifont` |
| Unifont Upper | Regular (400) | — | `/usr/share/fonts/opentype/unifont` |
| Unifont-JP | Regular (400) | — | `/usr/share/fonts/opentype/unifont` |
| WenQuanYi Zen Hei | Regular (500) | — | `/usr/share/fonts/truetype/wqy` |
| WenQuanYi Zen Hei Mono | Regular (500) | — | `/usr/share/fonts/truetype/wqy` |
| WenQuanYi Zen Hei Sharp | Regular (500) | — | `/usr/share/fonts/truetype/wqy` |
| Bitstream Charter, Courier 10 Pitch | 8 Type 1 files | — | `/usr/share/fonts/X11/Type1` (legacy PostScript) |

## 3. Premium families requested in the brief

| Family | Status here |
|---|---|
| Söhne, Söhne Mono | Not installed |
| GT America | Not installed |
| Graphik | Not installed |
| Neue Haas Grotesk / Neue Haas Unica | Not installed locally. **Neue Haas Grotesk Display Pro and Text Pro (Monotype; designer Christian Schwartz) are listed in the Adobe Fonts library of the connected Adobe account.** They cannot be used here: `use.typekit.net` and `p.typekit.net` are unreachable under this environment's network policy, and Adobe Fonts cannot be downloaded as files. No kit was created, because that would change the user's Adobe account. |
| Suisse Int'l, Suisse Works | Not installed |
| Founders Grotesk | Not installed |
| Tiempos (Headline / Text) | Not installed |

**Result:** the premium typography requirement **cannot be completed in this environment.** The concept stage uses open-licence families, labelled as such everywhere they appear. They are not substitutes passed off as the premium families.

## 4. Open-licence families fetched for audition

Fetched from the public `google/fonts` source repository with `working/fonts-ofl/fetch.sh`. These are complete, unsubsetted builds under SIL Open Font License 1.1. The files are **git-ignored and never packaged**: re-run `fetch.sh` to restore them. Rendering was verified in headless Chromium (Playwright): every face used reports `document.fonts` status `loaded`, and each was inspected visually on the audition sheets in `working/type-audition/`.

| Family | File | Weights / axes | Italic | Relevant OpenType features |
|---|---|---|---|---|
| Archivo | `archivo/Archivo-Italic[wdth,wght].ttf` | wght 100–900, wdth 62–125 | yes | tnum pnum lnum onum case zero frac |
| Archivo | `archivo/Archivo[wdth,wght].ttf` | wght 100–900, wdth 62–125 | — | tnum pnum lnum onum case zero frac |
| Atkinson Hyperlegible Mono | `atkinsonhyperlegiblemono/AtkinsonHyperlegibleMono-Italic[wght].ttf` | wght 200–800 | yes | case zero frac |
| Atkinson Hyperlegible Mono | `atkinsonhyperlegiblemono/AtkinsonHyperlegibleMono[wght].ttf` | wght 200–800 | — | case zero frac |
| Atkinson Hyperlegible Next | `atkinsonhyperlegiblenext/AtkinsonHyperlegibleNext-Italic[wght].ttf` | wght 200–800 | yes | tnum pnum case frac |
| Atkinson Hyperlegible Next | `atkinsonhyperlegiblenext/AtkinsonHyperlegibleNext[wght].ttf` | wght 200–800 | — | tnum pnum case frac |
| Barlow | `barlow/Barlow-Black.ttf` | static 900 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-BlackItalic.ttf` | static 900 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Bold.ttf` | static 700 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-BoldItalic.ttf` | static 700 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-ExtraBold.ttf` | static 800 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-ExtraBoldItalic.ttf` | static 800 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-ExtraLight.ttf` | static 275 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-ExtraLightItalic.ttf` | static 275 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Italic.ttf` | static 400 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Light.ttf` | static 300 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-LightItalic.ttf` | static 300 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Medium.ttf` | static 500 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-MediumItalic.ttf` | static 500 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Regular.ttf` | static 400 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-SemiBold.ttf` | static 600 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-SemiBoldItalic.ttf` | static 600 | yes | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-Thin.ttf` | static 250 | — | tnum pnum frac smcp |
| Barlow | `barlow/Barlow-ThinItalic.ttf` | static 250 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Black.ttf` | static 900 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-BlackItalic.ttf` | static 900 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Bold.ttf` | static 700 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-BoldItalic.ttf` | static 700 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-ExtraBold.ttf` | static 800 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-ExtraBoldItalic.ttf` | static 800 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-ExtraLight.ttf` | static 275 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-ExtraLightItalic.ttf` | static 275 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Italic.ttf` | static 400 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Light.ttf` | static 300 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-LightItalic.ttf` | static 300 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Medium.ttf` | static 500 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-MediumItalic.ttf` | static 500 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Regular.ttf` | static 400 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-SemiBold.ttf` | static 600 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-SemiBoldItalic.ttf` | static 600 | yes | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-Thin.ttf` | static 250 | — | tnum pnum frac smcp |
| Barlow Semi Condensed | `barlowsemicondensed/BarlowSemiCondensed-ThinItalic.ttf` | static 250 | yes | tnum pnum frac smcp |
| Besley | `besley/Besley-Italic[wght].ttf` | wght 400–900 | yes | tnum onum ss01 |
| Besley | `besley/Besley[wght].ttf` | wght 400–900 | — | tnum onum ss01 |
| Chivo | `chivo/Chivo-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum lnum onum case zero frac |
| Chivo | `chivo/Chivo[wght].ttf` | wght 100–900 | — | tnum pnum lnum onum case zero frac |
| Chivo Mono | `chivomono/ChivoMono-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum lnum onum case zero frac |
| Chivo Mono | `chivomono/ChivoMono[wght].ttf` | wght 100–900 | — | tnum pnum lnum onum case zero frac |
| Familjen Grotesk | `familjengrotesk/FamiljenGrotesk-Italic[wght].ttf` | wght 400–700 | yes | tnum pnum case zero frac ss02 |
| Familjen Grotesk | `familjengrotesk/FamiljenGrotesk[wght].ttf` | wght 400–700 | — | tnum pnum case zero frac ss02 |
| Geist | `geist/Geist-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum case frac ss01 ss02 |
| Geist | `geist/Geist[wght].ttf` | wght 100–900 | — | tnum pnum case frac ss01 ss02 |
| Geist Mono | `geistmono/GeistMono-Italic[wght].ttf` | wght 100–900 | yes | case frac ss02 |
| Geist Mono | `geistmono/GeistMono[wght].ttf` | wght 100–900 | — | case frac ss01 ss02 |
| Hanken Grotesk | `hankengrotesk/HankenGrotesk-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum case frac ss01 ss02 |
| Hanken Grotesk | `hankengrotesk/HankenGrotesk[wght].ttf` | wght 100–900 | — | case frac ss01 ss02 |
| Host Grotesk | `hostgrotesk/HostGrotesk-Italic[wght].ttf` | wght 300–800 | yes | case frac ss02 |
| Host Grotesk | `hostgrotesk/HostGrotesk[wght].ttf` | wght 300–800 | — | case frac ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Bold.ttf` | static 700 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-BoldItalic.ttf` | static 700 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-ExtraLight.ttf` | static 200 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-ExtraLightItalic.ttf` | static 200 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Italic.ttf` | static 400 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Light.ttf` | static 300 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-LightItalic.ttf` | static 300 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Medium.ttf` | static 500 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-MediumItalic.ttf` | static 500 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Regular.ttf` | static 400 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-SemiBold.ttf` | static 600 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-SemiBoldItalic.ttf` | static 600 | yes | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-Thin.ttf` | static 100 | — | zero frac ss01 ss02 |
| IBM Plex Mono | `ibmplexmono/IBMPlexMono-ThinItalic.ttf` | static 100 | yes | zero frac ss01 ss02 |
| IBM Plex Sans | `ibmplexsans/IBMPlexSans-Italic[wdth,wght].ttf` | wght 100–700, wdth 75–100 | yes | lnum onum zero frac ss01 ss02 |
| IBM Plex Sans | `ibmplexsans/IBMPlexSans[wdth,wght].ttf` | wght 100–700, wdth 75–100 | — | lnum onum zero frac ss01 ss02 |
| Instrument Sans | `instrumentsans/InstrumentSans-Italic[wdth,wght].ttf` | wdth 75–100, wght 400–700 | yes | tnum pnum case ss01 ss02 |
| Instrument Sans | `instrumentsans/InstrumentSans[wdth,wght].ttf` | wdth 75–100, wght 400–700 | — | tnum pnum case ss01 ss02 |
| Inter Tight | `intertight/InterTight-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum case zero frac ss01 ss02 |
| Inter Tight | `intertight/InterTight[wght].ttf` | wght 100–900 | — | tnum pnum case zero frac ss01 ss02 |
| Literata | `literata/Literata-Italic[opsz,wght].ttf` | opsz 7–72, wght 200–900 | yes | tnum pnum lnum onum case zero frac smcp ss01 ss02 |
| Literata | `literata/Literata[opsz,wght].ttf` | opsz 7–72, wght 200–900 | — | tnum pnum lnum onum case zero frac smcp ss01 ss02 |
| Mona Sans | `monasans/MonaSans-Italic[wdth,wght].ttf` | wdth 75–125, wght 200–900 | yes | tnum pnum case frac ss01 ss02 |
| Mona Sans | `monasans/MonaSans[wdth,wght].ttf` | wdth 75–125, wght 200–900 | — | tnum pnum case frac ss01 ss02 |
| Newsreader | `newsreader/Newsreader-Italic[opsz,wght].ttf` | wght 200–800, opsz 6–72 | yes | tnum pnum case |
| Newsreader | `newsreader/Newsreader[opsz,wght].ttf` | wght 200–800, opsz 6–72 | — | tnum pnum case |
| Public Sans | `publicsans/PublicSans-Italic[wght].ttf` | wght 100–900 | yes | tnum pnum lnum onum frac ss01 |
| Public Sans | `publicsans/PublicSans[wght].ttf` | wght 100–900 | — | tnum pnum lnum onum frac ss01 |
| Red Hat Mono | `redhatmono/RedHatMono-Italic[wght].ttf` | wght 300–700 | yes | case zero frac ss01 ss02 |
| Red Hat Mono | `redhatmono/RedHatMono[wght].ttf` | wght 300–700 | — | case zero frac ss01 ss02 |
| Red Hat Text | `redhattext/RedHatText-Italic[wght].ttf` | wght 300–700 | yes | tnum pnum case zero frac ss01 ss02 |
| Red Hat Text | `redhattext/RedHatText[wght].ttf` | wght 300–700 | — | tnum pnum case zero frac ss01 ss02 |
| Schibsted Grotesk | `schibstedgrotesk/SchibstedGrotesk-Italic[wght].ttf` | wght 400–900 | yes | tnum pnum case zero frac |
| Schibsted Grotesk | `schibstedgrotesk/SchibstedGrotesk[wght].ttf` | wght 400–900 | — | tnum pnum case zero frac |
| Source Serif 4 | `sourceserif4/SourceSerif4-Italic[opsz,wght].ttf` | wght 200–900, opsz 8–60 | yes | tnum pnum lnum onum case zero frac ss01 ss02 |
| Source Serif 4 | `sourceserif4/SourceSerif4[opsz,wght].ttf` | wght 200–900, opsz 8–60 | — | tnum pnum lnum onum case zero frac smcp ss01 ss02 |

Barlow and Barlow Semi Condensed were fetched but not carried into the auditions.

## 5. Shortlist and reasons

| Direction | Chosen | Why | Rejected in this role, and why |
|---|---|---|---|
| A — Clear authority (one grotesk family) | **Instrument Sans**: wdth 75–100, wght 400–700, true italics, `tnum` `case` `ss01` `ss02` | Crisp, confident headline shapes; clean tabular figures; a condensed width for labels without a second family. | **Schibsted Grotesk**: its `tnum` makes the full stop and comma tabular, giving “148 . 6” (seen on the first concept board, then replaced). **Mona Sans**: slashed zero in tabular figures. **Archivo / Chivo**: idiosyncratic ampersand in the key phrase “Field & Operations”. **Hanken Grotesk**: roman has no `tnum`. **Host Grotesk**: no `tnum`. **Geist**: tech-product associations. **Inter Tight**: ubiquitous. |
| B — Editorial judgement (serif + sans) | **Newsreader** (opsz 6–72, wght 200–800, italics) with **Public Sans** (wght 100–900, italics, `tnum` `lnum` `onum`) | Newsreader is an editorial serif with optical sizes, restrained but with character. Public Sans is plain and highly legible for labels and data. | **Source Serif 4**: sound, but less character. **Literata**: bookish. **Besley**: Clarendon nostalgia. |
| C — Field precision (technical sans + mono) | **IBM Plex Sans** (wdth 75–100, wght 100–700, italics; figures tabular by default) with **IBM Plex Mono** | Engineered detail, excellent numerals, a condensed width, and a mono companion for data labels. | **Red Hat Text/Mono**: friendly-geometric. **Atkinson Hyperlegible Next**: idiosyncratic figures. **Geist Mono**: tech-product associations. Plex carries an IBM association; this is recorded as a risk. |

## 6. Licensing questions (unresolved)

1. **Open-licence route.** SIL OFL 1.1 permits desktop use, PDF embedding, web use and redistribution with the licence. Per the brief, font files are still never bundled into deliverables. Document where to download them instead.
2. **Premium route.** Desktop availability does not grant web or embedding rights. HCO would need its own licences for desktop (brand and admin staff), web (site traffic tier) and possibly Office/app use. Adobe Fonts rights belong to the subscriber, not the client.
3. **PDF embedding in the final pack.** Chromium embeds *variable* fonts as Type 3 (text stays selectable, glyphs stay vector). For the final pack, static instances should be generated locally with the fontTools instancer (not committed), so fonts embed as TrueType subsets.
