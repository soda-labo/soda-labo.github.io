# SoDA Lab Website (Astro)

Website for the Social Data and AI Lab at Indiana University Bloomington.

Built with [Astro](https://astro.build/) + [Tailwind CSS](https://tailwindcss.com/).
Google Scholar citation counts are refreshed weekly by a local launchd job.

## Development

```sh
cd web
npm install
npm run dev      # http://localhost:4321
npm run build    # static output → web/dist
```

## Project layout

```
web/
├── src/
│   ├── pages/           # File-based routing (index, publications, team, …)
│   ├── components/      # Header, Footer, PublicationCard, Email
│   ├── layouts/         # Base layout wrapper
│   ├── lib/             # Data loaders + taxonomy (topics, methods, platforms)
│   ├── data/            # YAML/JSON: overrides, members, scholar cache
│   └── styles/          # global.css + Tailwind import
├── public/              # Static assets (images, PDFs, favicon)
└── scripts/             # Weekly Google Scholar refresh (Python + launchd)
```

## Editing content

- **Publications curation**: `web/src/data/overrides.yml`
- **Members**: `web/src/data/members.yml`
- **Home page text + press carousel**: `web/src/pages/index.astro`

The dev server hot-reloads on save.

## Scholar refresh

`web/scripts/install_launchd.sh` installs a weekly job that refreshes
`web/src/data/scholar_cache.json` from Google Scholar and pushes the change.

## History

The previous Jekyll site lives on the `gh-pages` branch (forked originally
from the [Allan Lab template](https://github.com/mpa139/allanlab), MIT).
