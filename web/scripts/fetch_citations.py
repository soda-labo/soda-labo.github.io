"""Refresh src/data/scholar_cache.json from Google Scholar.

Run from the web/ project root (or from anywhere via the update wrapper).
Exits 0 on success or no-change, non-zero on hard failure (e.g., CAPTCHA).
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from scholarly import scholarly

AUTHORS = {
    "haewoon_kwak": "dcjrz5MAAAAJ",
    "jisun_an": "FYtw3zkAAAAJ",
}

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "src" / "data" / "scholar_cache.json"


def fetch_author(name: str, scholar_id: str) -> dict:
    print(f"[{name}] fetching profile {scholar_id} ...", flush=True)
    t0 = time.time()
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["basics", "indices", "publications"])
    elapsed = time.time() - t0
    pubs = []
    for p in author.get("publications", []):
        bib = p.get("bib", {})
        pubs.append({
            "title": bib.get("title"),
            "year": bib.get("pub_year"),
            "venue": bib.get("citation"),
            "citations": p.get("num_citations", 0),
            "scholar_id": p.get("author_pub_id"),
        })
    print(f"[{name}] {len(pubs)} pubs, total cites {author.get('citedby')}, "
          f"h={author.get('hindex')} ({elapsed:.1f}s)", flush=True)
    return {
        "name": name,
        "scholar_id": scholar_id,
        "display_name": author.get("name"),
        "affiliation": author.get("affiliation"),
        "total_citations": author.get("citedby"),
        "h_index": author.get("hindex"),
        "i10_index": author.get("i10index"),
        "num_publications": len(pubs),
        "fetched_in_seconds": round(elapsed, 1),
        "publications": pubs,
    }


def main() -> int:
    print(f"Updating {OUT_PATH}")
    print(f"Fetched at: {datetime.now(timezone.utc).isoformat()}")
    results: dict = {}
    hard_failure = False
    for name, sid in AUTHORS.items():
        try:
            results[name] = fetch_author(name, sid)
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            print(f"[{name}] FAILED: {msg}", flush=True)
            results[name] = {"error": msg, "scholar_id": sid}
            blocked = (
                "captcha" in str(e).lower()
                or "MaxTriesExceeded" in type(e).__name__
            )
            if blocked:
                print("  → looks like Scholar blocked us. Aborting.", flush=True)
                hard_failure = True
                break
        time.sleep(2)

    if hard_failure:
        # Don't overwrite cache with a partial/failed result
        return 2

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
