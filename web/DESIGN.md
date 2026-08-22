---
name: SoDA Lab
description: A conference poster hall — slate board fabric carrying white poster stock, where a paper's size is its citation count.
colors:
  hall: "#eaeae7"
  paper: "#f6f6f3"
  paper-2: "#e2e2dd"
  board: "#46525c"
  ink: "#14181b"
  ink-soft: "#4a545c"
  ink-faint: "#5e6870"
  rule: "#d5d3cc"
  accent: "#990000"
  accent-deep: "#7d0000"
  topic-online-harm: "#dc2626"
  topic-news-journalism: "#57534e"
  topic-user-behavior: "#d97706"
  topic-beliefs-opinions: "#7c3aed"
  topic-llms-responsible-ai: "#4f46e5"
  topic-bias-fairness: "#0d9488"
  topic-networks-influence: "#0284c7"
  topic-digital-health: "#db2777"
typography:
  display:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(38px, 5.6vw, 68px)"
    fontWeight: 600
    lineHeight: 1.06
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(30px, 4.2vw, 46px)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.32
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Literata, Georgia, 'Times New Roman', serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  body-ui:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "tabular-nums"
  meta:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "tabular-nums"
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.14em"
rounded:
  none: "0"
  focus: "1px"
spacing:
  page-x: "24px"
  page-y: "40px"
  board-standard: "24px"
  board-major: "30px"
  board-landmark: "38px"
  masthead-y: "40px"
components:
  board-standard:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "24px 24px 22px"
  board-major:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "30px 30px 28px"
  board-landmark:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "38px 38px 35px"
  board-tag:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.2rem 0.45rem"
  action-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.7rem 1.15rem"
  action-primary-hover:
    backgroundColor: "{colors.accent-deep}"
    textColor: "{colors.paper}"
  action-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.7rem 1.15rem"
  action-secondary-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  nav-item:
    backgroundColor: "transparent"
    textColor: "color-mix(in srgb, #f6f6f3 72%, transparent)"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "10px 12px"
  nav-item-current:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    padding: "10px 12px"
  filter-chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.3rem 0.6rem"
    size: "12px"
  filter-chip-on:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    padding: "0.3rem 0.6rem"
  track-swatch:
    rounded: "{rounded.none}"
    width: "0.65rem"
    height: "0.65rem"
  masthead:
    backgroundColor: "{colors.board}"
    textColor: "{colors.paper}"
    typography: "{typography.headline}"
    rounded: "{rounded.none}"
    padding: "40px 24px"
  notice-head:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.45rem 1.15rem"
  stamp-open:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.1rem 0.4rem"
  stamp-closed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.1rem 0.4rem"
---

# Design System: SoDA Lab

## Overview

**Creative North Star: "The Poster Hall"**

The site is a conference poster session, not a publication ledger. Three
materials carry everything: the **hall floor** (`#eaeae7`) you stand on, the
**board fabric** (`#46525c`) you face, and the **poster stock** (`#f6f6f3`)
pinned to it. Nothing else is a surface. The page ground is always the floor;
a `.board` is only applied where a board actually stands (the header strip,
a page masthead, the home hero); `.stock` is only applied to a sheet that is
pinned to something. The fabric carries a real 3px weave built from two
`repeating-linear-gradient` layers, tight enough to read as material up close
and to flatten into a field from a distance — it is a material, never a
page-wide grain.

The system's one structural claim is that **size is meaning**. A publication
board's physical size is set by its citation count, so a landmark paper and a
workshop preprint are visibly not the same object from down the aisle. That
replaces the size ladder inside a single card: page-level hierarchy is carried
by the tier, not by stacking five type sizes inside one board.

Colour is rationed hard. IU crimson (`#990000`) is the only action colour and
the only colour the navigation strip is allowed; the eight research-topic hues
were demoted from decoration to **data** and appear exclusively as small
printed squares. Every corner is square. There is no monospace anywhere.

**Key Characteristics:**
- Three materials only: hall floor, board fabric, poster stock.
- Citation count sets board size (landmark / major / standard).
- One accent (IU crimson) for actions, board tags, and "you are here".
- Topic hues are swatches, never text.
- Zero border-radius; hairlines are inset rings, not borders.
- Archivo for signage and headings, Literata for reading. No monospace.
- Tabular figures globally — every number on the site is a measurement.

## Colors

A quarry palette: warm greys for the room, slate for the fabric, near-black
ink, and a single institutional crimson. The eight topic hues sit outside this
palette on purpose — they encode data, not mood.

### Primary
- **IU Crimson** (`#990000`): the one action colour. Primary buttons, the
  crimson board-number tag, the active nav destination, links inside prose and
  news items, the `Open` stamp, `::selection`, the caret, and the focus ring.
  It measures 8.24:1 on stock and 7.40:1 on the hall floor. Hover deepens to
  `#7d0000` (10.36:1).

### Neutral
- **Hall Floor** (`#eaeae7`): the page ground. `body` background, nothing else.
- **Poster Stock** (`#f6f6f3`): every sheet — publication boards, team cards,
  the news sidebar, filter controls, the footer, and the badge behind the lab
  mark. Also the type colour on fabric.
- **Stock in Shadow** (`#e2e2dd`): the empty bed behind an image that has not
  loaded or does not fill its frame (publication figures, press clippings).
- **Board Fabric** (`#46525c`): the header strip, the page masthead, the home
  hero band. Always full-bleed, never a container inside the reading column.
- **Ink** (`#14181b`): headings, board titles, lab-author names, and the ground
  of an inverted control (active filter chip, notice head, `Closed` stamp,
  the press caption strip). 16.49:1 on stock.
- **Ink Soft** (`#4a545c`): body copy, abstracts, author lists. 7.15:1 on stock.
- **Ink Faint** (`#5e6870`): metadata, counts, section labels, dates,
  placeholders. 5.26:1 on stock and 4.72:1 on the hall floor — the lightest
  ink that survives on both grounds.
- **Rule** (`#d5d3cc`): hairlines, control borders, section dividers, and the
  underline colour of a de-emphasised prose link.

### Tertiary — the eight track colours
Data, not decoration. One per research topic: online harm `#dc2626`, news &
journalism `#57534e`, user behavior `#d97706`, beliefs & opinions `#7c3aed`,
LLMs & responsible AI `#4f46e5`, bias & fairness `#0d9488`, networks &
influence `#0284c7`, digital health `#db2777`. They tell a visitor which
section of the hall a board stands in.

### Named Rules

**The Swatch-Only Rule.** A track colour may only be a filled square of at most
`0.65rem`, or the stroke of a line illustration. It is never text colour, never
a border, never a ground behind text. Audit test: five of the eight hues fail
WCAG AA as text on stock (`#d97706` 2.94:1, `#0d9488` 3.46:1, `#0284c7` 3.78:1,
`#db2777` 4.25:1, `#dc2626` 4.46:1), so the rule is not a preference — it is the
only way the taxonomy stays legible.

**The One Crimson Rule.** Crimson is the site's only chromatic accent. If a new
element needs to look important and is not an action, a board address, or the
current destination, it gets weight or inversion, not colour.

**The 4.5 Floor.** Every text-on-ground pair ships at 4.5:1 or better and the
measured number is recorded here. Paper at 72% over fabric (`#c5c8c9`, used for
nav destinations and the header tagline) sits at 4.76:1; the masthead lede uses
78% (5.26:1). An earlier tint failed AA and had to be replaced, so treat these
percentages as floors, not as styling knobs.

## Typography

**Display Font:** Archivo (with `system-ui`, `-apple-system`, `Segoe UI`, Roboto)
**Body Font:** Literata (with Georgia, Times New Roman) — applied via `.read`
**Label/Mono Font:** none. There is no monospace in this system.

**Character:** Archivo is hall signage — tight, weighted, slightly negative
tracking on anything large, wide positive tracking on anything small and
uppercase. Literata is what is actually printed on the sheet: a serif at a real
measure, for text a visitor stops to read. Both load from Google Fonts with
`display=swap` and a non-render-blocking preload.

### Hierarchy
- **Poster display** (600, `clamp(38px, 5.6vw, 68px)`, 1.06, `-0.035em`): the
  home hero statement only. `text-wrap: balance`. The research page runs its own
  hero at `clamp(44px, 6.2vw, 72px)` / `-0.02em`.
- **Masthead headline** (600, `clamp(30px, 4.2vw, 46px)`, 1.1, `-0.03em`): the
  page name on fabric, in paper.
- **Board title** (600, `-0.02em`, 1.32): 19px standard / 24px major / 32px
  landmark on desktop; 17 / 22 / 30px below 640px. `text-wrap: balance`.
- **Section heading** (600, 18–24px, `tracking-tight`): in-page section names
  on team, openings, and the home featured strip.
- **Reading body** (`.read`, Literata 400, 16px, 1.6, `max-width: 68ch`): lab
  statement, abstracts, research copy. Landmark boards raise the abstract to 18px.
- **UI body** (Archivo 400, 16px / 15px / 13px, 1.6): lists, metadata, author
  strings — anything that is scanned rather than read.
- **Label** (600–700, 11px, `0.14em`, uppercase): nav destinations, section
  labels, dates, the footer copyright, the filter disclosure, the notice head.
  The 11px/`0.14em` pairing is the house label; smaller tracking variants exist
  where the label sits inline with content (`0.1em` on the author strip and the
  track tag, `0.12em` on the research kicker and stamps, `0.08em` on the board
  tag).

### Named Rules

**The No-Mono Rule.** Years, citation counts, board numbers, and filter counts
are measurements, not code. `font-variant-numeric: tabular-nums` is set on
`html`, so Archivo's tabular figures align them in columns. Never introduce a
monospace face to make something look technical.

**The Two-Voice Rule.** Archivo speaks for the hall (signage, headings, labels,
controls); Literata speaks for the sheet (anything set with `.read`). A block
does not switch voice mid-way, and a caption never gets the serif.

**The 68ch Rule.** Reading text is capped at `68ch` by `.read`; the masthead
lede at `52ch`; the research hero lede at `36ch`. A paragraph that has no measure
cap is a bug.

## Layout

The reading column is `max-w-5xl` (64rem / 1024px) with `px-6` (24px) gutters
and `py-10` (40px) vertical padding, set once in `Base.astro`. Every page lines
up to that column, including the research page, which breaks out to full width
and then re-centres its own content at 64rem.

Fabric bands escape the column with `.board-bleed`
(`margin-inline: calc(50% - 50vw); width: 100vw`) while their content stays in
a nested `max-w-5xl` wrapper. `body` uses `overflow-x: clip` rather than
`hidden` so no new scroll container is created. A masthead or hero pulls itself
up with `-mt-10` to sit flush under the header.

Spacing follows Tailwind's 4px scale. Board padding is the density signal:
24px standard, 30px major, 38px landmark; boards stack with 20px between them.

Breakpoints in use: 640px (`sm`, and the publication-board media query), 720px
(the research page's own collapse to one column), 768px (`md`, where the nav
switches from a horizontal strip to a disclosure panel), 1024px (`lg`, where the
home page splits into content plus a 17rem press rail or a 19rem news rail).

Responsive behaviour worth knowing: below 640px every board hides its figure
except a landmark, which promotes its figure to a full-width 11rem band above
the title. A standard board's 72px crop was unreadable and stole the title's
measure, so only boards that earned the room keep one.

## Elevation & Depth

The system is flat except for one real object: a sheet of paper pinned to
fabric. `.stock` carries a two-layer shadow with genuine offset —
`0 1px 2px rgba(20,24,27,0.10)` for the contact edge and
`0 8px 20px -6px rgba(20,24,27,0.22)` for the lift. It is a cast shadow, not a
coloured halo, and it is the only `box-shadow` in the system that is used for
depth.

Everything else that looks like a border is an **inset ring** —
`box-shadow: inset 0 0 0 1px …` — so a hairline never changes an element's box
size: publication figures and team photos ring in `--color-rule`, the press
frame in `rgba(0,0,0,0.25)`, the openings notice and apply block in
`--color-rule`, and the secondary action in `inset 0 0 0 1.5px` of ink.

### Shadow Vocabulary
- **Pinned sheet** (`0 1px 2px rgba(20,24,27,0.10), 0 8px 20px -6px rgba(20,24,27,0.22)`):
  applied by `.stock` to anything that is a sheet of paper. Never to a button,
  a chip, or a fabric band.
- **Hairline ring** (`inset 0 0 0 1px var(--color-rule)`): image frames and
  bordered blocks where a real border would shift layout.

### Named Rules

**The Pinned-Sheet Rule.** Depth exists only where paper meets fabric. If a
surface is not a sheet, it is flat: filter chips, buttons, stamps, and nav
destinations get inversion or a 1px rule, never a shadow.

## Shapes

Everything is square. No component in the system sets a border-radius; the one
rounded value in the codebase is `border-radius: 1px` on `:focus-visible`, so
the 2px crimson outline does not clip a corner. Forms follow the same grammar:
the search field, sort select, filter buttons, and the "more filters" summary
are all 1px `--color-rule` rectangles on stock that darken their border to ink
on hover and invert to ink-on-paper when active.

The recurring silhouettes are printed objects: a crimson number tag offset
`-0.4rem / -0.6rem` past the board's top-left corner so it reads as applied
rather than contained; a solid ink head bar across the top of a notice; an
inline stamp before a status line; a caption strip printed in ink beneath a
press clipping. Research illustrations are open line art — `fill: none`,
`stroke: currentColor`, `stroke-width: 1.6` with 0.9 thin and 2.2 thick
variants and round caps — inheriting the section's track colour.

**The Square Rule.** Border-radius is 0. A rounded pill or a rounded card is
out of world; if an element needs to feel lighter, reduce its weight or its
contrast, not its corners.

## Components

### Buttons
- **Shape:** square (0 radius), 600 weight, `0.04em` tracking.
- **Primary** (`.act-primary`, `.apply-action`): crimson ground, paper text,
  `0.7rem 1.15rem` padding. Hover deepens to `#7d0000` over 0.15s.
- **Secondary** (`.act-secondary`): transparent with a 1.5px inset ink ring and
  ink text; hover inverts to ink ground / paper text.
- **Focus:** the global 2px crimson `:focus-visible` outline at 2px offset.
  Components do not define their own focus treatment.

### Chips
Two distinct chips, both square, both text-in-ink:
- **Track tag** (on a board, `.track-tag`): a `0.6rem` colour swatch followed by
  the topic name in 11px / `0.1em` uppercase ink-faint. It is an `<a href>` to
  `/publications?topic=…`; on the publications page itself the script calls
  `preventDefault()` and toggles the filter in place, syncing state to the URL.
- **Filter chip** (`.track-btn` / `.plain-btn`): stock ground, 1px rule border,
  12px ink label, a `0.65rem` swatch for topics only, and a tabular count in
  ink-faint. Hover darkens the border to ink. Active (`.is-on`) inverts to ink
  ground with paper text and a 70%-paper count. `.is-dashed` marks the
  "+ N more years" affordance.

### Cards / Containers
- **Corner style:** square.
- **Background:** `.stock` poster stock.
- **Shadow:** the pinned-sheet shadow (see Elevation).
- **Border:** none; images inside carry an inset hairline ring instead.
- **Internal padding:** 24 / 30 / 38px by tier for publication boards;
  20px for team cards and the news rail; 28–36px for the home statement sheet.

### Inputs / Fields
`.filter-field` — stock ground, 1px `--color-rule` border, 0.875rem ink text,
`0.5rem 0.7rem` padding, square. Placeholder in ink-faint. Hover darkens the
border to ink-faint. Focus uses the global crimson ring. The disclosure for
secondary filters is a `<details>` whose summary is styled as a label-cased
control with a CSS triangle chevron that rotates 180° when open; the native
marker is suppressed.

### Navigation
The header is a full-width fabric strip. The lab mark sits on a `2.75rem`
stock square — a badge printed on paper and pinned up. Destinations are 11px
uppercase `0.14em` labels in paper at 72%; hover raises them to full paper over
a 10% paper wash; the current destination gets a solid crimson block with paper
text, which is the hall's "you are here" and the only colour the strip carries.
Below 768px the strip collapses to a hamburger toggle and a stacked panel
separated by an 18%-paper hairline.

### Publication board (signature component)
The system's defining object. Tier is chosen from citation count —
`>= 500` landmark, `>= 100` major, otherwise standard — currently 5 / 25 / 109
of 139 boards. The tier changes padding, title size, figure size, and (on
landmark) author and abstract size; it does not change colour or shape. Lab
members' names inside the author string are bolded to ink; the venue is
italic; the metadata line is a single ink-faint run of venue · year · citations
in tabular figures.

**The Crowd Rule.** A board's size is its citation count and nothing else.
Never resize a board to promote it editorially — use `highlight` to feature it
and let the tier stand.

**The Unprinted Plate Rule.** 32 of 139 boards have no usable figure: the cron
lifts the first plate out of the PDF and sometimes there is nothing worth
lifting. Those boards render `.pub-figure.is-blank` at the tier's figure size —
stock in shadow, the same hairline ring, and the board's track swatch centred —
never a missing element. A board with no plate at all shunts its title left and
breaks the column every other board shares. The plate stays plain: an earlier
version hatched it with a repeating gradient, which the detector correctly
called a generated-UI signature. On mobile the plate follows the figure rule and
disappears except on landmark boards, where it sits at 6rem rather than the
11rem a real figure earns.

**The Unnumbered Host Rule.** The crimson `01`-style tag addresses *the work*.
The lab's own board on the home page deliberately carries no number; featured
boards are addressed from `01` upward.

### Masthead (signature component)
A full-bleed fabric band at the head of publications, team, and openings: the
page name in paper at `clamp(30px, 4.2vw, 46px)`, an optional lede at `52ch` in
paper at 78%. A page announces itself the way the hall entrance does, never
with a bare heading on the floor.

### Research section head and kicker
Section heads are a single horizontal row (`auto 1fr auto`): an optional 11px
uppercase label, a 1px rule that fills the gap, and the heading — laid out
across, never stacked.

**The Sub-Head Address Rule.** The numbered kicker (`<span class="num">` in
inverted ink plus the track name) sits *below* its `h3`, never above it. A small
label above a heading is banned outright; the same content reads as an address
when it follows the headline.

### Notice and stamps (openings)
A pinned official notice: stock ground with a hairline ring, a solid ink head
bar in label type, and one stamp per row — `Closed` in inverted ink, `Open` in
crimson. Status is stamped, never implied by absence and never by a coloured
left bar.

### Press clipping (home)
A clipping in an inset-ringed frame with an ink caption strip printed beneath
it: venue in 700, blurb in 66% paper, a tabular `n / N` position, and two
square 1.9rem step buttons that turn crimson on hover. It auto-advances every
6s, pauses on `mouseenter` **and** `focusin`, and does not start at all under
`prefers-reduced-motion: reduce`.

### Motion
Motion is a state response, never an entrance. Colour and border transitions
run 0.12–0.15s ease; the press track translates over 500ms ease-out; the filter
chevron rotates over 0.15s. Nothing animates on load, nothing parallaxes, and
the only autoplaying thing on the site checks the reduced-motion query first.

## Do's and Don'ts

### Do:
- **Do** put a new surface on one of the three materials: hall floor, `.board`
  fabric, or `.stock` paper. Anything else is out of world.
- **Do** bleed fabric to `100vw` with `.board-bleed` and keep its words in a
  nested `max-w-5xl px-6` wrapper.
- **Do** express a topic colour as a filled square of at most `0.65rem`, with
  the label beside it in `--color-ink` or `--color-ink-faint`.
- **Do** record the measured contrast ratio when introducing a new text/ground
  pair, and keep it at 4.5:1 or better.
- **Do** use `.read` for anything a visitor reads in sentences, and leave
  scanned text in Archivo.
- **Do** reach for weight, size, or inversion (ink ground / paper text) when
  something needs emphasis — that is this system's entire emphasis vocabulary.
- **Do** use an inset ring (`inset 0 0 0 1px`) for hairlines so a border never
  shifts layout.
- **Do** gate any autoplay or transform behind `prefers-reduced-motion`.

### Don't:
- **Don't** use a track colour as text, as a border, or as a ground behind text.
- **Don't** add a second accent. Crimson is the only chromatic action colour.
- **Don't** introduce a monospace face. Tabular Archivo figures are already the
  answer for numbers.
- **Don't** put a small uppercase label or eyebrow above a heading. If the
  content is needed, it goes below the heading as a kicker.
- **Don't** round anything. No pills, no rounded cards, no rounded buttons.
- **Don't** ship gradient text, a coloured `border-left` callout, or any
  glass / backdrop-blur decoration.
- **Don't** apply the `.stock` shadow to a control, a chip, or a fabric band.
- **Don't** apply the fabric weave as a page-wide texture; it belongs only where
  a board actually is.
- **Don't** resize a publication board by hand. Tier follows citations.
- **Don't** stack four or five type sizes inside a single board to create
  hierarchy. Hierarchy across the page is the tier's job.

### Accepted deviations
Recorded so a future editor does not "fix" them blindly:
- **Uppercase navigation and labels.** Uppercase micro-type is normally a smell;
  here it is hall signage grammar and it is deliberate at 11px / `0.14em`.
- **Violet and indigo in the taxonomy.** `#7c3aed` and `#4f46e5` are inherited
  brand commitments that now encode data rather than mood. They stay because
  the swatch-only rule makes their hue irrelevant to legibility.
- **No size ladder inside a board.** A board sets a title, an author line, a
  metadata line, and an abstract — four steps, not more. The missing ladder is
  intentional; the tiers carry hierarchy instead.
- **Token names inherited from the previous world.** `--color-paper`,
  `--color-board`, `--color-hall` and friends kept their names when the values
  changed, so every page kept resolving. Do not rename them for tidiness.

### Known violations of this system, in the build
None outstanding. The documenter's first pass listed four, and all four were
closed in the same session:
- The *Horizons* topic chips in `src/pages/research.astro` set `color` and
  `border-color` inline to the raw track hue, which overrode `.topic-chip`'s ink
  text. Five of the eight hues fail 4.5:1 as text on stock, so this was the
  Swatch-Only Rule broken in its one remaining place. They now pass `--swatch`
  like every other chip.
- `--color-board-deep` and `--color-accent-soft` were declared in `@theme` and
  consumed nowhere. Removed.
- `src/lib/tag-colors.ts` still exported `pillStyle`, `chipStyle`,
  `chipActiveStyle`, `methodChipStyle`, `methodChipActiveStyle`, `methodColor`
  and the `METHOD_COLORS` map from the previous world, with no importers.
  Removed; the classification helpers, which the build does use, are untouched.
- `.masthead` and `.crumbs` rules in `src/pages/research.astro` matched no
  markup. Removed.

### A detector finding that is not a defect
`impeccable detect` reports five `design-system-color` findings of
`rgb(0, 0, 0)` on the header navigation. The analyser cannot resolve
`color-mix(in srgb, var(--color-paper) 72%, transparent)` statically and falls
back to black. The browser's computed value is poster stock at 72% alpha over
fabric, which measures 4.76:1. Do not "fix" the nav to a literal colour to
silence this.
