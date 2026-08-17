"""Small, deterministic SVG primitives for editorial architecture diagrams."""

from __future__ import annotations

from html import escape
from math import ceil
from typing import Literal, Sequence

from .theme import THEME, Theme

Point = tuple[int, int]
TextLines = str | Sequence[str]
ConnectorStyle = Literal["default", "accent", "success", "danger", "dashed"]
TypographyMode = Literal["standard", "expanded"]

_SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans SC',sans-serif"
_MONO = "'SFMono-Regular',Consolas,'Liberation Mono','Noto Sans Mono CJK SC',monospace"
_MARKER_STYLE_BY_CONNECTOR: dict[ConnectorStyle, str] = {
    "default": "default",
    "accent": "accent",
    "success": "success",
    "danger": "danger",
    "dashed": "default",
}
_TYPOGRAPHY_MODES: frozenset[str] = frozenset({"standard", "expanded"})


class Canvas:
    """Collect SVG elements in a fixed paint order and render one accessible figure."""

    def __init__(
        self,
        slug: str,
        title: str,
        description: str,
        width: int = 960,
        height: int = 520,
        theme: Theme = THEME,
        typography: TypographyMode = "standard",
    ) -> None:
        if typography not in _TYPOGRAPHY_MODES:
            raise ValueError(f"Unsupported typography mode: {typography}")
        self.slug = slug
        self.title = title
        self.description = description
        self.width = width
        self.height = height
        self.theme = theme
        self.typography = typography
        self._layers: dict[str, list[str]] = {
            "zones": [],
            "connectors": [],
            "nodes": [],
            "annotations": [],
        }
        self._check_grid(width, height)

    def zone(self, x: int, y: int, width: int, height: int, label: str) -> None:
        self._check_grid(x, y, width, height)
        label_width = max(56, _grid_ceil(len(label) * 7 + 24))
        safe_label = escape(label.upper())
        self._layers["zones"].append(
            f'<g class="zone"><rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="8"/><rect class="zone-label-mask" x="{x + 16}" y="{y - 4}" '
            f'width="{label_width}" height="16" rx="4"/><text class="zone-label" '
            f'x="{x + 24}" y="{y + 8}">{safe_label}</text></g>'
        )

    def lane(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: TextLines,
        tinted: bool = False,
    ) -> None:
        self._check_grid(x, y, width, height)
        tint_class = " lane-tinted" if tinted else ""
        self._layers["zones"].append(
            f'<g class="lane{tint_class}"><rect x="{x}" y="{y}" width="{width}" height="{height}"/>'
            f'<line x1="{x + 128}" y1="{y}" x2="{x + 128}" y2="{y + height}"/>'
            f'{self._multiline_text(x + 64, y + height // 2 + 4, label, "lane-label", 12)}</g>'
        )

    def node(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: TextLines,
        subtitle: TextLines = "",
        tag: str = "",
        kind: str = "default",
    ) -> None:
        self._check_grid(x, y, width, height)
        classes = f"node node-{escape(kind)}"
        parts = [
            f'<g class="{classes}">',
            f'<rect class="node-mask" x="{x}" y="{y}" width="{width}" height="{height}" rx="8"/>',
            f'<rect class="node-box" x="{x}" y="{y}" width="{width}" height="{height}" rx="8"/>',
        ]
        if tag:
            tag_width = max(32, _grid_ceil(len(tag) * 7 + 16))
            parts.extend(
                (
                    f'<rect class="node-tag-box" x="{x + 12}" y="{y + 8}" width="{tag_width}" '
                    f'height="16" rx="4"/>',
                    f'<text class="node-tag" x="{x + 12 + tag_width / 2:g}" y="{y + 20}" '
                    f'text-anchor="middle">{escape(tag.upper())}</text>',
                )
            )
        if tag:
            if _line_count(title) > 1:
                title_y = y + (48 if self.typography == "expanded" else 44)
            else:
                title_y = y + 40
        else:
            title_y = y + 28
        parts.append(self._multiline_text(x + width // 2, title_y, title, "node-title", 16))
        if subtitle:
            expanded_spacing = 4 * (_line_count(title) - 1) if self.typography == "expanded" else 0
            sub_y = title_y + 20 + expanded_spacing
            parts.append(self._multiline_text(x + width // 2, sub_y, subtitle, "node-subtitle", 12))
        parts.append("</g>")
        self._layers["nodes"].append("".join(parts))

    def decision(
        self,
        cx: int,
        cy: int,
        width: int,
        height: int,
        title: TextLines,
        subtitle: str = "",
        focal: bool = False,
    ) -> None:
        self._check_grid(cx, cy, width, height)
        points = f"{cx},{cy - height // 2} {cx + width // 2},{cy} {cx},{cy + height // 2} {cx - width // 2},{cy}"
        kind = " decision-focal" if focal else ""
        parts = [
            f'<g class="decision{kind}">',
            f'<polygon class="decision-mask" points="{points}"/>',
            f'<polygon class="decision-box" points="{points}"/>',
            self._multiline_text(cx, cy - (4 if subtitle else 0), title, "decision-title", 16),
        ]
        if subtitle:
            parts.append(f'<text class="decision-subtitle" x="{cx}" y="{cy + 24}" text-anchor="middle">{escape(subtitle)}</text>')
        parts.append("</g>")
        self._layers["nodes"].append("".join(parts))

    def connector(
        self,
        points: tuple[Point, ...],
        label: str = "",
        style: ConnectorStyle = "default",
        label_at: Point | None = None,
    ) -> None:
        if style not in _MARKER_STYLE_BY_CONNECTOR:
            raise ValueError(f"Unsupported connector style: {style}")
        if len(points) < 2:
            raise ValueError("A connector needs at least two points")
        for point in points:
            self._check_grid(*point)
        for start, end in zip(points, points[1:]):
            if start[0] != end[0] and start[1] != end[1]:
                raise ValueError(f"Connector segment is diagonal: {start} -> {end}")
        path = _rounded_path(points)
        marker = f"url(#{self.slug}-arrow-{_marker_style(style)})"
        self._layers["connectors"].append(
            f'<path class="connector connector-{escape(style)}" d="{path}" marker-end="{marker}"/>'
        )
        if label:
            x, y = label_at or _label_position(points)
            self._check_grid(x, y)
            mask_width = max(40, _grid_ceil(len(label) * 7 + 16))
            self._layers["annotations"].append(
                f'<g class="connector-label connector-label-{style}">'
                f'<rect x="{x - mask_width // 2}" y="{y - 16}" '
                f'width="{mask_width}" height="16" rx="4"/><text x="{x}" y="{y - 4}" '
                f'text-anchor="middle">{escape(label.upper())}</text></g>'
            )

    def annotation(self, x: int, y: int, text: str, width: int = 200) -> None:
        self._check_grid(x, y, width)
        self._layers["annotations"].append(
            f'<g class="annotation"><line x1="{x}" y1="{y}" x2="{x + 24}" y2="{y}"/>'
            f'<text x="{x + 36}" y="{y + 4}">{escape(text)}</text></g>'
        )

    def label(self, x: int, y: int, text: str, kind: str = "eyebrow", anchor: str = "start") -> None:
        self._check_grid(x, y)
        self._layers["annotations"].append(
            f'<text class="label label-{escape(kind)}" x="{x}" y="{y}" '
            f'text-anchor="{escape(anchor)}">{escape(text)}</text>'
        )

    def step_header(self, x: int, y: int, number: str, label: str, focal: bool = False) -> None:
        self._check_grid(x, y)
        focal_class = " step-focal" if focal else ""
        self._layers["annotations"].append(
            f'<g class="step-header{focal_class}"><rect x="{x - 16}" y="{y}" width="32" height="16" rx="8"/>'
            f'<text class="step-number" x="{x}" y="{y + 12}" text-anchor="middle">{escape(number)}</text>'
            f'<text class="step-label" x="{x}" y="{y + 32}" text-anchor="middle">{escape(label.upper())}</text></g>'
        )

    def render(self) -> str:
        title = escape(self.title)
        description = escape(self.description)
        body = "".join(
            element
            for name in ("zones", "connectors", "nodes", "annotations")
            for element in self._layers[name]
        )
        return (
            f'<svg class="editorial-diagram editorial-diagram-{self.slug} '
            f'diagram-typography-{self.typography}" xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}" width="100%" role="img" '
            f'aria-labelledby="{self.slug}-title {self.slug}-desc" preserveAspectRatio="xMidYMid meet">'
            f'<title id="{self.slug}-title">{title}</title>'
            f'<desc id="{self.slug}-desc">{description}</desc>'
            f'{self._defs()}{self._styles()}'
            f'<rect width="{self.width}" height="{self.height}" fill="{self.theme.paper}"/>'
            f'{body}</svg>'
        )

    def _defs(self) -> str:
        return (
            "<defs>"
            + self._marker("default", self.theme.muted)
            + self._marker("accent", self.theme.accent_strong)
            + self._marker("success", self.theme.success)
            + self._marker("danger", self.theme.danger)
            + "</defs>"
        )

    def _marker(self, name: str, color: str) -> str:
        return (
            f'<marker id="{self.slug}-arrow-{name}" markerWidth="8" markerHeight="8" '
            f'refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{color}"/></marker>'
        )

    def _styles(self) -> str:
        t = self.theme
        return f"""<style>
.editorial-diagram text{{font-family:{_SANS};fill:{t.ink};letter-spacing:0}}
.zone>rect:first-child{{fill:{t.ink};fill-opacity:.018;stroke:{t.rule};stroke-width:1}}
.zone-label-mask,.connector-label rect{{fill:{t.paper}}}
.zone-label,.node-tag,.connector-label text,.label-eyebrow{{font-family:{_MONO};font-size:11px;font-weight:600;letter-spacing:.08em;fill:{t.muted}}}
.lane rect{{fill:{t.paper};stroke:{t.rule_soft};stroke-width:1}}.lane-tinted rect{{fill:{t.ink};fill-opacity:.018}}
.lane line{{stroke:{t.rule};stroke-width:1}}.lane-label{{font-family:{_MONO};font-size:11px;font-weight:600;fill:{t.muted};letter-spacing:.06em}}
.connector{{fill:none;stroke:{t.muted};stroke-width:1.5}}
.connector-accent{{stroke:{t.accent_strong};stroke-width:2}}
.connector-success{{stroke:{t.success}}}.connector-danger{{stroke:{t.danger}}}
.connector-dashed{{stroke-dasharray:6 4}}
.node-mask,.decision-mask{{fill:{t.paper};stroke:none}}
.node-box{{fill:{t.surface};stroke:{t.ink};stroke-width:1.25}}
.node-muted .node-box{{fill:{t.paper};stroke:{t.rule}}}
.node-store .node-box{{fill:{t.ink};fill-opacity:.045;stroke:{t.muted}}}
.node-optional .node-box{{fill:{t.paper};stroke:{t.rule};stroke-dasharray:6 4}}
.node-focal .node-box{{fill:{t.accent_tint};stroke:{t.accent_strong};stroke-width:2}}
.node-success .node-box{{fill:{t.success_tint};stroke:{t.success}}}
.node-danger .node-box{{fill:{t.danger_tint};stroke:{t.danger}}}
.node-tag-box{{fill:none;stroke:{t.muted};stroke-opacity:.5}}
.node-focal .node-tag-box{{stroke:{t.accent_strong}}}.node-focal .node-tag{{fill:{t.accent_strong}}}
.node-title,.decision-title{{font-size:13px;font-weight:650}}
.node-subtitle,.decision-subtitle{{font-family:{_MONO};font-size:10px;fill:{t.muted}}}
.decision-box{{fill:{t.surface};stroke:{t.ink};stroke-width:1.25}}
.decision-focal .decision-box{{fill:{t.accent_tint};stroke:{t.accent_strong};stroke-width:2}}
.connector-label rect{{stroke:{t.rule_soft};stroke-width:.5}}
.connector-label-accent rect{{stroke:{t.accent_strong};stroke-opacity:.45}}.connector-label-accent text{{fill:{t.accent_strong}}}
.connector-label-success rect{{stroke:{t.success};stroke-opacity:.45}}.connector-label-success text{{fill:{t.success}}}
.connector-label-danger rect{{stroke:{t.danger};stroke-opacity:.45}}.connector-label-danger text{{fill:{t.danger}}}
.connector-label-dashed rect{{stroke:{t.muted};stroke-dasharray:3 2}}.connector-label-dashed text{{fill:{t.muted}}}
.annotation line{{stroke:{t.accent_strong};stroke-width:2}}.annotation text{{font-size:12px;font-style:italic}}
.label-metric{{font-family:{_MONO};font-size:12px;font-weight:600;fill:{t.accent_strong}}}
.step-header rect{{fill:{t.ink};fill-opacity:.1}}.step-header text{{font-family:{_MONO};font-size:11px;font-weight:600;fill:{t.muted}}}
.step-header .step-label{{letter-spacing:.06em}}.step-focal rect{{fill:{t.accent};fill-opacity:.16}}.step-focal text{{fill:{t.accent_strong}}}
.diagram-typography-expanded .zone-label,.diagram-typography-expanded .node-tag,.diagram-typography-expanded .connector-label text,.diagram-typography-expanded .label-eyebrow{{font-size:12px}}
.diagram-typography-expanded .node-title,.diagram-typography-expanded .decision-title{{font-size:14px}}
.diagram-typography-expanded .node-subtitle,.diagram-typography-expanded .decision-subtitle{{font-size:10px}}
.diagram-typography-expanded .annotation text{{font-size:13px}}
</style>"""

    @staticmethod
    def _check_grid(*values: int) -> None:
        for value in values:
            if value % 4:
                raise ValueError(f"Value {value} is outside the 4 px grid")

    @staticmethod
    def _multiline_text(x: int, y: int, lines: TextLines, css_class: str, gap: int) -> str:
        values = (lines,) if isinstance(lines, str) else tuple(lines)
        if not values:
            return ""
        start_y = y - ((len(values) - 1) * gap // 2)
        tspans = "".join(
            f'<tspan x="{x}" y="{start_y + index * gap}">{escape(line)}</tspan>'
            for index, line in enumerate(values)
        )
        return f'<text class="{css_class}" text-anchor="middle">{tspans}</text>'


def _grid_ceil(value: int) -> int:
    return int(ceil(value / 4) * 4)


def _line_count(lines: TextLines) -> int:
    return 1 if isinstance(lines, str) else len(lines)


def _marker_style(style: ConnectorStyle) -> str:
    return _MARKER_STYLE_BY_CONNECTOR[style]


def _label_position(points: Sequence[Point]) -> Point:
    segments = list(zip(points, points[1:]))
    start, end = max(segments, key=lambda pair: abs(pair[1][0] - pair[0][0]) + abs(pair[1][1] - pair[0][1]))
    return _grid_ceil((start[0] + end[0]) // 2), _grid_ceil((start[1] + end[1]) // 2)


def _rounded_path(points: Sequence[Point], radius: int = 8) -> str:
    commands = [f"M {points[0][0]} {points[0][1]}"]
    for index in range(1, len(points) - 1):
        previous, corner, following = points[index - 1], points[index], points[index + 1]
        before = _toward(corner, previous, min(radius, _distance(previous, corner) // 2))
        after = _toward(corner, following, min(radius, _distance(corner, following) // 2))
        commands.extend((f"L {before[0]} {before[1]}", f"Q {corner[0]} {corner[1]} {after[0]} {after[1]}"))
    commands.append(f"L {points[-1][0]} {points[-1][1]}")
    return " ".join(commands)


def _distance(start: Point, end: Point) -> int:
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def _toward(start: Point, target: Point, distance: int) -> Point:
    if start[0] == target[0]:
        direction = 1 if target[1] > start[1] else -1
        return start[0], start[1] + direction * distance
    direction = 1 if target[0] > start[0] else -1
    return start[0] + direction * distance, start[1]
