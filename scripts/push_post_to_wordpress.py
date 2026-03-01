#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP_CLI = ROOT.parent / "skills" / "wordpress" / "scripts" / "wp-cli.js"


def parse_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    title = path.stem.replace("-", " ").title()
    body = raw

    if raw.startswith("---"):
      parts = raw.split("---", 2)
      if len(parts) >= 3:
        fm = parts[1]
        body = parts[2].strip()
        m = re.search(r'^title:\s*"?(.*?)"?$', fm, flags=re.M)
        if m:
          title = m.group(1).strip()

    # Very lightweight markdown->html conversion for WP editor readability
    html = body
    html = re.sub(r"^###\s+(.*)$", r"<h3>\1</h3>", html, flags=re.M)
    html = re.sub(r"^##\s+(.*)$", r"<h2>\1</h2>", html, flags=re.M)
    html = re.sub(r"^#\s+(.*)$", r"<h1>\1</h1>", html, flags=re.M)
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\n\n", "</p><p>", html)
    html = f"<p>{html}</p>"

    return title, html


def main():
    if len(sys.argv) < 2:
        print("Usage: ./scripts/push_post_to_wordpress.py content/posts/<file>.md")
        return 1

    md = Path(sys.argv[1])
    if not md.is_absolute():
        md = ROOT / md
    if not md.exists():
        print(f"File not found: {md}")
        return 1

    title, html = parse_md(md)
    payload = {
        "title": title,
        "content": html,
        "status": "pending"
    }

    tmp = ROOT / "data" / "wp_payload.json"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    cmd = ["node", str(WP_CLI), "posts:create", f"@{tmp}"]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Done: created pending WordPress post.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
