"""Editorial SVG diagrams for the portfolio."""

from collections.abc import Callable

from .projects import decision_maker, tier_guardian

Renderer = Callable[[], str]

DIAGRAMS: dict[str, Renderer] = {
    "decision-maker": decision_maker.render,
    "tier-guardian": tier_guardian.render,
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
