# SoDA Lab site — working notes

Astro 6 + Tailwind v4 site for the Social Data and AI Lab (Haewoon Kwak,
Jisun An) at Indiana University Bloomington. Live at
https://soda-labo.github.io/. Start sessions from this `web/` directory.

Last substantive update: 2026-08-22.

## Repos on disk

| Path | Branch | What |
|---|---|---|
| `~/Projects/soda-labo-astro/` | `main` | **This repo.** Site source lives in `web/`. Push to `main` → GitHub Actions builds and deploys. |
| `~/Projects/haewoon.github.io/` | `master` | Haewoon's personal landing card (single-file HTML, ~140 KB). Classic GitHub Pages. |
| `~/Projects/soda-labo.github.io/` | `gh-pages` | Dead Jekyll checkout. Only still around for the Python venv at `scripts/prototype-citations/.venv/` used for ad-hoc script runs. |

Backup tags: `jekyll-archive` (old Jekyll site, on the `soda-labo.github.io`
remote) and `pre-minimal-2026` (full personal site before slimming).

## Layout

```
web/
├── src/pages/        index · publications · research · team · openings · news
├── src/components/   Header · Footer · Masthead · PublicationCard · Email
├── src/layouts/      Base.astro  (max-w-5xl, py-10)
├── src/data/
│   ├── overrides.yml       hand-curated paper metadata (source of truth)
│   ├── scholar_cache.json  weekly Google Scholar snapshot (cron writes)
│   ├── members.yml         faculty · phd · visitors · alumni
│   └── news.yml            newest-first, "Month YYYY" dates, HTML headlines
├── src/lib/          publications.ts · members.ts · news.ts · tag-colors.ts
├── public/           pubpic/ (336×336 WebP) · teampic/ · press/ · sodalab-mark.svg
├── scripts/          Python pipeline (below)
├── PRODUCT.md        product truth: audiences, constraints, what is measurable
├── DESIGN.md         the visual system as built, + .impeccable/design.json
└── .env              SEMANTIC_SCHOLAR_API_KEY — gitignored, do not commit
```

**Read `DESIGN.md` before touching anything visual.** It records the poster-hall
system the site was rebuilt into in August 2026: the three materials, the two
type voices, why topic colours may only ever be swatches, and a list of accepted
deviations that look like bugs and are not. `PRODUCT.md` holds the product facts
the design answers to. The direction contract is the HTML comment at the top of
`<body>` in `Base.astro` and it ships in the built pages on purpose.

Deploy: `.github/workflows/deploy.yml` runs `npm ci && npm run build` in
`web/` then `actions/deploy-pages@v4`. Only `main` may deploy (GitHub
environment branch policy). Takes ~1–2 min after push.

## Weekly pipeline

`scripts/update_citations.sh`, run by launchd every Monday 09:00 local.
Log: `~/Library/Logs/sodalab-citations.log`.

1. `fetch_citations.py` — Google Scholar via `scholarly` → `scholar_cache.json`
2. `sync_overrides.py` — dedupe + add new papers to `overrides.yml`
3. **2.5** `fetch_abstracts.py` — caches OpenAlex/S2 IDs + abstracts into `scripts/abstracts.json`
4. `fetch_authors.py --apply` — author lists (normalises "Last, First" → "First Last")
5. `fetch_links.py --apply` — best link: arXiv abs > publisher landing > best-OA > doi.org > S2
6. `fetch_thumbnails.py --apply` — first figure from the PDF via PyMuPDF, else page-1 render
7. `optimize_pubpics.py` — crop + downscale + WebP, rewrites `image:` refs
8. commit + `pull --rebase` + push
9. same for the personal repo via its `update_stats.py`

Steps 4 and 5 read IDs out of `abstracts.json`, so **step 2.5 must stay ahead
of them** — without it new papers can never get authors or links.

## Editing conventions

- **New paper** — nothing to do; the cron picks it up. It lands visible if
  2024+, hidden otherwise. Only the description needs a human.
- **Feature on the home page** — `highlight: true`.
- **Hide** — `hide: true`. This also tombstones the entry so
  `sync_overrides.py` won't recreate it. Use it when merging duplicates.
- **Publication year** — `parseOverrideYear()` takes the **last** 4-digit
  year in `link.venue`, and that beats the Scholar year. So for a paper that
  was on arXiv in 2025 and published in 2026, write
  `venue: ACL Workshop … (C3NLP), 2026`. An explicit `year:` field wins over
  everything if you need it.
- **arXiv venue** — canonical form is `arXiv preprint arXiv:<id>, <year>`.
  `fetch_links.py` sometimes writes OpenAlex's `arXiv (Cornell University)`
  or `ArXiv.org`; normalise by hand.
- **Thumbnail** — roughly 20 % of auto-extracted figures grab a logo or a
  stock photo, so replacing them by hand is normal. Two cases, and they are
  not the same:
  - *Replacing* one: overwrite `public/pubpic/<existing>.webp` in place and run
    `optimize_pubpics.py`. Nothing else. The cache is keyed on mtime, so the
    new file is re-cropped on the next run and `image:` already points at it.
  - *Adding* one where the paper has none: save the image at
    `public/pubpic/<slug>.png`, **then set `image: <slug>.png` on the entry
    yourself**, then run the script. `optimize_pubpics.py` will not create the
    field: `sync_overrides_image_refs()` only rewrites entries whose `image:`
    already names the file it just renamed. The only thing that writes a fresh
    `image:` is `fetch_thumbnails.py`, and it skips any entry that has one.

  Either way the script center-crops to 336×336, converts to WebP, deletes the
  original, and rewrites `image:` to the `.webp` name. To retry the automatic
  extraction for a single paper:
  `fetch_thumbnails.py --apply --slug=<slug>`. Remember the slug is the
  `overrides.yml` key, which for a retitled paper is still the old title's.
- **News** — prepend to `news.yml`. Anchors inside `headline` pick up the
  accent styling automatically (the CSS uses `:global(a)` because the
  headline is injected with `set:html`). Paper titles are wrapped in escaped
  double quotes that sit *outside* the anchor, so the link text is exactly the
  title; venue and conference links are not titles and stay unquoted. The home
  page shows the last twelve months or six entries, whichever is more
  (`recentNews()`), and `/news` carries everything grouped by year, so nothing
  needs pruning as the file grows.
- **Descriptions** — 200–350 chars, lab voice: open with a question or hook,
  then what we did and what we found. No em dashes anywhere on the site.
  To draft one, paste the raw abstract into `description:` and ask for a
  rewrite; `apply_descriptions.py` takes a `{slug: text}` JSON for bulk work.

## Taxonomy — `src/lib/tag-colors.ts`

Eight topics, multi-label. `sync_overrides.py` mirrors the same keyword rules
for auto-classifying new papers, so **edit both** when rules change.

`online-harm` #dc2626 · `news-journalism` #57534e · `user-behavior` #d97706 ·
`beliefs-opinions` #7c3aed · `llms-responsible-ai` #4f46e5 ·
`bias-fairness` #0d9488 · `networks-influence` #0284c7 ·
`digital-health` #db2777

Secondary axes: `methods` (llm, nlp, networks, crowdsourced, user-study,
dataset) and `platforms` (twitter, reddit, youtube, facebook, instagram,
tiktok, gab, news-media, multi-platform).

Card chips are `<a href="/publications?topic=X">`. From any other page they
navigate and the publications page applies the filter from the URL params; on
the publications page itself the JS calls `preventDefault()` and toggles in
place. Filter state syncs back to the URL so any view is shareable.

## Traps that have actually bitten

- **Duplicate papers from retitling.** When a paper is renamed, Scholar may
  issue *new* IDs, so neither the scholar_id match nor the 0.92 fuzzy title
  match catches it and it renders twice. Fix: absorb the new `scholar_ids`
  into the curated entry, adopt the new title, `hide: true` the duplicate.
  Has happened three times (DeepSeek, belief-inference, C3NLP depression).
- **Personal repo diverges on its own.** A GitHub Action in Haewoon's CV repo
  pushes `PDFs/haewoon_CV.pdf` into it, so always rebase before pushing there.
- **Python version.** Scripts use `X | None` (3.10+). The cron bootstraps the
  venv from Homebrew python3.14/3.13; macOS `/usr/bin/python3` is 3.9 and
  fails. If Homebrew moves to 3.15+, add it to the `for candidate` list in
  `update_citations.sh`.
- **Astro scoped styles don't reach `set:html` content.** Wrap the inner
  selector in `:global(...)` or the rule silently never matches.
- **Tailwind hot-reload misses brand-new files.** Restart the dev server if
  classes appear to do nothing.

## Current state

201 override entries, 139 visible. All 139 have authors, a link, and a
description; 109 have a thumbnail. 47 news entries. Haewoon ~23.1k
citations (h 48), Jisun ~6.1k (h 43). These figures drift with every cron
run; treat them as a rough snapshot, not something to keep exact.

## Open items

- **Links waiting on publishers.** "Same Symptoms, Different Severity?"
  (EMNLP 2026 Findings) has no URL until EMNLP releases its proceedings, so
  its title in the August 2026 news entry is plain text and it is not in
  `overrides.yml`; Scholar has not picked it up either. "Leadership as
  Coordination Control" (TMLR) still links to arXiv 2606.19111 in both the
  news entry and the card until the camera-ready lands on OpenReview.
- Press carousel on the home page still has only the three Nature covers —
  adding more needs outlet, year, blurb, URL, and an image from Haewoon.
- `/publications` renders all ~140 papers in one page. Year-collapse or
  load-more was discussed and deferred; revisit if the page feels heavy.

## Commands

```bash
npm run dev                      # local preview
npm run build                    # static build → dist/
./scripts/update_citations.sh    # run the weekly pipeline by hand
tail -f ~/Library/Logs/sodalab-citations.log

# ad-hoc script runs use the old prototype venv (has pyyaml/Pillow/pymupdf)
PY=~/Projects/soda-labo.github.io/scripts/prototype-citations/.venv/bin/python
$PY scripts/fetch_links.py            # dry-run; add --apply to write
$PY scripts/optimize_pubpics.py

# launchd
launchctl list | grep sodalab
launchctl start com.sodalab.citations
```
