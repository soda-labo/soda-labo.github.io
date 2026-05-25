"""Apply a {slug: description} JSON map to overrides.yml in place.

Usage: python apply_descriptions.py /path/to/descs.json
"""
import sys, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"


def main(json_path: str) -> int:
    new_descs: dict[str, str] = json.loads(Path(json_path).read_text())
    overrides = yaml.safe_load(OVERRIDES.read_text())
    if not isinstance(overrides, dict):
        print("overrides.yml not a dict", file=sys.stderr); return 1

    applied, skipped = [], []
    for slug, desc in new_descs.items():
        if slug not in overrides:
            skipped.append(slug)
            continue
        overrides[slug]["description"] = desc
        applied.append((slug, len(desc)))

    OVERRIDES.write_text(yaml.dump(overrides, sort_keys=False, allow_unicode=True, width=200))

    print(f"Applied: {len(applied)} | Skipped (slug not found): {len(skipped)}")
    if applied:
        avg = sum(l for _, l in applied) / len(applied)
        mn = min(l for _, l in applied)
        mx = max(l for _, l in applied)
        print(f"Description length — min {mn}, avg {avg:.0f}, max {mx} chars")
    for s in skipped:
        print(f"  ! not found: {s}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: apply_descriptions.py <descs.json>", file=sys.stderr); sys.exit(1)
    sys.exit(main(sys.argv[1]))
