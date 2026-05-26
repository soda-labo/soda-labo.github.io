/**
 * News items loader.
 *
 * Input: src/data/news.yml — entries shaped like
 *   - date: "June 2025"
 *     headline: "<html with anchors>"
 *
 * Output: NewsItem[] sorted newest first.
 *
 * "Month YYYY" strings are parsed into a sortable timestamp; entries
 * with unrecognised dates fall to the bottom but keep their original
 * order.
 */
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const DATA_DIR = path.resolve(process.cwd(), "src/data");

export type NewsItem = {
  date: string;          // raw display string, e.g. "June 2025"
  headline: string;      // HTML
  sortKey: number;       // unix-ms; higher = newer
};

type RawEntry = { date?: string; headline?: string };

const MONTHS: Record<string, number> = {
  jan: 0, january: 0,
  feb: 1, february: 1,
  mar: 2, march: 2,
  apr: 3, april: 3,
  may: 4,
  jun: 5, june: 5,
  jul: 6, july: 6,
  aug: 7, august: 7,
  sep: 8, sept: 8, september: 8,
  oct: 9, october: 9,
  nov: 10, november: 10,
  dec: 11, december: 11,
};

/** Parse strings like "June 2025", "Sep 2024", "01. Sept 2015" → ms since epoch.
 *  Returns 0 for unparseable inputs. */
function parseDate(raw: string): number {
  if (!raw) return 0;
  // Try to find "Month YYYY"
  const m = raw.match(/(\d{1,2}\.?\s*)?([A-Za-z]+)\.?\s*(\d{4})/);
  if (!m) return 0;
  const day = m[1] ? parseInt(m[1].replace(/[.\s]/g, ""), 10) : 1;
  const month = MONTHS[m[2].toLowerCase()];
  const year = parseInt(m[3], 10);
  if (month === undefined || Number.isNaN(year)) return 0;
  return Date.UTC(year, month, day || 1);
}

export function loadNews(): NewsItem[] {
  const file = path.join(DATA_DIR, "news.yml");
  if (!fs.existsSync(file)) return [];
  const raw = (yaml.load(fs.readFileSync(file, "utf8")) ?? []) as RawEntry[];
  const items: NewsItem[] = raw
    .filter((e) => e && (e.headline ?? "").trim().length > 0)
    .map((e, i) => ({
      date: (e.date ?? "").trim(),
      headline: (e.headline ?? "").trim(),
      sortKey: parseDate(e.date ?? "") || (-i), // unknown dates keep file order
    }));
  items.sort((a, b) => b.sortKey - a.sortKey);
  return items;
}
