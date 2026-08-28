# AI Portfolio

<https://zlzayn.github.io/AI-portfolio/>

Static portfolio site generated from versioned project data, editorial SVG diagrams, and Jinja2 templates. The build is self-contained and does not read sibling repositories. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the build and diagram design rules.

Nine projects across seven domains — data processing, RAG retrieval, agent infrastructure, content safety, vision recognition, offline content generation, and AIGC creation — with shared traits (Prompt Engineering, Atomic Tool, converged upstream access, permission & security control) declared once at the portfolio level.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (dependency & env management)

## Build

```bash
uv run python build.py   # regenerates index.html
```

## Maintainers

- Rules and maintenance dashboard: [AGENTS.md](AGENTS.md)
