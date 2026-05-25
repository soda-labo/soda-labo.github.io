"""Resize and compress publication thumbnails in-place.

Scans `public/pubpic/` for images, converts each to a square (center-crop) at
TARGET_SIZE×TARGET_SIZE, re-encodes to WebP for ~70% smaller files, deletes
the original, and rewrites the matching `image:` field in overrides.yml so
the site references stay correct.

Idempotent: skips images that are already at the target dimensions AND that
the file's mtime hasn't been bumped since the last run (cached state in
.optimize_cache.json). Throw any size/aspect at it.

Input supported: JPG/JPEG, PNG, WebP, GIF (first frame only).
Output: WebP unless CONVERT_TO_WEBP is False (then format is preserved).
"""
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)
try:
    import yaml
except ImportError:
    yaml = None  # overrides.yml sync becomes a no-op

# ── Config ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent  # web/
PUBPIC_DIR = ROOT / "public" / "pubpic"
CACHE_FILE = PUBPIC_DIR / ".optimize_cache.json"
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"

# Cards render at 112×112 px; 336px = 3x retina, plenty for the current layout.
# Bump if you ever add a larger detail view.
TARGET_SIZE = 336
JPEG_QUALITY = 85
WEBP_QUALITY = 85
PNG_COMPRESS = 9       # 0-9; 9 = max compression (slower but smaller)

# When True, JPG/PNG/GIF inputs are saved as .webp and the originals deleted.
# Sample run on 67 PNGs measured ~69% size reduction. Switch off if you want
# to keep PNG/JPG outputs for a specific reason.
CONVERT_TO_WEBP = True

# File extensions we'll process. Anything else is left alone.
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def square_crop(img: Image.Image) -> Image.Image:
    """Center-crop to a square, then downscale (never upscale) to TARGET_SIZE.
    Behaves like CSS `object-fit: cover`."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    # Downscale only — small originals keep their native resolution.
    if side > TARGET_SIZE:
        img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
    return img


def save_optimized(img: Image.Image, dest: Path) -> int:
    """Save image to dest with format-appropriate compression. Returns bytes written."""
    suffix = dest.suffix.lower()
    # Pillow needs RGB for JPEG; PNG/WebP can stay as-is (palette/RGBA OK).
    if suffix in (".jpg", ".jpeg"):
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    elif suffix == ".png":
        if img.mode == "P":
            img = img.convert("RGBA")
        img.save(dest, "PNG", optimize=True, compress_level=PNG_COMPRESS)
    elif suffix == ".webp":
        img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
    elif suffix == ".gif":
        # Re-save as PNG (GIFs of static figures don't need animation).
        png_dest = dest.with_suffix(".png")
        if img.mode == "P":
            img = img.convert("RGBA")
        img.save(png_dest, "PNG", optimize=True, compress_level=PNG_COMPRESS)
        dest.unlink()  # remove the original .gif
        return png_dest.stat().st_size
    return dest.stat().st_size


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try: return json.loads(CACHE_FILE.read_text())
        except Exception: return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True))


def sync_overrides_image_refs(rename_map: dict[str, str]) -> int:
    """For every (old_name -> new_name) pair, update matching `image:` fields
    in overrides.yml. Returns the number of entries rewritten."""
    if not rename_map or yaml is None or not OVERRIDES.exists():
        return 0
    data = yaml.safe_load(OVERRIDES.read_text())
    if not isinstance(data, dict):
        return 0
    changed = 0
    for entry in data.values():
        if not isinstance(entry, dict):
            continue
        img = entry.get("image")
        if isinstance(img, str) and img in rename_map:
            entry["image"] = rename_map[img]
            changed += 1
    if changed:
        OVERRIDES.write_text(
            yaml.dump(data, sort_keys=False, allow_unicode=True, width=200)
        )
    return changed


def main() -> int:
    if not PUBPIC_DIR.exists():
        print(f"ERROR: {PUBPIC_DIR} not found", file=sys.stderr); return 1

    cache = load_cache()
    new_cache: dict = {}

    files = sorted(p for p in PUBPIC_DIR.iterdir() if p.suffix.lower() in EXTS and p.is_file())
    print(f"Scanning {PUBPIC_DIR.relative_to(ROOT.parent)} — {len(files)} image(s)")

    processed = 0
    skipped = 0
    total_before = 0
    total_after = 0
    rename_map: dict[str, str] = {}  # old filename → new filename

    for path in files:
        name = path.name
        mtime = path.stat().st_mtime
        size_before = path.stat().st_size
        total_before += size_before

        cached = cache.get(name) or {}
        # Skip if already known-good and unchanged since last optimization.
        # When CONVERT_TO_WEBP is on, we also require the file to already be
        # .webp — otherwise we want to migrate it.
        in_target_format = (
            not CONVERT_TO_WEBP or path.suffix.lower() == ".webp"
        )
        if (
            cached.get("mtime") == mtime
            and cached.get("optimized") is True
            and in_target_format
        ):
            new_cache[name] = cached
            total_after += size_before
            skipped += 1
            continue

        try:
            with Image.open(path) as img:
                # GIFs may be animated; take the first frame.
                if getattr(img, "is_animated", False):
                    img.seek(0)
                w, h = img.size

                # "Final form" = already square AND smaller-or-equal-to target
                # AND format we want to keep (WebP if conversion is on).
                already_square = (w == h)
                already_small_enough = (max(w, h) <= TARGET_SIZE)
                already_target_fmt = (
                    not CONVERT_TO_WEBP or path.suffix.lower() == ".webp"
                )
                if (
                    already_square and already_small_enough and already_target_fmt
                    and cached.get("optimized") is True
                ):
                    new_cache[name] = {"mtime": mtime, "optimized": True, "w": w, "h": h}
                    total_after += size_before
                    skipped += 1
                    continue

                out = square_crop(img.copy())

                # Decide final filename (extension may change)
                final_path = path
                if CONVERT_TO_WEBP and path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif"):
                    final_path = path.with_suffix(".webp")
                elif path.suffix.lower() == ".gif":
                    final_path = path.with_suffix(".png")

                size_after = save_optimized(out, final_path)

                # Delete the original if it was renamed
                if final_path != path and path.exists():
                    path.unlink()
                    rename_map[name] = final_path.name

                # Refresh mtime/cache for the (possibly renamed) file
                new_cache[final_path.name] = {
                    "mtime": final_path.stat().st_mtime,
                    "optimized": True,
                    "w": TARGET_SIZE,
                    "h": TARGET_SIZE,
                }
                total_after += size_after
                delta = size_before - size_after
                arrow = "→" if final_path == path else f"→ {final_path.name} →"
                print(f"  {name:48} {w}×{h} {arrow} {TARGET_SIZE}×{TARGET_SIZE}  "
                      f"({size_before/1024:.0f}KB → {size_after/1024:.0f}KB, "
                      f"{'-' if delta>=0 else '+'}{abs(delta)/1024:.0f}KB)")
                processed += 1
        except Exception as e:
            print(f"  SKIP {name}: {type(e).__name__}: {e}", file=sys.stderr)
            new_cache[name] = cached
            total_after += size_before

    save_cache(new_cache)

    # Sync overrides.yml references for any files we renamed
    if rename_map:
        n_changed = sync_overrides_image_refs(rename_map)
        print(f"\nSynced {n_changed} `image:` field(s) in overrides.yml")
    saved = total_before - total_after
    print()
    print(f"Processed: {processed}, skipped: {skipped}")
    print(f"Total: {total_before/1024/1024:.2f} MB → {total_after/1024/1024:.2f} MB "
          f"(saved {saved/1024/1024:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
