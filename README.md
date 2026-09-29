# AI Portfolio

[![CI](https://github.com/zlZayn/AI-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/zlZayn/AI-portfolio/actions/workflows/ci.yml)

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

---

## License

- Personal showcase site: no license terms are provided (no LICENSE file in this repository); text and imagery are authored by the maintainer.

## Contributing

- Personal project; questions and suggestions welcome via [Issues](https://github.com/zlZayn/AI-portfolio/issues).

Maintainer docs map → [AGENTS.md](AGENTS.md).
