"""Backfill missing `authors` fields in overrides.yml from cached OA/S2 IDs.

For every visible override entry without authors:
  1. If we cached an openalex_id, fetch the work and read authorships[].author.display_name.
  2. Else if we cached an s2_id, fetch the paper with fields=authors and read authors[].name.
  3. Format as "First Last, First Last, ..." (preserving order from the source).

Idempotent — entries already carrying an authors string are skipped.

Usage:
  python fetch_authors.py             # dry-run, prints what it'd write
  python fetch_authors.py --apply     # write to overrides.yml in place
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
            if e.code == 404:
                return None
            if attempt + 1 == retries: return None
            time.sleep(1)
        except Exception:
            if attempt + 1 == retries: return None
            time.sleep(1)
    return None


def normalize_name(name: str) -> str:
    """OpenAlex returns some names as 'Last, First Middle' which breaks
    comma-joined author lists. Flip those to 'First Middle Last'. Names with
    no comma or with multiple commas are returned unchanged."""
    name = name.strip()
    if name.count(",") != 1:
        return name
    last, first = (s.strip() for s in name.split(","))
    # If last-part contains spaces it's probably already 'First Last, Jr.' etc.
    if " " in last or not first:
        return name
    return f"{first} {last}"


def fetch_oa_authors(openalex_id: str) -> list[str]:
    """openalex_id may be a full URL (openalex.org/W…) or just W…; normalize
    to the API endpoint api.openalex.org/works/W… and fetch."""
    m = re.search(r"W\d+", openalex_id)
    if not m:
        return []
    wid = m.group(0)
    url = f"https://api.openalex.org/works/{wid}?select=authorships"
    data = get_json(url, HEADERS_OA)
    if not data: return []
    names: list[str] = []
    for a in (data.get("authorships") or []):
        # Prefer raw_author_name (usually 'First Last') over display_name
        # (which sometimes flips to 'Last, First' for ORCID-linked authors).
        raw = a.get("raw_author_name")
        disp = (a.get("author") or {}).get("display_name")
        name = normalize_name(raw or disp or "")
        if name and name not in names:
            names.append(name)
    return names


def fetch_s2_authors(s2_id: str) -> list[str]:
    url = f"https://api.semanticscholar.org/graph/v1/paper/{s2_id}?fields=authors"
    data = get_json(url, HEADERS_S2)
    if not data: return []
    return [a.get("name") for a in (data.get("authors") or []) if a.get("name")]


def main() -> int:
    apply = "--apply" in sys.argv
    overrides = yaml.safe_load(OVERRIDES.read_text())
    abs_data = json.loads(ABSTRACTS.read_text()) if ABSTRACTS.exists() else {}

    targets = []
    for slug, e in overrides.items():
        if not isinstance(e, dict): continue
        if e.get("hide"): continue
        if (e.get("authors") or "").strip(): continue
        targets.append(slug)

    print(f"Visible entries missing authors: {len(targets)}")
    print(f"Mode: {'APPLY (writing to overrides.yml)' if apply else 'DRY-RUN (no writes)'}")
    print()

    n_oa = n_s2 = n_skip = n_fail = 0
    new_authors: dict[str, str] = {}

    for i, slug in enumerate(targets, 1):
        a = abs_data.get(slug, {})
        oa = a.get("openalex_id")
        s2 = a.get("s2_id")
        title = overrides[slug].get("title", "")[:55]

        names: list[str] = []
        source = ""
        if oa:
            names = fetch_oa_authors(oa)
            time.sleep(SLEEP_OA)
            source = "oa"
            if names: n_oa += 1
        if not names and s2:
            names = fetch_s2_authors(s2)
            time.sleep(SLEEP_S2)
            source = "s2"
            if names: n_s2 += 1

        if not names:
            why = "no OA/S2 ID cached" if not (oa or s2) else f"fetch returned empty ({oa and 'oa'}{' ' if oa and s2 else ''}{s2 and 's2'})"
            print(f"  [{i:>2}/{len(targets)}] ✗ skip ({why}): {title}")
            n_skip += 1
            continue

        authors_str = ", ".join(names)
        new_authors[slug] = authors_str
        print(f"  [{i:>2}/{len(targets)}] ✓ ({source}, {len(names)}) {title}")
        print(f"             {authors_str[:120]}")

    print()
    print(f"OA fetched:  {n_oa}")
    print(f"S2 fetched:  {n_s2}")
    print(f"Skipped:     {n_skip}")
    print(f"Failed:      {n_fail}")

    if apply and new_authors:
        for slug, s in new_authors.items():
            overrides[slug]["authors"] = s
        OVERRIDES.write_text(
            yaml.dump(overrides, sort_keys=False, allow_unicode=True, width=200)
        )
        print(f"\n✓ Wrote {len(new_authors)} authors to {OVERRIDES.relative_to(ROOT)}")
    elif new_authors:
        print(f"\n(dry-run) {len(new_authors)} entries would be updated. Pass --apply to write.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
