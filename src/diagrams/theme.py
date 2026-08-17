"""Semantic design tokens shared by every portfolio diagram."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    paper: str = "#faf6ef"
    surface: str = "#ffffff"
    ink: str = "#2d2b55"
    muted: str = "#6c757d"
    soft: str = "#9ca3af"
    rule: str = "#d1d5db"
    rule_soft: str = "#e5e7eb"
    accent: str = "#f97316"
    accent_tint: str = "#fff7ed"
    success: str = "#2f7652"
    success_tint: str = "#f0f7f2"
    danger: str = "#a34444"
    danger_tint: str = "#fdf2f2"


THEME = Theme()
