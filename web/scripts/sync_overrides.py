"""Sync overrides.yml against scholar_cache.json.

For every paper in Google Scholar, ensure an entry exists in overrides.yml so
the user can edit any paper's metadata in one place. Existing entries are
preserved verbatim; only missing entries are appended.

New entries get:
  - tags / methods / platforms : auto-classified from title
  - scholar_ids : from GS
  - hide: true  : if the paper predates RECENT_YEAR_CUTOFF (so it doesn't
                  suddenly appear on the public site). User flips to false
                  to surface it.

Safe to re-run. Idempotent.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import yaml

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent  # web/
OVERRIDES = ROOT / "src" / "data" / "overrides.yml"
SCHOLAR_CACHE = ROOT / "src" / "data" / "scholar_cache.json"
REPORT = ROOT / "scripts" / "sync_report.md"

RECENT_YEAR_CUTOFF = 2024

# ── Taxonomy (kept in sync with src/lib/tag-colors.ts) ───────────────────────
TOPICS = {
    "online-harm", "news-journalism", "user-behavior", "beliefs-opinions",
    "llms-responsible-ai", "bias-fairness", "networks-influence", "digital-health",
}

TITLE_RULES: list[tuple[re.Pattern, str]] = [
    # Health-first so COVID/mental-health framings route here.
    (re.compile(r"\b(mental health|depress|anxiet|suicid|psychiatr|psychological|wellbe|COVID-?19|public health|vaccin)", re.I),
                                                                                    "digital-health"),
    (re.compile(r"\b(toxic|toxicity|harass|hate|abuse|trolling|cyberbull)", re.I), "online-harm"),
    (re.compile(r"\bmoderat", re.I),                                                "online-harm"),
    (re.compile(r"\b(news|journalis|misinform|disinform|fake news|factualit|propaganda)", re.I),
                                                                                    "news-journalism"),
    (re.compile(r"\b(bias|biased|fair|fairness|stereo|stereotype|diversity|gender|racial|race|representation|disparit|equity)", re.I),
                                                                                    "bias-fairness"),
    (re.compile(r"\b(LLM|ChatGPT|GPT[- ]?\d|FlanT5|DeepSeek|language model|LLMs|alignment|prompt|jailbreak|hallucinat|safety)", re.I),
                                                                                    "llms-responsible-ai"),
    (re.compile(r"\b(annotator|annotation|judge|simulation|simulat|benchmark)", re.I),
                                                                                    "llms-responsible-ai"),
    (re.compile(r"\b(belief|opinion|polariz|stance|ideolog|moral|persuas)", re.I),  "beliefs-opinions"),
    (re.compile(r"\b(network|graph|diffus|centrality|topology|influencer|cascade|propagation)", re.I),
                                                                                    "networks-influence"),
    (re.compile(r"\b(engagement|attention|retention|click|view|recommend|game|esport|player|gaming|gamer)", re.I),
                                                                                    "user-behavior"),
]

METHOD_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(LLM|LLMs|ChatGPT|GPT[- ]?\d|GPT-?[345]|FlanT5|DeepSeek|large language model|generative AI)", re.I), "llm"),
    (re.compile(r"\b(embedding|word2vec|BERT|transformer|tokeniz|sentiment|lexicon|topic model|stance detection|NLP|natural language)", re.I), "nlp"),
    (re.compile(r"\b(network|graph|topology|centrality|community detection|diffus|cascade|propagation|homophily|tie strength)", re.I), "networks"),
    (re.compile(r"\b(crowdsourc|mechanical turk|MTurk|AMT|annotat)", re.I), "crowdsourced"),
    (re.compile(r"\b(survey|focus group|user study|controlled experiment|A/B test|interview|qualitative|eye-tracking|eye tracking|case study|empirical study)", re.I), "user-study"),
    (re.compile(r"\b(dataset|corpus|benchmark|collection)", re.I), "dataset"),
]

PLATFORM_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(Twitter|tweet|hashtag|retweet|#\w+)", re.I), "twitter"),
    (re.compile(r"\b(Reddit|subreddit|r/\w+)", re.I),             "reddit"),
    (re.compile(r"\bYouTube", re.I),                              "youtube"),
    (re.compile(r"\bFacebook", re.I),                             "facebook"),
    (re.compile(r"\bInstagram", re.I),                            "instagram"),
    (re.compile(r"\bTikTok", re.I),                               "tiktok"),
    (re.compile(r"\bGab\b"),                                      "gab"),
]

HIDE_PATTERNS: list[re.Pattern] = [
    re.compile(r"^Reports of the Workshops", re.I),
    re.compile(r"^Proceedings of the .* (Conference|Workshop|Meeting)", re.I),
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def normalize_title(t: str) -> str:
    if not t: return ""
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def slugify(t: str) -> str:
    return normalize_title(t).replace(" ", "-")[:80]


def classify_topic(title: str) -> str:
    for pat, topic in TITLE_RULES:
        if pat.search(title or ""):
            return topic
    return "user-behavior"


def extract_methods(text: str) -> list[str]:
    found: list[str] = []
    for pat, m in METHOD_RULES:
        if pat.search(text) and m not in found:
            found.append(m)
    return found


def extract_platforms(text: str) -> list[str]:
    found: list[str] = []
    for pat, p in PLATFORM_RULES:
        if pat.search(text) and p not in found:
            found.append(p)
    if len(found) >= 2 and "multi-platform" not in found:
        found.append("multi-platform")
    if not found and re.search(r"\b(news media|news organization|news outlet)", text, re.I):
        found.append("news-media")
    return found


def should_hide_title(title: str) -> bool:
    return any(p.search(title or "") for p in HIDE_PATTERNS)


def parse_year(year_str, venue_str) -> int | None:
    if year_str:
        try: return int(year_str)
        except ValueError: pass
    if venue_str:
        m = re.search(r"\b(19|20)\d{2}\b", venue_str)
        if m: return int(m.group(0))
    return None


def is_shadow_entry(p: dict) -> bool:
    """Detect 'shadow' entries that GS returns through its scraping API but
    doesn't show on the author's profile UI. These are usually auto-merged,
    hidden by the author, or stub entries with no real publication record.

    Signature: no year, no citations, no venue. Real papers have at least
    one of those even when the others are missing.
    """
    year = parse_year(p.get("year"), p.get("venue"))
    citations = p.get("citations") or 0
    venue = (p.get("venue") or "").strip()
    return year is None and citations == 0 and not venue


def dedupe_scholar(cache: dict) -> list[dict]:
    """Combine both authors' publications; dedupe by fuzzy title.
    Shadow entries (see is_shadow_entry) are dropped before deduping."""
    all_pubs = []
    n_shadow = 0
    for info in cache.values():
        if not isinstance(info, dict) or "publications" not in info:
            continue
        for p in info["publications"]:
            if is_shadow_entry(p):
                n_shadow += 1
                continue
            all_pubs.append(p)
    if n_shadow:
        print(f"  ⚠ skipped {n_shadow} shadow entries (no year + no citations + no venue)")

    deduped: list[dict] = []
    seen_norm: list[tuple[str, int]] = []

    for p in all_pubs:
        title = p.get("title") or ""
        nt = normalize_title(title)
        if not nt:
            continue
        match_idx = None
        for ex_norm, idx in seen_norm:
            if SequenceMatcher(None, nt, ex_norm).ratio() >= 0.92:
                match_idx = idx; break
        if match_idx is not None:
            existing = deduped[match_idx]
            if p.get("scholar_id") and p["scholar_id"] not in existing["scholar_ids"]:
                existing["scholar_ids"].append(p["scholar_id"])
            existing["citations"] = max(existing["citations"], p.get("citations", 0))
        else:
            deduped.append({
                "title": title,
                "year": parse_year(p.get("year"), p.get("venue")),
                "venue": p.get("venue"),
                "citations": p.get("citations", 0),
                "scholar_ids": [p["scholar_id"]] if p.get("scholar_id") else [],
            })
            seen_norm.append((nt, len(deduped) - 1))

    return deduped


# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    if not OVERRIDES.exists():
        print(f"ERROR: {OVERRIDES} not found", file=sys.stderr); return 1
    if not SCHOLAR_CACHE.exists():
        print(f"ERROR: {SCHOLAR_CACHE} not found. Run fetch_citations.py first.", file=sys.stderr)
        return 1

    overrides = yaml.safe_load(OVERRIDES.read_text()) or {}
    cache = json.loads(SCHOLAR_CACHE.read_text())
    gs_pubs = dedupe_scholar(cache)
    print(f"Loaded overrides: {len(overrides)} entries; GS deduped: {len(gs_pubs)} pubs")

    # Build a normalized-title → slug index of existing overrides for fast match
    existing_index: dict[str, str] = {}
    # Plus a scholar_id → slug index so we can match arXiv-v2-renamed or
    # otherwise drifted titles whenever the override already carries the GS id.
    sid_index: dict[str, str] = {}
    for slug, entry in overrides.items():
        nt = normalize_title(entry.get("title") or "")
        if nt:
            existing_index[nt] = slug
        for sid in (entry.get("scholar_ids") or []):
            sid_index[sid] = slug

    added: list[tuple[str, str, int | None, bool]] = []
    updated_scholar_ids = 0

    for gs in gs_pubs:
        nt = normalize_title(gs["title"])

        # 1. scholar_id match — survives title renames (e.g. arXiv v2)
        match_slug = None
        for sid in gs["scholar_ids"]:
            if sid in sid_index:
                match_slug = sid_index[sid]; break
        # 2. Exact normalized title match
        if not match_slug:
            match_slug = existing_index.get(nt)
        # 3. Fuzzy title fallback
        if not match_slug:
            for ex_nt, ex_slug in existing_index.items():
                if SequenceMatcher(None, nt, ex_nt).ratio() >= 0.92:
                    match_slug = ex_slug; break

        if match_slug:
            # Existing entry — top up scholar_ids if missing any
            entry = overrides[match_slug]
            sids = entry.get("scholar_ids") or []
            changed = False
            for sid in gs["scholar_ids"]:
                if sid not in sids:
                    sids.append(sid); changed = True
            if changed:
                entry["scholar_ids"] = sids
                updated_scholar_ids += 1
            continue

        # ── New entry ────────────────────────────────────────────────────
        base_slug = slugify(gs["title"])
        slug = base_slug
        suffix = 2
        while slug in overrides:
            slug = f"{base_slug}-{suffix}"; suffix += 1

        topic = classify_topic(gs["title"])
        methods = extract_methods(gs["title"])
        platforms = extract_platforms(gs["title"])
        hide = should_hide_title(gs["title"]) or (gs["year"] is not None and gs["year"] < RECENT_YEAR_CUTOFF)

        new_entry: dict = {
            "title": gs["title"],
            "tags": [topic],
        }
        if methods: new_entry["methods"] = methods
        if platforms: new_entry["platforms"] = platforms
        if hide: new_entry["hide"] = True
        new_entry["scholar_ids"] = list(gs["scholar_ids"])

        overrides[slug] = new_entry
        existing_index[nt] = slug
        added.append((slug, gs["title"], gs["year"], hide))

    # Write back
    OVERRIDES.write_text(
        yaml.dump(overrides, sort_keys=False, allow_unicode=True, width=200)
    )

    # Report
    lines = [
        "# overrides.yml sync report\n",
        f"- Total entries: **{len(overrides)}**",
        f"- New entries added: **{len(added)}**",
        f"- Existing entries with updated scholar_ids: **{updated_scholar_ids}**\n",
    ]
    visible = [a for a in added if not a[3]]
    hidden = [a for a in added if a[3]]
    if visible:
        lines.append(f"## New & visible ({len(visible)})\n")
        for slug, title, year, _ in sorted(visible, key=lambda x: -(x[2] or 0)):
            lines.append(f"- ({year}) `{slug}`")
            lines.append(f"  - *{title}*")
    if hidden:
        lines.append(f"\n## New but hidden ({len(hidden)}, set `hide: false` to show)\n")
        for slug, title, year, _ in sorted(hidden, key=lambda x: -(x[2] or 0))[:40]:
            lines.append(f"- ({year}) `{slug}`")
            lines.append(f"  - *{title}*")
        if len(hidden) > 40:
            lines.append(f"\n_…and {len(hidden) - 40} more_")
    REPORT.write_text("\n".join(lines))

    print(f"\n✓ Wrote {OVERRIDES.relative_to(ROOT.parent)}")
    print(f"✓ Wrote {REPORT.relative_to(ROOT.parent)}")
    print(f"\nSummary:")
    print(f"  Total entries: {len(overrides)}")
    print(f"  New & visible (2024+):  {len(visible)}")
    print(f"  New but hidden:         {len(hidden)}")
    print(f"  Existing entries updated (scholar_ids): {updated_scholar_ids}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
