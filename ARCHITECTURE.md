# Architecture

## Overview

Single-entry build pipeline that generates a self-contained HTML portfolio page from YAML project data, inline images, Mermaid diagrams, and Jinja2 templates.

```
build.py → src/pipeline.assemble() → src/diagrams.render_all()
                                    → src/data_tables.generate_all()
                                    → Jinja2 render → index.html
```

## Build Pipeline

`python build.py` triggers `src/pipeline.assemble()` which runs these steps in order:

1. **Load YAML** — `content/profile.yaml` (site metadata) + `content/projects.yaml` (6 projects with descriptions, tech stack, highlights)
2. **Inline images** — read screenshots from `images/{project_id}/`, encode as base64 data URIs, attach to project data
3. **Generate data tables** — `src/data_tables.py` reads CSV/JSON from sibling project directories (`AI-decision-maker`, `AI-schema-mapper`, `AI-tier-guardian`) and produces HTML comparison tables (Before vs After, quality reports, test results)
4. **Render diagrams** — `src/diagrams.py` calls Mermaid CLI (mmdc) to render 6 SVG flowcharts, post-processes fonts, returns SVG strings
5. **Assemble HTML** — Jinja2 renders templates (`templates/`) with all data inlined: CSS, JS, images, diagrams, tables → single self-contained `index.html`

## Directory Layout

```
build.py            Entry point. Calls src/pipeline.assemble().

config/             Build configuration.
  puppeteer.json      Chrome path for Mermaid CLI (mmdc).
  requirements.txt    Python dependencies.

content/            Source data.
  profile.yaml        Site title, description, GitHub link.
  projects.yaml       6 project entries with descriptions, tags, highlights.

images/             Screenshots, one subdirectory per project.
  collaborate/*.png
  rag-embed/*.png
  tool-calling/*.png

src/                Python modules.
  pipeline.py         Orchestrator: runs steps 1-5 above.
  diagrams.py         6 Mermaid diagram definitions + mmdc wrapper.
  data_tables.py      CSV/JSON readers + HTML table generators.

static/             Frontend source files (inlined into HTML at build time).
  style.css
  script.js

templates/          Jinja2 templates (flat, no subdirectories).
  base.html           HTML skeleton with KaTeX CDN.
  hero.html           Title + stat decoration.
  grid.html           Project card grid.
  project.html        Individual project detail section.

index.html          Build output. Self-contained, double-clickable.
```

## Diagram Semantics (Mermaid)

All 6 flowcharts share a consistent color scheme mapped to architecture layers:

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
