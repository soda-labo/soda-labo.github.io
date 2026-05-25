"""Auto-generate paper thumbnails from open-access PDFs.

For every visible override without an `image:` field:
  1. Resolve a PDF URL — arXiv-DOI → arxiv.org/pdf/<id>, link.url if it's
     already arXiv or ends in .pdf, else OpenAlex/S2 open-access PDF URL.
  2. Download the PDF (cached in scripts/.pdf_cache/).
  3. Hybrid extraction:
       (a) scan the first 3 pages for embedded images, pick the largest
           "figure-shaped" one (>= 300px on both sides, aspect 0.3..3.0);
       (b) fall back to a 2x render of page 1.
  4. Save as `public/pubpic/<slug>.png`. optimize_pubpics.py will then
     center-crop + downscale + convert to WebP, and the next sync_overrides
     run finds the file.
  5. Set `image: <slug>.png` on the override.

Idempotent — entries that already have an image are skipped. Failures
(closed access, scanned PDFs, etc.) are reported but don't crash the run.

Usage:
  python fetch_thumbnails.py              # dry-run, prints what it'd do
  python fetch_thumbnails.py --apply      # download + write images
  python fetch_thumbnails.py --apply --slug=foo,bar   # only specific slugs
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr); sys.exit(1)
try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: pip install pymupdf", file=sys.stderr); sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"
ABSTRACTS = Path(__file__).parent / "abstracts.json"
PUBPIC_DIR = ROOT / "public" / "pubpic"
PDF_CACHE = Path(__file__).parent / ".pdf_cache"
PDF_CACHE.mkdir(exist_ok=True)


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
HEADERS = {"User-Agent": "SoDA-Lab-website-builder/1.0 (mailto:hwkwak@iu.edu)"}
HEADERS_S2 = dict(HEADERS)
if S2_KEY: HEADERS_S2["x-api-key"] = S2_KEY
SLEEP_API = 0.12          # OpenAlex
SLEEP_S2 = 1.1 if S2_KEY else 3.1
SLEEP_PDF = 3.0           # be polite to arxiv / publishers

ARXIV_DOI_RE = re.compile(r"10\.48550/arxiv\.([\d.]+)", re.I)
ARXIV_ID_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([\d.]+)", re.I)

# Figure extraction tuning
MIN_FIG_SIDE = 300         # px on smaller side
MAX_ASPECT = 3.0           # w/h or h/w — skip ribbons/banners
FIRST_N_PAGES = 3          # scan pages 1..N for figures


def get_json(url: str, headers: dict) -> dict | None:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception:
        return None


def resolve_pdf_url(slug: str, entry: dict, abs_entry: dict) -> tuple[str | None, str]:
    """Returns (pdf_url, source_tag)."""
    # 1. arXiv-issued DOI → arxiv.org/pdf
    doi = (abs_entry.get("doi") or "")
    m = ARXIV_DOI_RE.search(doi)
    if m: return f"https://arxiv.org/pdf/{m.group(1)}", "arxiv-doi"

    # 2. link.url is already arxiv
    link_url = ((entry.get("link") or {}).get("url") or "")
    m = ARXIV_ID_RE.search(link_url)
    if m: return f"https://arxiv.org/pdf/{m.group(1)}", "arxiv-link"

    # 3. link.url is already a PDF
    if link_url.lower().endswith(".pdf"): return link_url, "direct-pdf"

    # 4. OpenAlex best-OA PDF
    oa = abs_entry.get("openalex_id") or ""
    wm = re.search(r"W\d+", oa)
    if wm:
        data = get_json(
            f"https://api.openalex.org/works/{wm.group(0)}"
            "?select=open_access,best_oa_location,primary_location",
            HEADERS,
        )
        time.sleep(SLEEP_API)
        if data:
            for loc_key in ("best_oa_location", "primary_location"):
                pdf = ((data.get(loc_key) or {}).get("pdf_url") or "")
                if pdf: return pdf, f"oa-{loc_key}"
            oa_url = (data.get("open_access") or {}).get("oa_url") or ""
            if oa_url.lower().endswith(".pdf"): return oa_url, "oa-url"

    # 5. S2 openAccessPdf
    s2 = abs_entry.get("s2_id")
    if s2:
        data = get_json(
            f"https://api.semanticscholar.org/graph/v1/paper/{s2}?fields=openAccessPdf",
            HEADERS_S2,
        )
        time.sleep(SLEEP_S2)
        if data:
            pdf = ((data.get("openAccessPdf") or {}).get("url") or "")
            if pdf: return pdf, "s2-oa"

    return None, "none"


def download_pdf(url: str, slug: str) -> Path | None:
    """Cache PDFs to .pdf_cache/<slug>.pdf so reruns don't re-download."""
    cached = PDF_CACHE / f"{slug}.pdf"
    if cached.exists() and cached.stat().st_size > 1000:
        return cached
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if not data.startswith(b"%PDF"):
            return None  # publisher returned an HTML wall, not a PDF
        cached.write_bytes(data)
        time.sleep(SLEEP_PDF)
        return cached
    except Exception:
        return None


def extract_thumbnail(pdf_path: Path, dest: Path) -> str:
    """Try first-figure, fall back to first-page render. Returns method tag."""
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return "open-fail"

    # 1. First-figure extraction
    candidates: list[tuple[int, fitz.Pixmap]] = []
    for page_num in range(min(FIRST_N_PAGES, doc.page_count)):
        page = doc[page_num]
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                pix = fitz.Pixmap(doc, xref)
            except Exception:
                continue
            w, h = pix.width, pix.height
            if w < MIN_FIG_SIDE or h < MIN_FIG_SIDE:
                continue
            ratio = max(w / h, h / w)
            if ratio > MAX_ASPECT:
                continue
            # Convert CMYK or other modes to RGB for PNG
            if pix.n - pix.alpha >= 4:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
            candidates.append((w * h, pix))

    if candidates:
        candidates.sort(reverse=True, key=lambda t: t[0])
        candidates[0][1].save(dest)
        doc.close()
        return "figure"

    # 2. Fallback: render page 1 at 2x (~144 DPI)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(dest)
    doc.close()
    return "page1"


def main() -> int:
    apply = "--apply" in sys.argv
    slug_filter = None
    for arg in sys.argv:
        if arg.startswith("--slug="):
            slug_filter = set(arg.split("=", 1)[1].split(","))

    overrides = yaml.safe_load(OVERRIDES.read_text())
    abs_data = json.loads(ABSTRACTS.read_text()) if ABSTRACTS.exists() else {}

    targets = []
    for slug, e in overrides.items():
        if not isinstance(e, dict): continue
        if e.get("hide"): continue
        if (e.get("image") or "").strip(): continue
        if slug_filter and slug not in slug_filter: continue
        targets.append(slug)

    print(f"Visible entries missing image: {len(targets)}")
    print(f"Mode: {'APPLY' if apply else 'DRY-RUN'}")
    print()

    n_fig = n_page = n_no_pdf = n_dl_fail = 0
    new_images: dict[str, str] = {}

    for i, slug in enumerate(targets, 1):
        title = overrides[slug].get("title", "")[:55]
        pdf_url, source = resolve_pdf_url(slug, overrides[slug], abs_data.get(slug, {}))
        if not pdf_url:
            print(f"  [{i:>2}/{len(targets)}] ✗ no PDF: {title}")
            n_no_pdf += 1
            continue

        if not apply:
            print(f"  [{i:>2}/{len(targets)}] would fetch ({source}): {title}")
            print(f"             {pdf_url[:90]}")
            continue

        pdf_path = download_pdf(pdf_url, slug)
        if not pdf_path:
            print(f"  [{i:>2}/{len(targets)}] ✗ DL fail ({source}): {title}")
            n_dl_fail += 1
            continue

        dest = PUBPIC_DIR / f"{slug[:60]}.png"
        method = extract_thumbnail(pdf_path, dest)
        if method == "figure": n_fig += 1
        elif method == "page1": n_page += 1
        else:
            print(f"  [{i:>2}/{len(targets)}] ✗ extract fail: {title}")
            continue
        new_images[slug] = dest.name
        print(f"  [{i:>2}/{len(targets)}] ✓ ({source} → {method}) {title} → {dest.name}")

    if apply and new_images:
        for slug, img_name in new_images.items():
            overrides[slug]["image"] = img_name
        OVERRIDES.write_text(
            yaml.dump(overrides, sort_keys=False, allow_unicode=True, width=200)
        )
        print(f"\n✓ Set image: on {len(new_images)} entries in overrides.yml")
        print(f"  Run `python scripts/optimize_pubpics.py` to crop+WebP the new images.")

    print()
    print(f"figures: {n_fig} | page-1: {n_page} | no PDF: {n_no_pdf} | DL fail: {n_dl_fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
