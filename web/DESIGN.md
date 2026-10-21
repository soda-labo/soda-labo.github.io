---
name: SoDA Lab
description: A conference poster hall — pale mint board felt carrying white poster stock on a light hall floor.
colors:
  hall: "#eef5f1"
  paper: "#fbfdfc"
  paper-2: "#e6eeea"
  board: "#d9ebe1"
  on-board: "#14181b"
  on-board-soft: "#4a545c"
  on-board-faint: "#535e66"
  ink: "#14181b"
  ink-soft: "#4a545c"
  ink-faint: "#5e6870"
  rule: "#d6e0db"
  accent: "#1d4a73"
  accent-deep: "#153857"
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
  board: "24px"
  masthead-y: "40px"
components:
  board:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "24px 24px 22px"
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
    textColor: "{colors.on-board-soft}"
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
materials carry everything: the **hall floor** (`#eef5f1`, mint mist) you stand on, the
**board fabric** (`#d9ebe1`, pale mint felt) you face, and the **poster stock**
(`#fbfdfc`)
pinned to it. Nothing else is a surface. The page ground is always the floor;
a `.board` is only applied where a board actually stands (the header strip,
a page masthead, the home hero, the footer); `.stock` is only applied to a
sheet that is pinned to something. The fabric is felt: an SVG fractal-noise
texture in dark flecks only, readable as material up close and flat from a
distance. It is a material, never a page-wide grain. Until October 2026 it was
a 3px weave of two `repeating-linear-gradient` layers, which is the stripe
pattern generated UIs reach for; noise is what board cloth looks like, and
dark-only flecks can only deepen the ground. On the light felt they are kept to
6% alpha; the 14% the old dark fabric used made pale felt look grubby.

**The palette was lightened in October 2026.** It had been a dark slate fabric
(`#46525c`) with paper-coloured text on a grey hall floor (`#eaeae7`), and read
as heavy. The lab asked for something fresher; of six pale felts compared side
by side (sky, mint, aqua, butter, sand, cool grey), mint was chosen. Text on
fabric flipped from paper to ink with it.

Every publication board is the same size. The rebuild originally sized boards
by citation count (landmark / major / standard), on the claim that a landmark
paper and a workshop preprint should not look like the same object; the lab
removed that in October 2026, so a board's prominence no longer encodes its
citations. What distinguishes papers now is track (the swatch), order (newest
first by default, or by citations through the sort control), and the home
page's featured boards.

Colour is rationed hard. Harbor navy (`#1d4a73`) is the only action colour and
the only colour the navigation strip is allowed; the eight research-topic hues
were demoted from decoration to **data** and appear exclusively as small
printed squares. Every corner is square. There is no monospace anywhere.

**Key Characteristics:**
- Three materials only: hall floor, board fabric, poster stock.
- Every publication board is one size; citations are a sort, not a scale.
- One accent (harbor navy) for actions, board tags, and "you are here".
- Topic hues are swatches, never text.
- Zero border-radius; hairlines are inset rings, not borders.
- Archivo for signage and headings, Literata for reading. No monospace.
- Tabular figures globally — every number on the site is a measurement.

## Colors

A light palette: a mint-mist room, pale mint felt, near-black ink, and a
single harbor navy. The eight topic hues sit outside this
palette on purpose — they encode data, not mood.

### Primary
- **Harbor Navy** (`#1d4a73`): the one action colour. Primary buttons, the
  navy board-number tag, the active nav destination, links inside prose and
  news items, the `Open` stamp, `::selection`, the caret, and the focus ring.
  It measures 9.02:1 on stock, 8.32:1 on the hall floor, and 6.95:1 on the
  felt. Hover deepens to `#153857` (11.85:1), as `--color-accent-deep`.
  Until October 2026 the accent was IU crimson (`#990000`). Once the felt went
  mint, red sat as mint's complement and every tag vibrated against the board;
  a cool navy stays in the felt's family and keeps the action colour quiet.

### Neutral
- **Hall Floor** (`#eef5f1`): the page ground. `body` background, nothing else.
  A whisper of the felt's hue, so the floor under the header strip reads as the
  same room rather than a warm off-white beside a cool board. It was `#f5f5f0`
  until October 2026.
- **Poster Stock** (`#fbfdfc`, cool white): every sheet — publication boards, team cards,
  the news sidebar, filter controls, and the badge behind the lab mark. Also
  the type colour on navy and on ink (buttons, stamps, the press strip).
  Sheets sit close to the floor in value (1.08:1); the pinned-sheet shadow is
  what separates them.
- **Stock in Shadow** (`#e6eeea`): the empty bed behind an image that has not
  loaded or does not fill its frame (publication figures, press clippings).
- **Board Fabric** (`#d9ebe1`, measured `#d2e4da` with the felt): the header
  strip, the page masthead, the home hero band, and the footer, so every page
  opens and closes on it. Always full-bleed, never a container inside the
  reading column.
- **On-board inks** (`--color-on-board` `#14181b` 13.5:1, `-soft` `#4a545c`
  5.8:1, `-faint` `#535e66` 5.0:1, all measured on the felt): the only text
  colours header, masthead and footer use. Ink Faint itself is 4.30:1 on the
  felt, under the floor, which is why the fabric has its own faint step.
  Change the fabric, and these are the tokens to re-verify.
- **Ink** (`#14181b`): headings, board titles, lab-author names, and the ground
  of an inverted control (active filter chip, notice head, the
  press caption strip). 17.48:1 on stock, 16.12:1 on the floor.
- **Ink Soft** (`#4a545c`): body copy, abstracts, author lists. 7.58:1 on stock, 6.99:1 on the floor.
- **Ink Faint** (`#5e6870`): metadata, counts, section labels, dates,
  placeholders. 5.57:1 on stock and 5.14:1 on the hall floor. Not for use on
  the felt (4.30:1); see On-board inks.
- **Rule** (`#d6e0db`): hairlines, control borders, section dividers, and the
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
WCAG AA as text on the hall floor (`#d97706` 2.88:1, `#0d9488` 3.38:1, `#0284c7` 3.70:1,
`#db2777` 4.15:1, `#dc2626` 4.36:1), so the rule is not a preference — it is the
only way the taxonomy stays legible.

**The One Accent Rule.** Navy is the site's only chromatic accent. If a new
element needs to look important and is not an action, a board address, or the
current destination, it gets weight or inversion, not colour.

**The 4.5 Floor.** Every text-on-ground pair ships at 4.5:1 or better and the
measured number is recorded here. On the felt, that is the three on-board
inks above. Twice now a colour has looked fine and measured under the floor
(a grey ink-faint on the old hall, and ink-faint on the new felt), so measure
the rendered ground, felt included, rather than trusting the token.

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
  home hero statement only. `text-wrap: balance`. No other page has a display
  hero; research opens on a masthead like the rest.
- **Masthead headline** (600, `clamp(30px, 4.2vw, 46px)`, 1.1, `-0.03em`): the
  page name on fabric, in ink.
- **Board title** (600, `-0.02em`, 1.32): 19px on desktop, 17px below 640px.
  `text-wrap: balance`.
- **Section heading** (600, 18–24px, `tracking-tight`): in-page section names
  on team, openings, and the home featured strip.
- **Reading body** (`.read`, Literata 400, 16px, 1.6, `max-width: 68ch`): lab
  statement, abstracts, research copy.
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

**The Measure Rule.** Literata reading text is capped at `64ch` by `.read`
(about 78 characters; `68ch` ran to 83, past the ~80 ceiling); Archivo body
text on /openings at `60ch` (about 78; Archivo's wide `0` makes `68ch` run to 88); news archive entries at `64ch`; the
masthead lede at `52ch`. A paragraph with no measure cap is a bug. Running text
(`p`, `li`, `dd`) sets `text-wrap: pretty` so a paragraph never ends on one
word, and every `h1`–`h3` sets `text-wrap: balance`.

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

Spacing follows Tailwind's 4px scale. Boards take 24px of padding (about 18px
below 640px) and stack with 20px between them.

Breakpoints in use: 640px (`sm`, and the publication-board media query), 720px
(the research page's own collapse to one column), 768px (`md`, where the nav
switches from a horizontal strip to a disclosure panel), 1024px (`lg`, where the
home page splits into content plus a 17rem press rail or a 19rem news rail).

Responsive behaviour worth knowing: below 640px every board hides its figure.
A 72px crop was unreadable and stole the title's measure, so on a phone a board
is its title, its finding, and its track.

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
the 2px navy outline does not clip a corner. Forms follow the same grammar:
the search field, sort select, filter buttons, and the "more filters" summary
are all 1px `--color-rule` rectangles on stock that darken their border to ink
on hover and invert to ink-on-paper when active.

The recurring silhouettes are printed objects: a navy number tag offset
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
- **Primary** (`.act-primary`, `.apply-action`): navy ground, paper text,
  `0.7rem 1.15rem` padding. Hover deepens to `#153857` over 0.15s.
- **Secondary** (`.act-secondary`): transparent with a 1.5px inset ink ring and
  ink text; hover inverts to ink ground / paper text.
- **Focus:** the global 2px navy `:focus-visible` outline at 2px offset.
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
- **Internal padding:** 24px for publication boards; 20px for team cards and
  the news rail; 20–36px for the home statement sheet.

### Inputs / Fields
`.filter-field` — stock ground, 1px `--color-rule` border, 0.875rem ink text,
`0.5rem 0.7rem` padding, square. Placeholder in ink-faint. Hover darkens the
border to ink-faint. Focus uses the global navy ring. The disclosure for
secondary filters is a `<details>` whose summary is styled as a label-cased
control with a CSS triangle chevron that rotates 180° when open; the native
marker is suppressed.

### Navigation
The header is a full-width fabric strip. The lab mark sits on a `2.75rem`
stock square — a badge printed on paper and pinned up. Destinations are 11px
uppercase `0.14em` labels in on-board-soft; hover raises them to full ink over
a 7% ink wash; the current destination gets a solid navy block with paper
text, which is the hall's "you are here" and the only colour the strip carries.
Below 768px the strip collapses to a hamburger toggle and a stacked panel
separated by a 14%-ink hairline.

### Publication board (signature component)
The system's defining object. One size for every paper: a 5.5rem figure,
a 19px title, the author string, a metadata line, the abstract, and the track
tags. Lab members' names inside the author string are bolded to ink; the venue
is italic; the metadata line is a single ink-faint run of venue · year ·
citations in tabular figures.

**The One Size Rule.** Every board is the same size. Until October 2026 boards
were sized by citation count (>= 500 landmark, >= 100 major); the lab removed
it. Do not bring it back, and do not resize a board by hand to promote it:
feature a paper with `highlight`, and let readers who want impact use the
"Most cited" sort.

**The Unprinted Plate Rule.** Roughly a fifth of boards have no usable figure
at any given time: the cron lifts the first plate out of the PDF and sometimes
there is nothing worth lifting, and the count moves every week. Those boards render `.pub-figure.is-blank` at the figure's size —
stock in shadow, the same hairline ring, and the board's track swatch centred —
never a missing element. A board with no plate at all shunts its title left and
breaks the column every other board shares. The plate stays plain: an earlier
version hatched it with a repeating gradient, which the detector correctly
called a generated-UI signature. On mobile the plate follows the figure rule and
disappears with it.

### Hall directory (home)
A ruled list of the eight tracks with the number of boards standing under each,
in the home page's reading sheet. Same grammar as the board's track tag: a
0.65rem swatch, the name in ink, the count in ink-faint tabular figures, the
whole row a link into `/publications?topic=`. Counts come from the corpus, so
they follow the cron rather than being typed.

It exists for balance as much as for navigation. The reading sheet is
`self-start` (see the Pinned-Sheet Rule) and ran 668px shorter than the news
column beside it. The directory closes that to about 250px with content that
does a job, which is the only acceptable way to lengthen a column: the earlier
attempt let the grid stretch the sheet instead and shipped 704px of blank paper.
Never pad this column with a decorative block to even the columns up.

Each row carries its own `border-top`, and the last row adds a `border-bottom`.
The rule does not live on the `<ul>`: a bordered wrapper leaves its first child
flush against the line.

### News sheet and the news archive (`/news`)
The home column carries the last twelve months, or six entries if twelve months
holds fewer (`recentNews()` in `src/lib/news.ts`). The floor is not cosmetic:
2025 carries a single entry, and a strict window would empty this column beside
the reading sheet it balances. At the current corpus the window yields six and
the two columns land within 17px of each other.

`/news` is the same material at full length: a fabric masthead, then one stock
sheet per year with a `8.5rem` date column beside the entry, collapsing to a
single column below 768px. Entries are separated by a hairline that belongs to
the row, never to the sheet. Headlines arrive through `set:html`, so their
anchor styling has to be wrapped in `:global(...)` or it silently never matches.

The archive is evidence, not filler: it is the record that the lab has published
without a gap since 2020, which is exactly what the prospective-member audience
is reading for. Do not prune it to shorten the file.

**The Unnumbered Host Rule.** The navy `01`-style tag addresses *the work*.
The lab's own board on the home page deliberately carries no number; featured
boards are addressed from `01` upward.

### Masthead (signature component)
A full-bleed fabric band at the head of every page but home: the
page name in ink at `clamp(30px, 4.2vw, 46px)`, an optional lede at `52ch` in
on-board-soft. A page announces itself the way the hall entrance does, never
with a bare heading on the floor.

### Research section head and kicker
Section heads are a single horizontal row (`auto 1fr`): the heading, then a
1px rule running to the column's edge, aligned with every other divider on the
page. Laid out across, never stacked.

**The Unnumbered Area Rule.** Each research area carries a track label below
its `h3`: a 9px swatch in the area's primary track colour (`--track`) and the
area name in label type. No number. The areas were numbered 01–09 until
October 2026, when a design audit pointed out the obvious: nine research areas
are not a sequence, so an ordinal claims an order that does not exist and reads
as decoration. Numbers stay only where something is genuinely addressed, the
featured boards on the home page. A small label above a heading is still banned
outright.

### Footer
The page closes the way it opens, on board fabric. A colophon rather than a
sitemap, since the header already lists every destination: the lab name, one
sentence of affiliation with the Luddy link inline, both faculty emails, and
the one action the site exists for, "Join the lab", as the same navy block
as the home page's primary action. Links in the colophon are underlined at rest
because they sit inside a sentence. On-board-soft carries the body (5.8:1),
on-board-faint the copyright line (5.0:1). Until October 2026 the footer was a
three-column paper band with a "Links" column holding two links: the one surface
the poster-hall rebuild never reached.

### Notice and stamps (openings)
A pinned official notice: stock ground with a hairline ring, a solid ink head
bar in label type, and one stamp per row: `Closed` as a 1.5px ink-faint
outline on stock, `Open` solid navy. Filled against outlined is what tells
them apart; with a navy accent, a solid ink `Closed` beside a solid navy
`Open` read as the same stamp. Status is stamped, never implied by absence
and never by a coloured left bar.

### Press clipping (home)
A clipping in an inset-ringed frame with an ink caption strip printed beneath
it: venue in 700, blurb in 66% paper, a tabular `n / N` position, and two
square 1.9rem step buttons that turn navy on hover. It auto-advances every
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
- **Don't** add a second accent. Navy is the only chromatic action colour.
- **Don't** introduce a monospace face. Tabular Archivo figures are already the
  answer for numbers.
- **Don't** put a small uppercase label or eyebrow above a heading. If the
  content is needed, it goes below the heading as a kicker.
- **Don't** round anything. No pills, no rounded cards, no rounded buttons.
- **Don't** ship gradient text, a coloured `border-left` callout, or any
  glass / backdrop-blur decoration.
- **Don't** apply the `.stock` shadow to a control, a chip, or a fabric band.
- **Don't** apply the fabric texture as a page-wide grain; it belongs only
  where a board actually is. And don't bring back repeating-gradient stripes
  for it: that is the pattern the felt replaced.
- **Don't** resize a publication board, by hand or by citations. Every board
  is one size.
- **Don't** stack four or five type sizes inside a single board to create
  hierarchy.

### Accepted deviations
Recorded so a future editor does not "fix" them blindly:
- **Uppercase navigation and labels.** Uppercase micro-type is normally a smell;
  here it is hall signage grammar and it is deliberate at 11px / `0.14em`.
- **Violet and indigo in the taxonomy.** `#7c3aed` and `#4f46e5` are inherited
  brand commitments that now encode data rather than mood. They stay because
  the swatch-only rule makes their hue irrelevant to legibility.
- **No size ladder inside a board.** A board sets a title, an author line, a
  metadata line, and an abstract — four steps, not more. The missing ladder is
  intentional; a list this long reads by scanning titles, not by type scale.
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
