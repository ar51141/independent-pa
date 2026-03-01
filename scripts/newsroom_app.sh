#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

while true; do
  echo ""
  echo "=== The Independent PA — Newsroom App ==="
  echo "1) Run newsroom cycle (RSS -> drafts -> Hugo build)"
  echo "2) Start local preview server"
  echo "3) Publish to GitHub Pages (commit + push)"
  echo "4) Push a post to WordPress as Pending"
  echo "5) List recent posts"
  echo "0) Exit"
  read -rp "Choose: " choice

  case "$choice" in
    1)
      ./scripts/newsroom_cycle.sh
      ;;
    2)
      hugo server -D
      ;;
    3)
      read -rp "Commit message: " msg
      ./scripts/publish.sh "$msg"
      ;;
    4)
      read -rp "Post path (e.g. content/posts/2026-03-01-the-600k-exit-a-paly-student-guide.md): " post
      python3 scripts/push_post_to_wordpress.py "$post"
      ;;
    5)
      ls -1t content/posts | head -n 10
      ;;
    0)
      exit 0
      ;;
    *)
      echo "Invalid option"
      ;;
  esac
done
