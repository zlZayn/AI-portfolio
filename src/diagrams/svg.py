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
        fit: bool = False,
    ) -> None:
        # 健壮性：fit=True 时按标题/副标题/角标内容自适应宽高，文字天然不超框。
        if fit:
            width, height = self._fit_node_size(width, height, title, subtitle, tag)
        self._check_grid(x, y, width, height)
        self._guard_node_fit(width, height, title, subtitle, tag)
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
        segs: list[tuple[Point, Point, int]] = []
        for idx, (start, end) in enumerate(zip(points, points[1:])):
            if start[0] != end[0] and start[1] != end[1]:
                raise ValueError(f"Connector segment is diagonal: {start} -> {end}")
            length = abs(end[0] - start[0]) + abs(end[1] - start[1])
            segs.append((start, end, length))
            # 结构守卫 1：每段 >= 28px（圆角 radius=8 占两端各 8，剩 >=12px 直线；且箭头不挤压）
            if length < 28:
                raise ValueError(
                    f"Connector segment #{idx + 1} {start} -> {end} too short ({length}px < 28px)"
                )
        # 结构守卫 2：弯折次数 (len(points)-2) <= 2，即 points <= 4
        if len(points) > 4:
            raise ValueError(
                f"Connector has {len(points) - 2} bends (points={len(points)}); keep <= 2 bends (points<=4)"
            )
        # 结构守卫 3：末段 >= 28px。绘制时会从路径终点沿末段前退 7px 放 marker，
        # 所以 28 末段 → 剩余 21px 可视直线，足够清楚地显示箭头方向。
        last_len = segs[-1][2]
        if last_len < 28:
            raise ValueError(
                f"Connector last segment ({segs[-1][0]} -> {segs[-1][1]}) = {last_len}px < 28px"
            )
        # 关键：渲染前把 connector 两端从节点边界"抽出来"避免与节点描边重叠。
        #   - 起点沿首段方向"远离节点" 4px：线起端与源节点边框之间留 4px 气隙
        #   - 终点从末段方向"回退 9px"：marker refX=9 顶点恰好落在原 points[-1]（节点边界），
        #     这样 connector 线末端到节点边框之间留 9px 的箭头空腔 + 气隙，不再贴。
        render_points = _push_first_point(points, 4)
        render_points = _retract_last_point(render_points, 9)
        path = _rounded_path(render_points)
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
        # 图层：zone 背景 → 节点（含不透明 mask，画在连线下方接住"溢出线"但不遮挡末端箭头）
        #     → connector 线 → connector 末端文字标签（带半透明底盖线）
        # nodes 在 connectors 前：避免盒子盖掉进入盒边的箭头，但 node-mask 需要配合"箭头
        # 终点前退"来避免线被 mask 切断后看不见。
        body = "".join(
            element
            for name in ("zones", "nodes", "connectors", "annotations")
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
        # marker: 箭头">"，箭头顶点 (9,5) 对齐 refX=9，刚好命中 connector 路径终点
        # （即 node 边界坐标），顶点之后留 1px 余量，markerWidth=10 避免被裁。
        # 线宽 1.6 与 connector 主线 1.6 对齐，箭头视觉更锐利。
        return (
            f'<marker id="{self.slug}-arrow-{name}" markerWidth="10" markerHeight="10" '
            f'refX="9" refY="5" orient="auto-start-reverse">'
            f'<path d="M0.5,0.5 L9,5 L0.5,9.5" fill="none" stroke="{color}" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
        )

    def _styles(self) -> str:
        t = self.theme
        return f"""<style>
.editorial-diagram text{{font-family:{_SANS};fill:{t.ink};letter-spacing:0}}
.zone>rect:first-child{{fill:{t.ink};fill-opacity:.018;stroke:{t.rule};stroke-width:1}}
.zone-label-mask{{fill:{t.paper}}}
.connector-label rect{{fill:{t.paper};fill-opacity:.82}}
.zone-label,.node-tag,.connector-label text,.label-eyebrow{{font-family:{_MONO};font-size:11px;font-weight:600;letter-spacing:.08em;fill:{t.muted}}}
.lane rect{{fill:{t.paper};stroke:{t.rule_soft};stroke-width:1}}.lane-tinted rect{{fill:{t.ink};fill-opacity:.018}}
.lane line{{stroke:{t.rule};stroke-width:1}}.lane-label{{font-family:{_MONO};font-size:11px;font-weight:600;fill:{t.muted};letter-spacing:.06em}}
.connector{{fill:none;stroke:{t.muted};stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}}
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

    def _fit_node_size(self, width: int, height: int, title, subtitle, tag: str) -> tuple[int, int]:
        """按标题/副标题/角标内容自适应节点宽高，保证文本落在框内（可缩可放）。"""
        title_size = 14 if self.typography == "expanded" else 13
        lines = title if isinstance(title, (tuple, list)) else (title,)
        line_count = len(lines)
        title_width = max((_text_width(line, title_size) for line in lines), default=0)
        subtitle_width = _text_width(subtitle, 10, mono=True) if subtitle else 0
        tag_width = len(tag) * 7 + 12 if tag else 0
        inner = max(title_width, subtitle_width, tag_width)
        # 水平：左右各 14px 内边距，再留 6px 防字宽测量误差。
        width = max(width, _grid_ceil(inner + 2 * 14 + 6))

        if tag:
            title_y = (48 if self.typography == "expanded" else 44) if line_count > 1 else 40
        else:
            title_y = 28
        title_bottom = _tspan_bottom(title_y, line_count, 16)
        if subtitle:
            expanded_spacing = 4 * (line_count - 1) if self.typography == "expanded" else 0
            body_bottom = _tspan_bottom(title_bottom + 20 + expanded_spacing, 1, 12)
        else:
            body_bottom = title_bottom + 6
        height = max(height, _grid_ceil(body_bottom + 14))
        return width, height

    def _guard_node_fit(self, width: int, height: int, title, subtitle, tag: str) -> None:
        """渲染期溢出守卫：任何一行文本超出容器即报错，而不是渲染后才被肉眼发现。"""
        title_size = 14 if self.typography == "expanded" else 13
        lines = title if isinstance(title, (tuple, list)) else (title,)
        inner_width = width - 28
        for line in lines:
            if _text_width(line, title_size) > inner_width:
                trunced = line if len(line) <= 24 else line[:21] + "..."
                raise ValueError(f"node title '{trunced}' (est. {_text_width(line, title_size):.0f}px) "
                                 f"exceeds box width {inner_width}px")
        if subtitle and _text_width(subtitle, 10, mono=True) > inner_width:
            raise ValueError(f"node subtitle '{subtitle}' exceeds box width {inner_width}px")
        if tag and len(tag) * 7 + 12 > inner_width:
            raise ValueError(f"node tag '{tag}' exceeds box width {inner_width}px")

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


# --- 健壮性：按内容测量文本宽度，避免文字超框位第 1 位。

# 全角 / CJK 范围及其常用标点按整字宽计，ASCII 按比例计，形成保守的像素估计。
_WIDE_MARKS = set("，。！？；：、（）《》「」『』—…·‘’“”：")


def _char_width(ch: str, size: int, mono: bool) -> float:
    if ord(ch) > 0x2E80 or ch in _WIDE_MARKS:
        return float(size)
    return size * (0.62 if mono else 0.55)


def _text_width(text: str, size: int, mono: bool = False) -> float:
    """估算单行文本像素宽度，CJK 感知且偏保守（宁大勿小）。"""
    return sum(_char_width(c, size, mono) for c in text)


def _tspan_bottom(title_y: int, line_count: int, gap: int) -> int:
    """多行 tspans 以首行中线 title_y 为基准、向下以 gap 步进，返回最后一行基线。"""
    return title_y + (line_count - 1) * gap


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


def _retract_last_point(points: Sequence[Point], amount: int) -> tuple[Point, ...]:
    """将 points 最后一点沿末段方向退回 amount px（使 marker 顶点落在原终点）。"""
    if len(points) < 2:
        return tuple(points)
    head = list(points[:-2])
    prev = points[-2]
    last = points[-1]
    length = abs(last[0] - prev[0]) + abs(last[1] - prev[1])
    if length > amount:
        new_last = _toward(last, prev, amount)
        head.append(prev)
        head.append(new_last)
        return tuple(head)
    return tuple(points[:-1] + (prev,))


def _push_first_point(points: Sequence[Point], amount: int) -> tuple[Point, ...]:
    """将 points 起点沿首段方向远离 amount px（线起端不贴源节点边框）。"""
    if len(points) < 2:
        return tuple(points)
    first = points[0]
    second = points[1]
    length = abs(second[0] - first[0]) + abs(second[1] - first[1])
    if length > amount:
        new_first = _toward(first, second, amount)
        return (new_first,) + tuple(points[1:])
    return tuple(points)
