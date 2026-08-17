"""Editorial SVG diagrams for the portfolio."""

from collections.abc import Callable

from .projects import (
    collaborate,
    decision_maker,
    rag_embed,
    raw_to_guide,
    schema_mapper,
    tablesnap,
    tier_guardian,
    tool_calling,
)

Renderer = Callable[[], str]

DIAGRAMS: dict[str, Renderer] = {
    "decision-maker": decision_maker.render,
    "rag-embed": rag_embed.render,
    "schema-mapper": schema_mapper.render,
    "tool-calling": tool_calling.render,
    "collaborate": collaborate.render,
    "tier-guardian": tier_guardian.render,
    "tablesnap": tablesnap.render,
    "raw-to-guide": raw_to_guide.render,
}


def render_all() -> dict[str, str]:
    """Render every registered project diagram."""
    result: dict[str, str] = {}
    for project_id, renderer in DIAGRAMS.items():
        svg = renderer()
        result[project_id] = svg
        print(f"  [{project_id}] diagram rendered ({len(svg)} bytes)")
    return result


__all__ = ["render_all"]
