#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${1:-}" ]]; then
  echo "Usage: ./scripts/publish.sh \"Commit message\""
  exit 1
fi

msg="$1"

python3 scripts/validate_publish.py

git add .
git commit -m "$msg"
git push origin main

echo "Published: pushed to main (GitHub Action will deploy)."
