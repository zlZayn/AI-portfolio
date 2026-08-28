# AI Portfolio — Architecture

## Overview

`build.py` generates one self-contained portfolio page from YAML content, inline images, generated data tables, editorial SVG diagrams, CSS, JavaScript, and Jinja2 templates.

The build has no runtime diagram engine. Python renders deterministic SVG strings and Jinja2 embeds them directly in `index.html`.

## Build Pipeline

`uv run python build.py` performs six steps:

1. Load `content/profile.yaml` and the nine entries in `content/projects.yaml`.
2. Encode screenshots from `images/{project_id}/` as inline data URIs.
3. Generate comparison tables from versioned snapshots in `content/data-tables/`.
4. Render the nine accessible SVG diagrams through `src.diagrams.render_all()`.
5. Render the page sections with Jinja2 and inline CSS/JavaScript.
6. Normalize line endings and trailing whitespace, then write `index.html`.

## Directory Responsibilities

| Path | Responsibility |
| --- | --- |
| `build.py` | Single build entry point and source assembly |
| `content/` | Profile, traits, project copy, and versioned data-table snapshots |
| `images/` | Project screenshots |
| `src/data_tables.py` | Generated project comparison tables |
| `src/diagrams/` | Editorial SVG rendering package |
| `static/` | CSS and browser behavior inlined at build time |
| `templates/` | Jinja2 page structure |
| `tests/` | SVG primitive and project-story contract tests |
| `index.html` | Generated, self-contained site |

## Diagram Package

The public interface remains small:

```python
from src.diagrams import render_all

diagrams: dict[str, str] = render_all()
```

The package separates shared rules from project meaning:

| Module | Responsibility |
| --- | --- |
| `src/diagrams/__init__.py` | Project registry and `render_all()` contract |
| `src/diagrams/theme.py` | Portfolio-aligned semantic color tokens |
| `src/diagrams/svg.py` | Escaping, accessibility, paint order, nodes, zones, lanes, decisions, and orthogonal connectors |
| `src/diagrams/projects/*.py` | One hand-tuned layout per project |

Project modules describe content and geometry only. They do not define colors, markers, typography, or accessibility behavior.

## Visual Grammar

Diagram types follow `cathrynlavery/diagram-design` 2.4. Type selection reflects the dominant relationship, not visual variety.

| Type | Projects | Why |
| --- | --- | --- |
| Flowchart | `decision-maker`, `tier-guardian` | Cache and arbitration decisions create real branches |
| Architecture | `rag-embed`, `schema-mapper`, `tool-calling`, `collaborate`, `tablesnap`, `raw-to-guide`, `imagora` | Components, control planes, shared contracts, boundaries, and bypass paths carry the meaning |

Each diagram emphasizes one architectural claim:

- `decision-maker`: cache hits reuse semantic signals; misses request compact AI codes; code still validates, assembles, and executes every write.
- `rag-embed`: enhanced queries retrieve context while the original question reaches the answer model.
- `schema-mapper`: only unique values reach AI; full rows bypass AI and follow a local mapping, inference, polishing, validation, and reporting path.
- `tool-calling`: MCP and Function Calling share one tool registry and guarded runtime.
- `collaborate`: a validated dynamic plan controls variable-width parallel stages; bridges, failure isolation, synthesis, durable state, SSE recovery, and follow-up form one orchestration architecture.
- `tier-guardian`: two zero-token code gates own release, block, and review decisions.
- `tablesnap`: screen and file inputs share one local VLM call without an OCR reconstruction pipeline.
- `raw-to-guide`: one Schema contract governs both reference validation and generation; invalid AI-authored links loop back before maps, indexes, or the offline app are built.
- `imagora`: contract-formatted prompts import as batch cards; two frontends share one task pipeline; results are stored by content hash in the asset registry and rebound as canvas nodes for chained iteration.

## Rendering Rules

- Canvas geometry uses a 4 px grid and a fixed responsive `viewBox`.
- Non-axis-aligned relationships use rounded orthogonal paths; diagonal segments raise `ValueError`.
- Connector paths render before nodes so opaque node masks keep paths readable; connector labels render after nodes so cards cannot hide their text.
- Connector labels inherit their path semantics: orange for focus, green for success, red for danger, and dashed borders for optional or fallback paths.
- Orange is editorial focus, limited to one or two primary mechanisms per diagram.
- Human-readable names use the site sans-serif stack; technical tags use monospace.
- Standard labels remain readable at the 960 px mobile canvas; dense architectures can opt into the shared expanded typography mode and a project-specific minimum width.
- Every SVG has a project-prefixed `<title>`, `<desc>`, marker IDs, `role="img"`, and resolving `aria-labelledby`.
- XML text is escaped before insertion.
- Diagrams are static. No browser JavaScript, remote assets, or animation are required.

## Responsive Behavior

Diagrams scale to the project column on desktop. On narrow screens the container permits horizontal scrolling at a minimum readable width instead of shrinking labels below legibility. The SVG remains unframed so it reads as part of the project section rather than a nested card.

## Design Tokens

Page colors, shadows, and motion remain in `static/style.css`. Diagram colors use matching semantic tokens in `src/diagrams/theme.py` because SVG is generated before CSS is inlined.

When the portfolio palette changes, update both sources in the same change and run the visual checks. The current diagram roles are warm paper, white surface, deep ink, muted gray, orange focus, green success, and red block.

## Verification

Run automated contracts:

```bash
uv run python -m unittest discover -s tests -v
```

The tests verify:

- data-table snapshots produce all three showcase sections;
- repeated builds are byte-identical;
- all nine project IDs are registered;
- content-contract fields, domains, and trait coverage rules hold;
- required architectural phrases remain visible;
- SVG metadata and project-prefixed IDs are present;
- text escaping works;
- diagonal connectors are rejected;
- connector labels match validated path semantics and render above nodes;
- no Mermaid or `foreignObject` artifacts enter output.

Then rebuild and inspect desktop and mobile layouts:

```bash
uv run python build.py
```

## Dependencies

The Python dependency set is Jinja2 and PyYAML. Diagram generation uses only the Python standard library. It does not require Mermaid CLI, Node.js, Chrome, Puppeteer, or a network connection.

## Reproducible Data

The build never reads outside this repository. Small, curated outputs from `AI-decision-maker`, `AI-schema-mapper`, and `AI-tier-guardian` are versioned under `content/data-tables/`; generated HTML therefore remains identical in the main checkout, Git worktrees, and standalone clones. Refresh snapshots explicitly from their source projects, review the data diff, then rebuild `index.html` in the same commit.
