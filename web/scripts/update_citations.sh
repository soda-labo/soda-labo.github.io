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

# Make sure venv exists (auto-bootstrap on first run)
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating venv at $VENV"
  /usr/bin/python3 -m venv "$VENV" || python3 -m venv "$VENV"
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

# 4) Optimize any new/oversize publication thumbnails (cached, idempotent)
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
