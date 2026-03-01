#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 scripts/newsroom_hook.py
hugo

echo "Newsroom cycle complete: feeds checked, drafts generated, site builds clean."
