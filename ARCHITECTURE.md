# Architecture

## Overview

Single-entry build pipeline that generates a self-contained HTML portfolio page from YAML project data, inline images, Mermaid diagrams, and Jinja2 templates.

```
build.py assemble() → src/diagrams.render_all()
                    → src/data_tables.generate_all()
                    → Jinja2 render → index.html
```

## Build Pipeline

`uv run python build.py` runs `assemble()` in build.py, in this order:

1. **Load YAML** — `content/profile.yaml` (site metadata) + `content/projects.yaml` (8 projects with descriptions, tech stack, highlights)
2. **Inline images** — read screenshots from `images/{project_id}/`, encode as base64 data URIs, attach to project data
3. **Generate data tables** — `src/data_tables.py` reads CSV/JSON from sibling project directories (`AI-decision-maker`, `AI-schema-mapper`, `AI-tier-guardian`) and produces HTML comparison tables (Before vs After, quality reports, test results)
4. **Render diagrams** — `src/diagrams.py` calls Mermaid CLI (mmdc) to render 8 SVG flowcharts, post-processes fonts, returns SVG strings
5. **Assemble HTML** — Jinja2 renders templates (`templates/`) with all data inlined: CSS, JS, images, diagrams, tables → single self-contained `index.html`

## Directory Layout

```
build.py            Entry point. Defines and calls assemble().

config/             Build configuration.
  puppeteer.json      Chrome path for Mermaid CLI (mmdc).
  requirements.txt    Python dependencies.

content/            Source data.
  profile.yaml        Site title, description, GitHub link.
  projects.yaml       8 project entries with descriptions, tags, highlights.

images/             Screenshots, one subdirectory per project.
  collaborate/*.png
  rag-embed/*.png
  tool-calling/*.png
  tablesnap/*.png
  raw-to-guide/*.png

src/                Python modules.
  diagrams.py         8 Mermaid diagram definitions + mmdc wrapper.
  data_tables.py      CSV/JSON readers + HTML table generators.

static/             Frontend source files (inlined into HTML at build time).
  style.css           Design tokens (:root variables) + component styles.
  script.js           Typewriter, nav toggle, lightbox, scroll behaviors.

templates/          Jinja2 templates (flat, no subdirectories).
  base.html           HTML skeleton with KaTeX CDN + header (logo, hamburger).
  hero.html           Title + stat decoration.
  grid.html           Project card grid.
  project.html        Individual project detail section.

index.html          Build output. Self-contained, double-clickable.
```

## Design Tokens & Header

All colors, shadows, and motion curves are defined once in `:root` inside `static/style.css` — single source of truth. Change a token and every component that references it updates.

The header never lists project links inline. It shows the logo plus a hamburger button (`button.nav-toggle`, SVG lines with round caps). Opening it reveals a floating panel (`nav.header-nav`) centered below the header — the page stays visible and scrollable behind a light dim (`div.nav-backdrop`). Any scroll collapses the panel. This keeps the top bar clean regardless of project count.

## Diagram Semantics (Mermaid)

All 8 flowcharts share a consistent color scheme mapped to architecture layers:

| Class | Color | Layer |
|---|---|---|
| `input` | Warm cream | External Interface — data in/out, user input |
| `ai` | Purple | Reasoning / Agent / Knowledge Engine — LLM nodes |
| `proc` | Warm orange | Orchestration / Runtime — deterministic execution |
| `dec` | Amber | Router / Decision — zero-token branch points |
| `ok` | Green | Result / Cache Hit — success terminal |
| `stop` | Red | Block / Halt — rejection terminal |

Each diagram lives in its own function in `src/diagrams.py` and is rendered independently by `render_all()`.

## Data Flow

```
                   ┌──────────────────┐
                   │   content/*.yaml │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │  inline_images() │── images/{project_id}/*.png
                   └────────┬─────────┘
                            ↓
            ┌───────────────┼───────────────┐
            ↓               ↓               ↓
    ┌────────────┐  ┌──────────────┐  ┌──────────┐
    │data_tables │  │   diagrams   │  │static/*  │
    │.generate() │  │ .render_all()│  │.css/.js  │
    └──────┬─────┘  └──────┬───────┘  └─────┬────┘
           ↓               ↓                ↓
            ┌──────────────┼───────────────┐
            │    Jinja2: templates/*.html  │
            └──────────────┬───────────────┘
                           ↓
                    ┌──────────────┐
                    │  index.html  │
                    └──────────────┘
```
