"""Backfill missing `link.url` and `link.venue` fields in overrides.yml.

For every visible override entry without a link.url:
  1. If openalex_id cached, fetch the OA work and read:
       primary_location.landing_page_url (best — publisher page)
       open_access.oa_url                 (open-access PDF)
       primary_location.source.display_name (venue)
  2. Else if s2_id cached, fetch S2 paper and read openAccessPdf.url + venue.
  3. Fall back to a doi.org link (canonical) or an arXiv URL if the DOI
     is an arXiv-issued one (10.48550/arxiv.*).

Link priority (best → worst):
  - publisher landing page (DOI on a non-arXiv host)
  - arXiv abs page (when DOI is 10.48550/arxiv.*)
  - open-access PDF (only if no landing page found)
  - doi.org redirect

Idempotent — entries that already have a link.url are skipped.

Usage:
  python fetch_links.py             # dry-run, prints what it'd write
  python fetch_links.py --apply     # write to overrides.yml in place
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"
ABSTRACTS = Path(__file__).parent / "abstracts.json"


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists(): return
    for raw in env.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_dotenv()
S2_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
HEADERS_OA = {"User-Agent": "SoDA-Lab-website-builder/1.0 (mailto:hwkwak@iu.edu)"}
HEADERS_S2 = dict(HEADERS_OA)
if S2_KEY:
    HEADERS_S2["x-api-key"] = S2_KEY
SLEEP_OA = 0.12
SLEEP_S2 = 1.1 if S2_KEY else 3.1


def get_json(url: str, headers: dict, retries: int = 3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt); continue
            if e.code == 404: return None
            if attempt + 1 == retries: return None
            time.sleep(1)
        except Exception:
            if attempt + 1 == retries: return None
            time.sleep(1)
    return None


ARXIV_DOI_RE = re.compile(r"10\.48550/arxiv\.([\d.v]+)", re.I)


def arxiv_url_from_doi(doi: str | None) -> str | None:
    """If the DOI is arXiv-issued, return https://arxiv.org/abs/XXXX instead."""
    if not doi: return None
    m = ARXIV_DOI_RE.search(doi)
    return f"https://arxiv.org/abs/{m.group(1)}" if m else None


def doi_url(doi: str | None) -> str | None:
    if not doi: return None
    doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    return f"https://doi.org/{doi}" if doi else None


def fetch_oa_link(openalex_id: str) -> tuple[str | None, str | None]:
    """Returns (best_url, venue_name).

    Strategy:
      1. If DOI is arXiv-issued, jump to arxiv.org/abs/<id>.
      2. Else use primary_location.landing_page_url if available.
      3. Else use best_oa_location.landing_page_url (open-access copy, may be
         an arXiv version of an otherwise paywalled paper).
      4. Else scan all `locations` for any arxiv.org URL.
      5. Else fall back to doi.org or the OA PDF link.
    """
    m = re.search(r"W\d+", openalex_id or "")
    if not m: return None, None
    wid = m.group(0)
    url = (f"https://api.openalex.org/works/{wid}"
           "?select=doi,primary_location,open_access,locations,best_oa_location")
    data = get_json(url, HEADERS_OA)
    if not data: return None, None

    doi = (data.get("doi") or "").replace("https://doi.org/", "")
    pl = data.get("primary_location") or {}
    bol = data.get("best_oa_location") or {}
    locations = data.get("locations") or []
    venue = ((pl.get("source") or {}).get("display_name")
             or (bol.get("source") or {}).get("display_name"))

    # 1. arXiv DOI → arxiv abs page
    arxiv = arxiv_url_from_doi(doi)
    if arxiv: return arxiv, venue

    # 2. Primary location landing page
    if pl.get("landing_page_url"):
        return pl["landing_page_url"], venue

    # 3. Best OA location landing page
    if bol.get("landing_page_url"):
        return bol["landing_page_url"], venue

    # 4. Scan all locations for an arxiv URL
    for loc in locations:
        for key in ("landing_page_url", "pdf_url"):
            v = loc.get(key) or ""
            if "arxiv.org" in v:
                return v, venue

    # 5. Fall back to doi.org or PDF
    if doi:
        return doi_url(doi), venue
    pdf = pl.get("pdf_url") or bol.get("pdf_url") or (data.get("open_access") or {}).get("oa_url")
    return pdf, venue


def fetch_s2_link(s2_id: str) -> tuple[str | None, str | None]:
    if not s2_id: return None, None
    url = (f"https://api.semanticscholar.org/graph/v1/paper/{s2_id}"
           "?fields=externalIds,openAccessPdf,venue,journal,url")
    data = get_json(url, HEADERS_S2)
    if not data: return None, None
    doi = (data.get("externalIds") or {}).get("DOI")
    arxiv = arxiv_url_from_doi(doi)
    if arxiv: return arxiv, data.get("venue")
    if doi:   return doi_url(doi), data.get("venue")
    pdf = (data.get("openAccessPdf") or {}).get("url")
    if pdf:   return pdf, data.get("venue")
    return data.get("url"), data.get("venue")


def main() -> int:
    apply = "--apply" in sys.argv
    overrides = yaml.safe_load(OVERRIDES.read_text())
    abs_data = json.loads(ABSTRACTS.read_text()) if ABSTRACTS.exists() else {}

    targets = []
    for slug, e in overrides.items():
        if not isinstance(e, dict): continue
        if e.get("hide"): continue
        if ((e.get("link") or {}).get("url") or "").strip(): continue
        targets.append(slug)

    print(f"Visible entries missing link.url: {len(targets)}")
    print(f"Mode: {'APPLY (writing to overrides.yml)' if apply else 'DRY-RUN (no writes)'}")
    print()

    n_oa = n_s2 = n_doi = n_skip = 0
    new_links: dict[str, tuple[str, str | None]] = {}

    for i, slug in enumerate(targets, 1):
        a = abs_data.get(slug, {})
        oa = a.get("openalex_id")
        s2 = a.get("s2_id")
        doi_raw = a.get("doi")
        title = overrides[slug].get("title", "")[:55]

        url: str | None = None
        venue: str | None = None
        source = ""

        if oa:
            url, venue = fetch_oa_link(oa); source = "oa"
            time.sleep(SLEEP_OA)
            if url: n_oa += 1
        if not url and s2:
            url, venue = fetch_s2_link(s2); source = "s2"
            time.sleep(SLEEP_S2)
            if url: n_s2 += 1
        if not url and doi_raw:
            url = arxiv_url_from_doi(doi_raw) or doi_url(doi_raw); source = "doi-only"
            if url: n_doi += 1

        if not url:
            print(f"  [{i:>2}/{len(targets)}] ✗ skip ({source or 'no IDs'}): {title}")
            n_skip += 1
            continue

        new_links[slug] = (url, venue)
        print(f"  [{i:>2}/{len(targets)}] ✓ ({source}) {title}")
        print(f"             {url[:90]}" + (f"  [venue: {venue[:40]}]" if venue else ""))

    print()
    print(f"OA fetched: {n_oa} | S2 fetched: {n_s2} | DOI fallback: {n_doi} | Skipped: {n_skip}")

    if apply and new_links:
        for slug, (url, venue) in new_links.items():
            existing_link = overrides[slug].get("link") or {}
            existing_link["url"] = url
            # Only fill venue if not already set
            if venue and not (existing_link.get("venue") or "").strip():
                existing_link["venue"] = venue
            overrides[slug]["link"] = existing_link
        OVERRIDES.write_text(
            yaml.dump(overrides, sort_keys=False, allow_unicode=True, width=200)
        )
        print(f"\n✓ Wrote {len(new_links)} link(s) to {OVERRIDES.relative_to(ROOT)}")
    elif new_links:
        print(f"\n(dry-run) {len(new_links)} entries would be updated. Pass --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
