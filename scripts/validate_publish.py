#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"

PLACEHOLDER_IMAGE = "/images/gohugo-default-sample-hero-image.jpg"


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = parts[1]
    out = {}

    # simple key: value parser for common scalar fields
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z0-9_]+):\s*(.*)$", line.strip())
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        out[k] = v.strip('"')

    out["raw"] = fm
    return out


def has_sources(fm_raw: str) -> bool:
    return ("source_url:" in fm_raw) or ("sources:" in fm_raw)


def is_draft(fm):
    return fm.get("draft", "true").lower() == "true"


def main():
    bad = []
    for md in sorted(POSTS.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm or is_draft(fm):
            continue

        errors = []
        fi = fm.get("featured_image", "")
        if (not fi) or fi == PLACEHOLDER_IMAGE:
            errors.append("featured_image must be set to a related non-placeholder image")

        credit = fm.get("image_credit", "")
        if (not credit) or ("placeholder" in credit.lower()):
            errors.append("image_credit must be set with a real credit")

        if not has_sources(fm.get("raw", "")):
            errors.append("must include source_url or sources list")

        if errors:
            bad.append((md.name, errors))

    if bad:
        print("Publish blocked. Fix these posts first:\n")
        for name, errs in bad:
            print(f"- {name}")
            for e in errs:
                print(f"  * {e}")
        return 1

    print("Publish validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
