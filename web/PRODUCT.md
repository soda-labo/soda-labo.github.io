# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two primary audiences, weighted equally. When they conflict, neither is
sacrificed for the other.

**Prospective members.** PhD applicants (admitted through the Luddy School
Informatics program), postdocs, visiting scholars and students, and IU
undergraduate / master's students. They usually arrive from a paper, a talk,
or a search. They need three things in order: what the lab actually studies,
whether their own interest fits it, and whether anything is open right now.
`/openings` is the conversion point, and the "Current availability" box is the
fact they came for. They have often already read one of the lab's papers.

**Peer researchers.** Computational social science, NLP, and network science
researchers who arrive looking for one specific paper or scanning what the lab
has published lately. They need to reach the paper's real link fast, and to
narrow ~140 entries by topic without reading all of them.

Press, program managers, and department reviewers visit too, but were not
confirmed as a group the design owes a dedicated path.

## Product Purpose

The public front door for the Social Data and AI Lab (SoDA Lab) at Indiana
University Bloomington, led by Haewoon Kwak and Jisun An. It exists to make the
lab's work findable and its research direction legible to people deciding
whether to read it, cite it, or join it.

The visit succeeded when one of these happened:

1. A well-matched person emailed with a specific direction in mind, not a
   generic inquiry.
2. A researcher reached the paper they were looking for.
3. The visitor left with the lab's position in mind: social phenomena studied
   through large-scale data and AI.

## Positioning

The lab treats the computational and the social as one system. Online platforms
are shaped by algorithms (what is recommended, who is followed) and by people
(what gets shared, discussed, ignored) at the same time, and the lab builds
tools that measure both sides together rather than reducing the result to
engagement counts. Its scope covers measurement, understanding, design, and
assessment of implications, which is wider than a methods lab and more
computational than a survey-based one.

Two PIs with distinct but overlapping records, and a body of work that spans
eight topics at once rather than one specialty, are facts a neighboring lab
cannot simply claim.

## Operating Context

**The publication list maintains itself; the design must survive that.** A
launchd cron runs every Monday at 09:00 local: it pulls Google Scholar, adds new
papers to `src/data/overrides.yml`, backfills authors, links, and thumbnails,
optimizes images, commits, and pushes. GitHub Actions then builds and deploys on
any push to `main`.

Consequences that constrain design decisions:

- New papers appear without a human ever opening the page. Anything that must be
  hand-written per paper (description, corrected thumbnail) will be missing or
  wrong for some entries at all times. Roughly 20 percent of auto-extracted
  thumbnails grab a logo or stock photo.
- The publication list only grows. A layout that reads well at 140 entries has
  to still read well at 250.
- `overrides.yml` is rewritten by Python scripts, so any per-paper field a design
  depends on must survive a `yaml.dump` round trip.

Editorial content (news, team, openings availability, research narrative) is
hand-edited and changes rarely.

## Capabilities and Constraints

- Static Astro 6 + Tailwind v4 build on GitHub Pages. No backend, no database,
  no forms, no server-side filtering.
- Publication filtering is client-side JS over the full rendered list. Filter
  state syncs to the URL, so any filtered view is shareable, and topic chips on
  a card link to `/publications?topic=X`.
- Five pages: index, publications, research, team, openings.
- Content lives in YAML (`overrides.yml`, `members.yml`, `news.yml`) plus one
  Scholar cache. Adding data is editing a file, not a CMS.
- **Analytics measure traffic, not people.** Google Analytics 4 runs in
  production only, with Consent Mode denied by default, so it writes no cookies
  and no browser storage and there is no consent banner. The trade is that
  without a client id a returning visitor is counted fresh each time, so "users"
  reads closer to "visits" and anything longitudinal is modelled. Pageviews,
  referrers, and which pages get read are reliable.
- **Two of the three success criteria are still not measurable.** Analytics can
  show that `/openings` was read, never that a good-fit person emailed, and
  never that the lab's position was remembered. Design decisions about those two
  cannot be settled with site data.
- Email addresses render as `user [at] host` and are rewritten to a real
  `mailto:` by inline JS for spam resistance. The primary conversion action is
  therefore JS-gated and produces no on-site signal at all.
- Open decision: `/publications` renders all ~140 papers in one page.
  Year-collapse or load-more was discussed and deferred.

## Brand Commitments

- Name: SoDA Lab, the Social Data and AI Lab at Indiana University Bloomington.
  Mark at `public/sodalab-mark.svg`.
- **No em dashes anywhere in site copy.** Confirmed as a site-wide rule, not
  just a rule for publication descriptions. Site copy is currently clean; the
  only remaining em dashes in the tree are inside JSX comments, which never
  render.
- Publication descriptions follow a fixed voice: 200 to 350 characters, opening
  with a question or hook, then what the work did and what it found.
- The eight-topic taxonomy is product terminology, not decoration: online-harm,
  news-journalism, user-behavior, beliefs-opinions, llms-responsible-ai,
  bias-fairness, networks-influence, digital-health. The research page and the
  publication chips read the same source and must stay in sync.
- The openings page states explicitly that applicants from all backgrounds are
  welcome, including those underrepresented in computing and social science.

## Evidence on Hand

- 139 visible publications, all with authors, a working link, and a description.
  107 have a thumbnail. 62 further entries are hidden or tombstoned, which
  includes workshop summaries and organiser notes that Scholar files as papers.
- 44 news entries, newest first.
- Press: exactly three items, all covers or features (Nature Human Behaviour
  2025, Nature News 2020 on Jisun, Nature News 2016 on Haewoon). There is no
  fourth. Do not design a carousel that implies more.
- Citation counts, refreshed weekly from Scholar: Haewoon approximately 23.0k
  (h-index 48), Jisun approximately 6.1k (h-index 43).
- Team: 2 faculty, 7 PhD students, 1 current visitor, plus alumni (2 postdocs,
  4 past visitors, and SMU-era graduate and undergraduate students).
- Custom hand-drawn SVG illustrations exist for the research areas. They are
  original to this site, not stock.
- Current fact with an expiry: the lab is on parental leave through Fall 2026.
  Earliest hosting of new visitors is Spring 2027, and postdoc positions are not
  available. This is stated in one place on the openings page.
- No testimonials, no student quotes, no funding logos, no lab photos beyond
  individual headshots. Do not invent any of these.

## Product Principles

1. **Two front doors, one lab.** A prospective student and a peer researcher
   must both find their path within one screen of arriving. Neither gets a
   watered-down version.
2. **Availability is a fact, not a mood.** What is open, what is not, and when
   that changes is stated plainly. Vague encouragement wastes an applicant's
   time and the lab's.
3. **Design for the unattended entry.** Every publication surface has to look
   deliberate when the newest item was added by a cron job with a mediocre
   thumbnail and no human review.
4. **The work is the evidence.** The lab's standing is shown through papers,
   press, and named people, never through claims about itself.
5. **Scale is the default, not the exception.** Lists grow every week. Layouts
   are judged at their future size.

## Accessibility & Inclusion

No specific standard has been established for this site. Undecided, and worth
settling before the next substantial visual change.
