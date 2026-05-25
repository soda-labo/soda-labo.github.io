#!/bin/zsh
# Install (or reinstall) the weekly Scholar-citation refresh as a launchd job.
# Idempotent: safe to re-run.

set -eu

SCRIPT_DIR="${0:A:h}"
TEMPLATE="$SCRIPT_DIR/com.sodalab.citations.plist"
UPDATE_SCRIPT="$SCRIPT_DIR/update_citations.sh"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCHD_DIR/com.sodalab.citations.plist"
LOG_PATH="$HOME/Library/Logs/sodalab-citations.log"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Template not found: $TEMPLATE" >&2
  exit 1
fi
if [[ ! -x "$UPDATE_SCRIPT" ]]; then
  echo "Wrapper script not executable: $UPDATE_SCRIPT" >&2
  exit 1
fi

mkdir -p "$LAUNCHD_DIR"

# Unload old version if present (ignore errors)
launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true

# Render template with absolute paths
sed \
  -e "s|__SCRIPT_PATH__|$UPDATE_SCRIPT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$TEMPLATE" > "$INSTALLED_PLIST"

launchctl load "$INSTALLED_PLIST"

echo "✓ Installed:  $INSTALLED_PLIST"
echo "  Wrapper:    $UPDATE_SCRIPT"
echo "  Logs:       $LOG_PATH"
echo
echo "Next steps:"
echo "  • Force a one-off run now to confirm it works:"
echo "      launchctl start com.sodalab.citations"
echo "      tail -f $LOG_PATH"
echo "  • To uninstall later:"
echo "      launchctl unload $INSTALLED_PLIST && rm $INSTALLED_PLIST"
