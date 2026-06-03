#!/bin/zsh
# Weekly cron job: refresh GS citations, commit & push if anything changed.
# Run by launchd; logs to ~/Library/Logs/sodalab-citations.log

set -u
set -o pipefail

# Resolve repo root from this script's location
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="${SCRIPT_DIR:h}"
VENV="$SCRIPT_DIR/.venv"
DATA_FILE="$REPO_ROOT/src/data/scholar_cache.json"
OVERRIDES="$REPO_ROOT/src/data/overrides.yml"
BRANCH=$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)

echo "=== $(date -Iseconds) ==="
echo "repo:   $REPO_ROOT"
echo "branch: $BRANCH"

# Load .env if present (API keys etc.) so child Python scripts inherit them.
# The .env file is gitignored.
if [[ -f "$REPO_ROOT/.env" ]]; then
  set -a
  source "$REPO_ROOT/.env"
  set +a
  echo "Loaded $REPO_ROOT/.env"
fi

# Make sure venv exists (auto-bootstrap on first run). Some of our scripts
# use PEP 604 union syntax (X | None) which needs Python 3.10+, so prefer
# a modern Homebrew interpreter and fall back to /usr/bin/python3 only when
# nothing else is around.
PYBIN=""
for candidate in /opt/homebrew/bin/python3.14 /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3 python3 /usr/bin/python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYBIN="$candidate"; break
  fi
done
if [[ -z "$PYBIN" ]]; then
  echo "No python3 found on PATH." >&2
  exit 1
fi

# If the existing venv is on Python <3.10, rebuild it.
if [[ -x "$VENV/bin/python" ]]; then
  if ! "$VENV/bin/python" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
    echo "Existing venv is Python <3.10, rebuilding with $PYBIN"
    rm -rf "$VENV"
  fi
fi
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating venv at $VENV (using $PYBIN)"
  "$PYBIN" -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet scholarly
fi

# 1) Fetch Scholar
"$VENV/bin/python" "$SCRIPT_DIR/fetch_citations.py"
FETCH_RC=$?
if [[ $FETCH_RC -ne 0 ]]; then
  echo "FAIL: fetch_citations.py exited $FETCH_RC; not committing."
  exit $FETCH_RC
fi

# Make sure pyyaml + Pillow are around (sync_overrides + optimize_pubpics need them)
"$VENV/bin/python" -c "import yaml" 2>/dev/null || "$VENV/bin/pip" install --quiet pyyaml
"$VENV/bin/python" -c "from PIL import Image" 2>/dev/null || "$VENV/bin/pip" install --quiet Pillow

# 2) Sync overrides.yml with any new GS papers (additive, preserves edits)
"$VENV/bin/python" "$SCRIPT_DIR/sync_overrides.py"

# 3) Backfill missing author lists via OpenAlex/Semantic Scholar (idempotent —
#    skips entries that already have authors). Only hits the API for new papers
#    that sync_overrides just added.
"$VENV/bin/python" "$SCRIPT_DIR/fetch_authors.py" --apply

# 4) Backfill missing paper links (publisher landing page, arXiv, DOI).
#    Idempotent — skips entries that already have link.url.
"$VENV/bin/python" "$SCRIPT_DIR/fetch_links.py" --apply

# 5) Auto-extract paper thumbnails from open-access PDFs (figure first, fall
#    back to first-page render). Only runs on entries missing an image and
#    with a downloadable PDF; results land in public/pubpic/ as raw PNG.
#    Needs PyMuPDF — `pip install pymupdf` if it's missing in the venv.
"$VENV/bin/python" -c "import fitz" 2>/dev/null || "$VENV/bin/pip" install --quiet pymupdf
"$VENV/bin/python" "$SCRIPT_DIR/fetch_thumbnails.py" --apply

# 6) Optimize any new/oversize publication thumbnails (cached, idempotent —
#    converts the PNGs from step 5 to 336x336 WebP and updates overrides.yml).
"$VENV/bin/python" "$SCRIPT_DIR/optimize_pubpics.py"

# Commit & push only if anything actually changed
cd "$REPO_ROOT" || exit 1
PUBPIC_DIR="$REPO_ROOT/public/pubpic"
if git diff --quiet -- "$DATA_FILE" "$OVERRIDES" "$PUBPIC_DIR" 2>/dev/null \
   && [ -z "$(git status --porcelain -- "$PUBPIC_DIR")" ]; then
  echo "Nothing changed — nothing to commit."
  exit 0
fi

git diff --stat -- "$DATA_FILE" "$OVERRIDES" 2>/dev/null
git status --short -- "$PUBPIC_DIR"

git add "$DATA_FILE" "$OVERRIDES" "$PUBPIC_DIR"
git commit -m "chore: refresh Scholar citations, sync overrides, optimize images ($(date +%Y-%m-%d))"
git push origin "$BRANCH"
echo "Pushed update to origin/$BRANCH."

# ── Sync Haewoon's personal site stats from the same scholar cache ───────────
# Reads scholar_cache.json (just updated above) and rewrites the
# data-stat="..." spans on the personal site's index.html, then pushes if
# anything changed. No extra GS fetch — same cache, two sites.
PERSONAL_REPO="$HOME/Projects/haewoon.github.io"
if [[ -f "$PERSONAL_REPO/update_stats.py" ]]; then
  echo
  echo "Syncing personal site stats…"
  /usr/bin/env python3 "$PERSONAL_REPO/update_stats.py"
  cd "$PERSONAL_REPO" || exit 0
  if ! git diff --quiet -- index.html; then
    git add index.html
    git commit -m "chore: refresh Scholar stats ($(date +%Y-%m-%d))"
    git push origin master
    echo "Pushed personal site update."
  else
    echo "Personal site already up to date."
  fi
fi
