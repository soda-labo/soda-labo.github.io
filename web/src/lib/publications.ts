/**
 * Publications data pipeline.
 *
 * Inputs:
 *  - src/data/overrides.yml    : human-curated metadata (tags, image, links, etc.)
 *  - src/data/scholar_cache.json : citation counts + all GS-known publications
 *
 * Output: a unified list of Publication objects, deduped, sorted by year + cites.
 *
 * Policy:
 *  - Every override entry shows up.
 *  - Uncurated GS entries from RECENT_YEAR_CUTOFF onward also show up.
 *  - Older uncurated GS entries are hidden.
 */
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import { classifyTitle, classifyMethods, classifyPlatforms, TOPICS } from "./tag-colors";

// Data files live in src/data/. Use cwd (= Astro project root at build time)
// so this works whether the module is loaded from source or a bundled chunk.
const DATA_DIR = path.resolve(process.cwd(), "src/data");

const RECENT_YEAR_CUTOFF = 2024;

export type Link = { url: string; venue?: string };

export type Publication = {
  /** stable id used for keys (slug from title) */
  id: string;
  title: string;
  /** display authors string. Comes from overrides if available, else derived. */
  authors: string;
  /** clean venue display ("WWW 2010"), with year if available */
  venue: string;
  year: number | null;
  /** max citation count across matched GS entries */
  citations: number;
  /** Primary topics (usually 1, can be multi). */
  tags: string[];
  /** Methodologies used (LLM, NLP, networks, etc.). Auto-extracted or curated. */
  methods: string[];
  /** Platforms studied (Twitter, Reddit, etc.). Auto-extracted or curated. */
  platforms: string[];
  image?: string;
  description?: string;
  link?: Link;
  news?: string[];
  highlight: boolean;
  /** when true, this entry has no override curation */
  uncurated: boolean;
  /** scholar IDs from both author profiles, if matched */
  scholarIds: string[];
};

type OverrideEntry = {
  title: string;
  tags?: string[];
  methods?: string[];
  platforms?: string[];
  hide?: boolean;
  image?: string;
  highlight?: boolean;
  description?: string;
  link?: { url: string; venue?: string };
  news?: string[];
  authors?: string;
  scholar_ids?: string[];
  /** Explicit publication year. Wins over venue-extracted and GS year.
   *  Useful when GS only knows the arXiv preprint year (e.g. 2025) but the
   *  paper was officially published the following year (e.g. C3NLP 2026). */
  year?: number;
};

type ScholarPub = {
  title: string;
  year: string | null;
  venue: string | null;
  citations: number;
  scholar_id: string;
};

type ScholarCache = Record<
  string,
  {
    publications?: ScholarPub[];
    error?: string;
  }
>;

function readOverrides(): Record<string, OverrideEntry> {
  const raw = fs.readFileSync(path.join(DATA_DIR, "overrides.yml"), "utf8");
  return (yaml.load(raw) ?? {}) as Record<string, OverrideEntry>;
}

function readScholarCache(): ScholarCache {
  const raw = fs.readFileSync(path.join(DATA_DIR, "scholar_cache.json"), "utf8");
  return JSON.parse(raw) as ScholarCache;
}

function normalizeTitle(t: string): string {
  return t
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function slugify(t: string): string {
  return normalizeTitle(t).replace(/\s+/g, "-").slice(0, 80);
}

/** Heuristic: turn GS's noisy citation string into a short venue label. */
function prettifyVenue(raw: string | null | undefined): string {
  if (!raw) return "";
  let v = raw.trim();
  // Strip trailing page numbers + year: ", 591-600, 2010"
  v = v.replace(/,\s*\d+[-–]\d+(,\s*\d{4})?$/, "");
  v = v.replace(/,\s*\d{4}$/, "");
  // Common abbrev rules — kept tight on purpose to avoid wrong rewrites
  const rules: [RegExp, string][] = [
    [/Proceedings of the .* World Wide Web.*/i, "WWW"],
    [/Proceedings of the .* SIGCHI.*Human Factors.*/i, "CHI"],
    [/Proceedings of the .* ACM SIGKDD.*/i, "KDD"],
    [/Proceedings of the .* AAAI Conference on Web and Social Media.*/i, "ICWSM"],
    [/Proceedings of the .* AAAI Conference.*/i, "AAAI"],
    [/Proceedings of the .* CSCW.*/i, "CSCW"],
    [/Proceedings of the .* EMNLP.*/i, "EMNLP"],
    [/Proceedings of the .* ACL.*Association for Computational Linguistics.*/i, "ACL"],
    [/Proceedings of the .* NAACL.*/i, "NAACL"],
  ];
  for (const [re, name] of rules) {
    if (re.test(v)) return name;
  }
  // Trim "Proceedings of the X" boilerplate
  v = v.replace(/^Proceedings of the \d+(st|nd|rd|th)?\s*/i, "");
  v = v.replace(/^Proceedings of /i, "");
  return v;
}

function parseYear(y: string | null | undefined, fallbackVenue?: string): number | null {
  if (y) {
    const n = parseInt(y, 10);
    if (!Number.isNaN(n)) return n;
  }
  // Try to pull a year out of venue string
  if (fallbackVenue) {
    const m = fallbackVenue.match(/\b(19|20)\d{2}\b/);
    if (m) return parseInt(m[0], 10);
  }
  return null;
}

function parseOverrideYear(o: OverrideEntry): number | null {
  const m = o.link?.venue?.match(/\b(19|20)\d{2}\b/);
  return m ? parseInt(m[0], 10) : null;
}

/** Dedupe GS publications across authors by fuzzy(ish) title equivalence. */
function dedupeScholar(cache: ScholarCache): Map<string, {
  title: string;
  year: number | null;
  venue: string | null;
  citations: number;
  scholarIds: string[];
}> {
  const map = new Map<string, {
    title: string;
    year: number | null;
    venue: string | null;
    citations: number;
    scholarIds: string[];
  }>();
  for (const info of Object.values(cache)) {
    if (!info.publications) continue;
    for (const p of info.publications) {
      const key = normalizeTitle(p.title || "");
      if (!key) continue;
      const existing = map.get(key);
      const year = parseYear(p.year, p.venue ?? undefined);
      if (existing) {
        existing.citations = Math.max(existing.citations, p.citations || 0);
        existing.scholarIds.push(p.scholar_id);
      } else {
        map.set(key, {
          title: p.title,
          year,
          venue: p.venue,
          citations: p.citations || 0,
          scholarIds: [p.scholar_id],
        });
      }
    }
  }
  return map;
}

export function loadPublications(): Publication[] {
  const overrides = readOverrides();
  const gsMap = dedupeScholar(readScholarCache());

  // Title-normalised index of every GS entry (e.g. "u s" vs "us" still keep
  // separate keys here — that's why we also build a scholar_id index below).
  const overrideNormToGsKey = new Map<string, string>();
  for (const gsKey of gsMap.keys()) overrideNormToGsKey.set(gsKey, gsKey);

  // scholar_id -> gsKey reverse index. Lets an override claim any GS entries
  // it lists in `scholar_ids`, even when the GS title drifted (typos, "U.S."
  // vs "US", renamed preprint, etc.) so the uncurated path doesn't surface
  // the same paper a second time.
  const sidToGsKey = new Map<string, string>();
  for (const [gsKey, gs] of gsMap.entries()) {
    for (const sid of gs.scholarIds) sidToGsKey.set(sid, gsKey);
  }

  const out: Publication[] = [];
  const consumedGsKeys = new Set<string>();

  for (const [id, o] of Object.entries(overrides)) {
    // Always consume the matched GS entry so hidden papers don't reappear
    // through the uncurated path. Match by normalised title first, then by
    // any scholar_ids the override carries.
    const norm = normalizeTitle(o.title);
    const gsKey = overrideNormToGsKey.get(norm);
    const gs = gsKey ? gsMap.get(gsKey) : undefined;
    if (gsKey) consumedGsKeys.add(gsKey);
    for (const sid of o.scholar_ids ?? []) {
      const k = sidToGsKey.get(sid);
      if (k) consumedGsKeys.add(k);
    }

    if (o.hide) continue;

    // Year priority: explicit override > venue-extracted (curated) > GS (often
    // just the arXiv preprint year, which is wrong once the paper is formally
    // published the following year).
    const year = o.year ?? parseOverrideYear(o) ?? gs?.year ?? null;
    out.push({
      id,
      title: o.title,
      authors: o.authors ?? "",
      venue: o.link?.venue ?? prettifyVenue(gs?.venue) ?? "",
      year,
      citations: gs?.citations ?? 0,
      tags: (o.tags ?? []).filter((t) => (TOPICS as readonly string[]).includes(t)),
      methods: o.methods ?? [],
      platforms: o.platforms ?? [],
      image: o.image,
      description: o.description,
      link: o.link?.url ? { url: o.link.url, venue: o.link.venue } : undefined,
      news: o.news,
      highlight: !!o.highlight,
      uncurated: false,
      scholarIds: gs?.scholarIds ?? o.scholar_ids ?? [],
    });
  }

  // Uncurated, recent papers from GS — auto-classify by title.
  for (const [gsKey, gs] of gsMap.entries()) {
    if (consumedGsKeys.has(gsKey)) continue;
    if (!gs.year || gs.year < RECENT_YEAR_CUTOFF) continue;
    const inferredTopic = classifyTitle(gs.title);
    const scanText = `${gs.title} ${gs.venue ?? ""}`;
    out.push({
      id: slugify(gs.title),
      title: gs.title,
      authors: "",
      venue: prettifyVenue(gs.venue),
      year: gs.year,
      citations: gs.citations,
      tags: inferredTopic ? [inferredTopic] : [],
      methods: classifyMethods(scanText),
      platforms: classifyPlatforms(scanText),
      highlight: false,
      uncurated: true,
      scholarIds: gs.scholarIds,
    });
  }

  // Sort: year desc (nulls last), then citations desc, then title asc
  out.sort((a, b) => {
    const ay = a.year ?? -1;
    const by = b.year ?? -1;
    if (ay !== by) return by - ay;
    if (a.citations !== b.citations) return b.citations - a.citations;
    return a.title.localeCompare(b.title);
  });

  return out;
}

function countFacet(pubs: Publication[], pick: (p: Publication) => string[]) {
  const counts = new Map<string, number>();
  for (const p of pubs) {
    for (const v of pick(p)) counts.set(v, (counts.get(v) ?? 0) + 1);
  }
  return [...counts.entries()]
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => b.count - a.count);
}

export function allTags(pubs: Publication[]): { tag: string; count: number }[] {
  return countFacet(pubs, (p) => p.tags).map(({ value, count }) => ({ tag: value, count }));
}

export function allMethods(pubs: Publication[]): { method: string; count: number }[] {
  return countFacet(pubs, (p) => p.methods).map(({ value, count }) => ({ method: value, count }));
}

export function allPlatforms(pubs: Publication[]): { platform: string; count: number }[] {
  return countFacet(pubs, (p) => p.platforms).map(({ value, count }) => ({ platform: value, count }));
}

export function allYears(pubs: Publication[]): number[] {
  const ys = new Set<number>();
  for (const p of pubs) if (p.year) ys.add(p.year);
  return [...ys].sort((a, b) => b - a);
}
