# The Independent PA — Technical Runbook

Visual-first Hugo newsroom for Palo Alto student coverage.

## Quick Start

```bash
cd independent-pa
hugo server -D
```

Local preview: http://localhost:1313/independent-pa/

## Core Commands

### 1) Run newsroom automation cycle

```bash
./scripts/newsroom_cycle.sh
```

What it does:
- checks RSS feeds (Palo Alto Weekly + Daily Post)
- auto-creates draft posts for major stories
- verifies Hugo build succeeds

### 2) Publish updates

```bash
./scripts/publish.sh "Publish: <headline>"
```

This commits + pushes to `main`. GitHub Actions deploys automatically.

## GitHub Setup (one-time)

Use username: `ar51141`

```bash
gh auth login
gh repo create independent-pa --public --source=. --remote=origin --push
```

If repo already exists:

```bash
git remote add origin https://github.com/ar51141/independent-pa.git
git push -u origin main
```

## GitHub Pages

In GitHub repo settings:
- Settings → Pages
- Build and deployment source: **GitHub Actions**

Workflow file already included:
- `.github/workflows/deploy.yml`

Live URL:
- https://ar51141.github.io/independent-pa/

## Content Model (auto-generated draft shape)

Each automated post includes:
- Hero image placeholder
- 3-slide quick summary
- Paly Student Impact section

## Brand System

Defined in `assets/css/extended/brand.css`

- Deep Green: `#1F4D3A`
- Slate: `#3E4A59`
- Gold: `#C9A227`

## Useful Files

- `hugo.toml` — site config and base URL
- `scripts/newsroom_hook.py` — RSS-to-draft automation
- `scripts/newsroom_cycle.sh` — one-shot automation cycle
- `scripts/publish.sh` — commit + push publish helper
- `content/posts/` — newsroom stories
