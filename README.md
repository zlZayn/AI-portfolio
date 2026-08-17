# AI Portfolio

<https://zlzayn.github.io/AI-portfolio/>

Static portfolio site generated from versioned project data, editorial SVG diagrams, and Jinja2 templates. The build is self-contained and does not read sibling repositories. See [ARCHITECTURE.md](ARCHITECTURE.md) for the build and diagram design rules.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (dependency & env management)

## Build

```bash
uv run python build.py   # regenerates index.html
```
