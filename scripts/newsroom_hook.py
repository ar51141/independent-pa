#!/usr/bin/env python3
import os
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
STATE_PATH = ROOT / "data" / "hook_state.json"

SOURCES = [
    {"name": "Palo Alto Weekly", "feed": "https://paloaltoonline.com/feed/"},
    {"name": "Palo Alto Daily Post", "feed": "https://padailypost.com/feed/"},
]

MAJOR_KEYWORDS = {
    "superintendent", "pausd", "board", "budget", "school", "student",
    "safety", "police", "tunnel", "crossing", "phone", "law", "act",
    "closure", "strike", "election", "district"
}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"seen": {}}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def parse_rss(xml_data: bytes):
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    items = []
    if channel is None:
        return items
    for item in channel.findall("item")[:12]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link or title).strip()
        pub = (item.findtext("pubDate") or "").strip()
        items.append({"title": title, "link": link, "id": guid, "published": pub})
    return items


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:72]


def is_major(title: str) -> bool:
    words = set(re.findall(r"[a-zA-Z]+", title.lower()))
    return len(words & MAJOR_KEYWORDS) > 0


def write_post(source: str, item: dict):
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(item["title"])
    filename = POSTS_DIR / f"{date}-{slug}.md"
    if filename.exists():
        return filename

    safe_title = item['title'].replace('"', "'")
    content = f'''---
title: "{safe_title}"
short_title: "{safe_title[:56]}"
deck: "Quick, student-readable summary of a new Palo Alto development."
date: {datetime.now(timezone.utc).isoformat()}
draft: true
author: "The Independent PA Newsroom"
categories: ["civic"]
tags: ["visual-first", "palo-alto", "paly"]
featured_image: "/images/gohugo-default-sample-hero-image.jpg"
hero_image: "/images/gohugo-default-sample-hero-image.jpg"
source_name: "{source}"
source_url: "{item['link']}"
layout: "single"
---

## What happened

A major civic update was reported by **{source}**.

## Quick overview

- Here is the core update in simple terms.
- Here is what we can confirm right now.
- Here is what to watch next.

## Paly Student Impact

- Why this matters to students now.
- What changes students should expect or track.

## Sources

- {item['link']}
'''
    filename.write_text(content)
    return filename


def main():
    state = load_state()
    created = []

    for src in SOURCES:
        seen = set(state["seen"].get(src["feed"], []))
        try:
            items = parse_rss(fetch(src["feed"]))
        except Exception as e:
            print(f"WARN {src['name']}: {e}")
            continue

        for item in items:
            item_id = item["id"]
            if item_id in seen:
                continue
            if is_major(item["title"]):
                path = write_post(src["name"], item)
                created.append(str(path))
            seen.add(item_id)

        state["seen"][src["feed"]] = list(seen)[-2000:]

    save_state(state)

    if created:
        print("Created drafts:")
        for p in created:
            print(f"- {p}")
    else:
        print("No new major stories.")


if __name__ == "__main__":
    main()
