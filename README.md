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

---

## Local commit hook (pre-commit)

Auto-fixes formatting and lint before each commit (seconds only; tests stay in CI).
Prerequisite: uv and pre-commit (`uv tool install pre-commit` puts the shim in `~/.local/bin`).

```bash
uv tool install pre-commit
pre-commit install
```

> Restart the terminal (or reload the shell config) for PATH to take effect.

- Run over everything: `pre-commit run --all-files`
- Skip one commit: `git commit --no-verify`
- Definition: [.pre-commit-config.yaml](.pre-commit-config.yaml) (the same ruff config the read-only CI uses)
