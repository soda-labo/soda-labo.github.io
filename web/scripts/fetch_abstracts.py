"""Fetch each paper's abstract from OpenAlex, with Semantic Scholar fallback.

For every entry in overrides.yml:
  1. Try OpenAlex by DOI (extracted from link.url), then by title search.
  2. Reconstruct the abstract from OpenAlex's inverted index.
  3. If the result looks like a mismatch (low keyword overlap with the title)
     OR no abstract was found, fall back to Semantic Scholar.

Results are cached in scripts/abstracts.json. Idempotent by default.

Usage:
  python fetch_abstracts.py                  # fetch missing only
  python fetch_abstracts.py --refresh        # re-fetch everything from scratch
  python fetch_abstracts.py --s2-fallback    # only retry low-quality cached entries via S2

Optional env var: SEMANTIC_SCHOLAR_API_KEY  (free key bumps S2 to 1 req/s)
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"
OUT = Path(__file__).parent / "abstracts.json"


def load_dotenv() -> None:
    """Read KEY=value lines from web/.env into os.environ if present.

    Native parser — no python-dotenv dependency. Lines starting with '#' are
    skipped; quotes around values are stripped. Existing env vars win, so
    `export FOO=bar python script.py` always overrides the file.
    """
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


load_dotenv()

OPENALEX_BASE = "https://api.openalex.org/works"
S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
S2_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

HEADERS_OA = {
    "User-Agent": "SoDA-Lab-website-builder/1.0 (mailto:hwkwak@iu.edu)",
}
HEADERS_S2 = {
    "User-Agent": "SoDA-Lab-website-builder/1.0 (mailto:hwkwak@iu.edu)",
}
if S2_KEY:
    HEADERS_S2["x-api-key"] = S2_KEY

SLEEP_OA = 0.12     # ~8 req/s, well under OpenAlex polite-pool limit
SLEEP_S2 = 1.1 if S2_KEY else 3.1  # 1 req/s with key, ~0.33/s without

# Minimum keyword overlap between paper title and fetched abstract to consider
# the match valid. OpenAlex's fuzzy-title search occasionally returns a
# completely different paper (DeepSeek → SME paper, Urban Trajectory →
# Panjabi ethnography). Below this threshold we'd rather have no abstract.
MIN_OVERLAP = 0.30
# Stricter floor on title-vs-matched-title overlap. Catches the case where
# two distinct papers share much of the same generic vocabulary (e.g. two
# LLM papers) so the abstract-overlap heuristic alone passes them through.
MIN_TITLE_OVERLAP = 0.50

# Stopwords for keyword-overlap heuristic
STOP = {
    "the","and","with","from","for","over","using","this","that","their","have",
    "these","what","when","where","while","how","why","into","about","across",
    "more","most","than","then","they","through","upon","under","such","other",
    "also","based","study","case","data","model","models","method","methods",
    "analysis","approach","results","paper","article","research","towards","via",
    "between","being","both","each","does","done","much","very","into","onto",
    "ourselves","its","our","are","was","were","not","but","can","may","new",
}


# ── helpers ──────────────────────────────────────────────────────────────────
def reconstruct_abstract(inv_index: dict | None) -> str | None:
    if not inv_index:
        return None
    word_at: dict[int, str] = {}
    for w, positions in inv_index.items():
        for p in positions:
            word_at[p] = w
    if not word_at:
        return None
    return " ".join(word_at[i] for i in range(max(word_at.keys()) + 1) if i in word_at)


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)
def extract_doi(url: str | None) -> str | None:
    if not url:
        return None
    m = DOI_RE.search(url)
    if m:
        return m.group(0).rstrip(".)")
    m = re.search(r"nature\.com/articles/([a-z0-9-]+)", url, re.I)
    if m:
        return f"10.1038/{m.group(1)}"
    return None


def get_json(url: str, headers: dict | None = None, retries: int = 3) -> dict | None:
    h = headers or HEADERS_OA
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            if e.code == 404:
                return None
            if attempt + 1 == retries:
                return None
            time.sleep(1)
        except Exception:
            if attempt + 1 == retries:
                return None
            time.sleep(1)
    return None


def keyword_overlap(title: str, abstract: str | None) -> float:
    """Fraction of title's non-stop words that appear in the abstract."""
    if not abstract or not title:
        return 0.0
    t_words = {w for w in re.findall(r"[a-z]{4,}", title.lower()) if w not in STOP}
    a_words = set(re.findall(r"[a-z]{4,}", abstract.lower()))
    if not t_words:
        return 0.0
    return len(t_words & a_words) / len(t_words)


# ── OpenAlex ─────────────────────────────────────────────────────────────────
def oa_by_doi(doi: str) -> dict | None:
    return get_json(f"{OPENALEX_BASE}/doi:{urllib.parse.quote(doi, safe='/')}", HEADERS_OA)


def oa_search_title(title: str) -> dict | None:
    fields = "id,doi,title,display_name,abstract_inverted_index,publication_year"
    url = f"{OPENALEX_BASE}?search={urllib.parse.quote(title)}&per_page=3&select={fields}"
    data = get_json(url, HEADERS_OA)
    if data and data.get("results"):
        return data["results"][0]
    return None


# ── Semantic Scholar ─────────────────────────────────────────────────────────
S2_FIELDS = "title,abstract,year,externalIds"


def s2_by_doi(doi: str) -> dict | None:
    if not doi:
        return None
    safe = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
    return get_json(f"{S2_BASE}/DOI:{urllib.parse.quote(safe, safe='/')}?fields={S2_FIELDS}", HEADERS_S2)


def s2_search_title(title: str) -> dict | None:
    # `match` endpoint returns the single best title match — perfect here
    match_url = f"{S2_BASE}/search/match?query={urllib.parse.quote(title)}&fields={S2_FIELDS}"
    res = get_json(match_url, HEADERS_S2)
    if res and res.get("data"):
        return res["data"][0]
    # fall back to regular search
    url = f"{S2_BASE}/search?query={urllib.parse.quote(title)}&limit=3&fields={S2_FIELDS}"
    res = get_json(url, HEADERS_S2)
    if res and res.get("data"):
        return res["data"][0]
    return None


# ── caching ──────────────────────────────────────────────────────────────────
def load_cache() -> dict:
    if OUT.exists():
        try: return json.loads(OUT.read_text())
        except Exception: return {}
    return {}


def save_cache(cache: dict) -> None:
    OUT.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def fetch_one_oa(title: str, doi: str | None) -> tuple[str | None, dict | None, str]:
    """Try OpenAlex by DOI then title. Returns (abstract, work, method)."""
    if doi:
        work = oa_by_doi(doi)
        if work:
            inv = work.get("abstract_inverted_index")
            return (reconstruct_abstract(inv) if inv else None), work, "openalex-doi"
    if title:
        work = oa_search_title(title)
        if work:
            inv = work.get("abstract_inverted_index")
            return (reconstruct_abstract(inv) if inv else None), work, "openalex-title"
    return None, None, "fail"


def fetch_one_s2(title: str, doi: str | None) -> tuple[str | None, dict | None, str]:
    """Try Semantic Scholar by DOI then title."""
    if doi:
        work = s2_by_doi(doi)
        if work and work.get("abstract"):
            return work["abstract"], work, "s2-doi"
    if title:
        work = s2_search_title(title)
        if work and work.get("abstract"):
            return work["abstract"], work, "s2-title"
    return None, work if "work" in dir() else None, "s2-fail"


def best_of(title: str, candidates: list[tuple[str | None, dict | None, str]]):
    """Pick the candidate with the highest title-keyword overlap.

    Also computes a title-vs-matched-title overlap so the caller can detect
    cases where the search engine returned an unrelated paper that happens to
    share many words with the query title in its abstract (e.g. an LLM paper
    matched to a different LLM paper). Returns (abstract, work, method).
    """
    scored = [(keyword_overlap(title, a), a, w, m) for a, w, m in candidates if a]
    if not scored:
        return None, None, "none"
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1], scored[0][2], scored[0][3]


def matched_title_overlap(title: str, work: dict | None) -> float:
    """How many of the query title's distinctive words appear in the
    matched work's title. Catches wrong-paper matches where abstracts
    share lots of common terms (e.g. generic LLM vocabulary)."""
    if not work:
        return 1.0  # no way to check; don't penalize
    mt = work.get("title") or work.get("display_name") or ""
    if not mt:
        return 1.0
    return keyword_overlap(title, mt)


# ── main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    refresh = "--refresh" in sys.argv
    s2_only = "--s2-fallback" in sys.argv
    overrides = yaml.safe_load(OVERRIDES.read_text())
    if not isinstance(overrides, dict):
        print("ERROR: overrides.yml not a dict", file=sys.stderr); return 1

    cache = load_cache() if not refresh else {}

    print(f"S2 API key: {'set' if S2_KEY else 'not set (using slower public access)'}")
    print(f"Mode: {'s2-fallback' if s2_only else ('refresh' if refresh else 'add-missing')}\n")

    n_oa_new = n_s2_fallback = n_skip = n_fail = 0

    for i, (slug, entry) in enumerate(overrides.items(), 1):
        title = entry.get("title", "")
        if not title:
            continue
        doi = extract_doi((entry.get("link") or {}).get("url"))

        existing = cache.get(slug) or {}
        existing_abs = existing.get("abstract")
        existing_overlap = keyword_overlap(title, existing_abs)

        # Decide what to do
        if s2_only:
            # Skip if existing entry is already high-quality
            if existing_abs and existing_overlap >= MIN_OVERLAP:
                n_skip += 1
                continue
            # Try S2 only
            print(f"  [{i:>3}/{len(overrides)}] retrying via S2: {title[:60]}")
            abs_s2, work_s2, m_s2 = fetch_one_s2(title, doi)
            time.sleep(SLEEP_S2)
            candidates = []
            if existing_abs:
                candidates.append((existing_abs, None, existing.get("method", "openalex")))
            if abs_s2:
                candidates.append((abs_s2, work_s2, m_s2))
            chosen, work, method = best_of(title, candidates)
            if chosen and chosen != existing_abs:
                n_s2_fallback += 1
                cache[slug] = {
                    "title": title,
                    "matched_title": (work or {}).get("title") if work else existing.get("matched_title"),
                    "abstract": chosen,
                    "method": method,
                    "doi": (work or {}).get("externalIds", {}).get("DOI") if work else existing.get("doi"),
                    "openalex_id": existing.get("openalex_id"),
                    "s2_id": (work or {}).get("paperId") if work else None,
                    "overlap": round(keyword_overlap(title, chosen), 2),
                }
                print(f"    ✓ S2 better (overlap {existing_overlap:.2f} → {keyword_overlap(title, chosen):.2f})")
            elif chosen:
                n_skip += 1
                print(f"    ○ kept existing (S2 found nothing better)")
            else:
                n_fail += 1
                print(f"    ✗ S2 also failed")
            continue

        # Default add-missing or refresh mode
        if not refresh and existing_abs and existing_overlap >= MIN_OVERLAP:
            n_skip += 1
            continue

        # On --refresh, try BOTH sources and keep whichever scores better.
        # On add-missing, OpenAlex first; S2 only as fallback for misses.
        abs_oa, work_oa, m_oa = fetch_one_oa(title, doi)
        time.sleep(SLEEP_OA)

        if not refresh and abs_oa and keyword_overlap(title, abs_oa) >= MIN_OVERLAP:
            # OpenAlex looks fine — skip S2 to save time
            cache[slug] = {
                "title": title,
                "matched_title": (work_oa or {}).get("title") or (work_oa or {}).get("display_name"),
                "abstract": abs_oa,
                "method": m_oa,
                "doi": (work_oa or {}).get("doi"),
                "openalex_id": (work_oa or {}).get("id"),
                "overlap": round(keyword_overlap(title, abs_oa), 2),
            }
            n_oa_new += 1
            print(f"  [{i:>3}/{len(overrides)}] ✓ ({m_oa}) {title[:60]}")
            continue

        # Try S2 (always on refresh, as fallback otherwise)
        abs_s2, work_s2, m_s2 = fetch_one_s2(title, doi)
        time.sleep(SLEEP_S2)
        candidates = []
        if abs_oa:
            candidates.append((abs_oa, work_oa, m_oa))
        if abs_s2:
            candidates.append((abs_s2, work_s2, m_s2))
        chosen, work, method = best_of(title, candidates)
        chosen_overlap = keyword_overlap(title, chosen) if chosen else 0.0
        mt_overlap = matched_title_overlap(title, work) if chosen else 0.0
        # Reject low-overlap matches — OpenAlex/S2 search can return a totally
        # different paper that shares a few common words. Two checks:
        #   (a) abstract keyword overlap with title (catches obvious topic shifts)
        #   (b) matched_title overlap with title (catches "different paper, same
        #       generic vocabulary" cases like an LLM paper matched to another)
        if chosen and (chosen_overlap < MIN_OVERLAP or mt_overlap < MIN_TITLE_OVERLAP):
            mt = (work or {}).get("title") or (work or {}).get("display_name") or ""
            tag = (f"mismatch reject, abs={chosen_overlap:.2f} title={mt_overlap:.2f} "
                   f"matched=\"{mt[:50]}\"")
            cache[slug] = {
                "title": title, "abstract": None, "method": "fail-mismatch",
                "matched_title": mt or None,
                "doi": None, "openalex_id": None,
            }
            n_fail += 1
            print(f"  [{i:>3}/{len(overrides)}] ✗ ({tag}) {title[:40]}")
            continue
        if chosen:
            cache[slug] = {
                "title": title,
                "matched_title": (work or {}).get("title") or (work or {}).get("display_name"),
                "abstract": chosen,
                "method": method,
                "doi": (work or {}).get("doi") or (work or {}).get("externalIds", {}).get("DOI") if work else None,
                "openalex_id": (work or {}).get("id") if "openalex" in method else None,
                "s2_id": (work or {}).get("paperId") if "s2" in method else None,
                "overlap": round(chosen_overlap, 2),
            }
            if "s2" in method:
                n_s2_fallback += 1
            else:
                n_oa_new += 1
            # Show winner notation when both sources had something
            tag = f"{method}"
            if abs_oa and abs_s2:
                oa_score = keyword_overlap(title, abs_oa)
                s2_score = keyword_overlap(title, abs_s2)
                tag = f"{method}, OA={oa_score:.2f} S2={s2_score:.2f}"
            print(f"  [{i:>3}/{len(overrides)}] ✓ ({tag}) {title[:55]}")
        else:
            cache[slug] = {
                "title": title, "abstract": None, "method": "fail",
                "matched_title": None, "doi": None, "openalex_id": None,
            }
            n_fail += 1
            print(f"  [{i:>3}/{len(overrides)}] ✗ {title[:60]}")

    save_cache(cache)
    print()
    print(f"OpenAlex new/refreshed:  {n_oa_new}")
    print(f"S2 fallback used:        {n_s2_fallback}")
    print(f"Skipped (already good):  {n_skip}")
    print(f"Failed:                  {n_fail}")
    total_with_abs = sum(1 for r in cache.values() if r.get("abstract"))
    print(f"\nTotal cache: {len(cache)} entries, {total_with_abs} with abstract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
