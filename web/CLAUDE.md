# SoDA Lab site — working notes

Astro 6 + Tailwind v4 site for the Social Data and AI Lab (Haewoon Kwak,
Jisun An) at Indiana University Bloomington. Live at
https://soda-labo.github.io/. Start sessions from this `web/` directory.

Last substantive update: 2026-08-21.

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
├── src/pages/        index · publications · research · team · openings
├── src/components/   Header · Footer · PublicationCard · Email
├── src/layouts/      Base.astro  (max-w-5xl, py-10)
├── src/data/
│   ├── overrides.yml       hand-curated paper metadata (source of truth)
│   ├── scholar_cache.json  weekly Google Scholar snapshot (cron writes)
│   ├── members.yml         faculty · phd · visitors · alumni
│   └── news.yml            newest-first, "Month YYYY" dates, HTML headlines
├── src/lib/          publications.ts · members.ts · news.ts · tag-colors.ts
├── public/           pubpic/ (336×336 WebP) · teampic/ · press/ · sodalab-mark.svg
├── scripts/          Python pipeline (below)
└── .env              SEMANTIC_SCHOLAR_API_KEY — gitignored, do not commit
```

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
- **Thumbnail** — drop any format at `public/pubpic/<slug>.png` and run
  `optimize_pubpics.py`; it converts to WebP and rewrites the `image:` field.
  Roughly 20 % of auto-extracted figures grab a logo or stock photo, so
  replacing them by hand is normal.
- **News** — prepend to `news.yml`. Anchors inside `headline` pick up the
  accent styling automatically (the CSS uses `:global(a)` because the
  headline is injected with `set:html`).
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

201 override entries, 140 visible. All 140 have authors and a link; 137 have
a description; 107 have a thumbnail. 44 news entries. Haewoon ~23.0k
citations (h 48), Jisun ~6.1k (h 43).

## Open items

- Three new papers still need a hand-written description: RespMultimodal
  2026, "When AI Becomes Routine" (AIES), and "Leadership as Coordination
  Control". They have authors and links already.
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
