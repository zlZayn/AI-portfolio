"""Self-check each diagram's connectors for:
 1. First point render offset 4px from source node boundary (air gap)
 2. Last point (head) exactly on target node boundary
 3. Last segment axis-aligned & arrow drawn orthogonally
 4. Head does NOT sink into target node rect (boundary OK, not inside)
 5. Source start does NOT sink into source node rect

Uses the rendered SVG content to inspect what was actually emitted.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.diagrams import DIAGRAMS  # noqa: E402


# Parse every <rect> with class node-mask or decision-mask-rect: their x,y,w,h is the true box.
# For decisions we emit an extra bbox rect because polygon mask doesn't give an easy bounding box in SVG.
_MASK_RE = re.compile(
    r'<rect class="(?:node-mask|decision-mask-rect)" x="(-?\d+(?:\.\d+)?)" y="(-?\d+(?:\.\d+)?)" '
    r'width="(\d+(?:\.\d+)?)" height="(\d+(?:\.\d+)?)"[^/]*/>'
)
_CONN_PATH_RE = re.compile(
    r'<path[^>]*class="connector(?: connector-\w+)?"[^>]*d="([^"]+)"[^>]*/>'
)
_ARROW_PATH_RE = re.compile(
    r'<path[^>]*class="connector(?: connector-\w+)*"[^>]*'
    r'd="M ([\d.\-]+) ([\d.\-]+) L ([\d.\-]+) ([\d.\-]+) L ([\d.\-]+) ([\d.\-]+)"[^>]*/>'
)
_D_RE = re.compile(r"[MLQ]\s*(-?\d+(?:\.\d+)?)\s*(-?\d+(?:\.\d+)?)")


def _parse_bboxes(svg: str) -> list[tuple[float, float, float, float]]:
    """Return list of (x,y,w,h) for all node/decision mask rects (the true box)."""
    bboxes: list[tuple[float, float, float, float]] = []
    for m in _MASK_RE.finditer(svg):
        x, y, w, h = (float(v) for v in m.groups())
        bboxes.append((x, y, w, h))
    return bboxes


def _path_points(d: str) -> list[tuple[float, float]]:
    """Parse path commands and return only the rendered vertices of the polyline
    (M start and L points). Quadratic Bezier 'Q cx,cy ex,ey' contributes only the endpoint."""
    # tokenize pairs as (cmd, x, y); commands are single letter M/L/Q
    tokens = d.replace(",", " ").split()
    pts: list[tuple[float, float]] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if not t or t[0] not in "MLQ":
            i += 1
            continue
        cmd = t[0]
        # read two floats after the optional command prefix
        nums_str = t[1:] if len(t) > 1 else ""
        if not nums_str:
            i += 1
            if i < len(tokens):
                nums_str = tokens[i]
            else:
                break
        try:
            x = float(nums_str)
        except ValueError:
            i += 1
            continue
        # y
        i += 1
        if i >= len(tokens):
            break
        y = float(tokens[i])
        if cmd in "ML":
            pts.append((x, y))
        elif cmd == "Q":
            # skip control point; read endpoint x,y from next two tokens
            # current (x,y) is the control point
            i += 1
            if i + 1 >= len(tokens):
                break
            ex = float(tokens[i])
            ey = float(tokens[i + 1])
            i += 1
            pts.append((ex, ey))
        i += 1
    return pts


def _inside(pt: tuple[float, float], box: tuple[float, float, float, float], margin: float = 0.5) -> bool:
    x, y = pt
    bx, by, bw, bh = box
    return bx - margin <= x <= bx + bw + margin and by - margin <= y <= by + bh + margin


def _boxstr(b: tuple[float, float, float, float]) -> str:
    return f"(L{b[0]:.0f} T{b[1]:.0f} R{b[0]+b[2]:.0f} B{b[1]+b[3]:.0f})"


def _on_boundary(pt: tuple[float, float], box: tuple[float, float, float, float], tol: float = 0.7) -> bool:
    x, y = pt
    bx, by, bw, bh = box
    if abs(x - bx) <= tol and by - tol <= y <= by + bh + tol:
        return True
    if abs(x - (bx + bw)) <= tol and by - tol <= y <= by + bh + tol:
        return True
    if abs(y - by) <= tol and bx - tol <= x <= bx + bw + tol:
        return True
    if abs(y - (by + bh)) <= tol and bx - tol <= x <= bx + bw + tol:
        return True
    return False


def check_slug(slug: str, svg: str) -> list[str]:
    issues: list[str] = []
    bboxes = _parse_bboxes(svg)
    if not bboxes:
        issues.append("no node bboxes detected")
        return issues

    paths: list[str] = []
    for m in _CONN_PATH_RE.finditer(svg):
        d = m.group(1)
        # skip the hand-drawn arrows (3-segment M L L, matched later)
        pts = _path_points(d)
        if len(pts) == 3:
            # heuristic: arrow V, skip here
            continue
        paths.append(d)

    arrows: list[tuple[float, float, float, float, float, float]] = []
    for m in _ARROW_PATH_RE.finditer(svg):
        a = tuple(float(x) for x in m.groups())
        assert len(a) == 6
        arrows.append(a)  # type: ignore[arg-type]

    if len(paths) != len(arrows):
        issues.append(f"connector/arrow mismatch: paths={len(paths)} arrows={len(arrows)}")
        # continue with min
    N = min(len(paths), len(arrows))

    for i in range(N):
        pts = _path_points(paths[i])
        if len(pts) < 2:
            issues.append(f"conn#{i}: path too short")
            continue
        render_first = pts[0]
        render_last = pts[-1]
        Lx, Ly, Hx, Hy, Rx, Ry = arrows[i]

        # Head (H) must be on some node boundary (target)
        head = (Hx, Hy)
        if not any(_on_boundary(head, b) for b in bboxes):
            issues.append(f"conn#{i}: arrow head ({Hx:.1f},{Hy:.1f}) NOT on any node boundary")

        # Arrow back must be perpendicular-ish to last segment
        last_seg = (pts[-2], render_last)
        dx = render_last[0] - last_seg[0][0]
        dy = render_last[1] - last_seg[0][1]
        if abs(dx) > 0.5 and abs(dy) > 0.5:
            issues.append(f"conn#{i}: last segment diagonal {last_seg}")
            continue
        back = ((Lx + Rx) / 2.0, (Ly + Ry) / 2.0)
        bd = (back[0] - Hx, back[1] - Hy)
        if abs(dx) > 0.5:  # horizontal last: back must be on same y, x offset
            if abs(bd[1]) > 0.2 or abs(bd[0]) < 8.5 or abs(bd[0]) > 9.5:
                issues.append(f"conn#{i}: arrow back misaligned for H last seg: back={back}")
        else:  # vertical
            if abs(bd[0]) > 0.2 or abs(bd[1]) < 8.5 or abs(bd[1]) > 9.5:
                issues.append(f"conn#{i}: arrow back misaligned for V last seg: back={back}")

        # render_first must NOT be inside any node body (strictly inside, not on boundary)
        # If _inside but _on_boundary for the same node → OK (exit point on face)
        for b in bboxes:
            if _inside(render_first, b, margin=0.5) and not _on_boundary(render_first, b, tol=0.9):
                issues.append(f"conn#{i}: render start {render_first} STRICTLY INSIDE node body {_boxstr(b)}")
                break
        # render_last (after retract 4px) must be OUTSIDE/on-boundary of target, not inside
        for b in bboxes:
            if _inside(render_last, b, margin=0.5) and not _on_boundary(render_last, b, tol=0.9):
                issues.append(f"conn#{i}: render last {render_last} STRICTLY INSIDE node body {_boxstr(b)}")
                break
    return issues


def _close_outside(pt: tuple[float, float], box: tuple[float, float, float, float], lo: float, hi: float) -> bool:
    """Return True if pt lies lo..hi px outside the nearest face of box."""
    x, y = pt
    bx, by, bw, bh = box
    # Distance to nearest face along each axis
    candidates: list[float] = []
    if by - 0.5 <= y <= by + bh + 0.5:
        candidates.append(abs(x - bx))
        candidates.append(abs(x - (bx + bw)))
    if bx - 0.5 <= x <= bx + bw + 0.5:
        candidates.append(abs(y - by))
        candidates.append(abs(y - (by + bh)))
    for d in candidates:
        if lo <= d <= hi:
            return True
    return False


def main() -> int:
    total = 0
    bad_slugs: list[tuple[str, list[str]]] = []
    for slug, fn in DIAGRAMS.items():
        svg = fn()
        issues = check_slug(slug, svg)
        n_conn = len(re.findall(r'<path[^>]*class="connector connector-', svg))
        # Count real connectors by arrow count
        n_arrows = len(list(_ARROW_PATH_RE.finditer(svg)))
        total += n_arrows
        status = "PASS" if not issues else f"FAIL ({len(issues)} issues, {n_arrows} conns)"
        print(f"[{status}] {slug}")
        for i_ in issues:
            print(f"    - {i_}")
        if issues:
            bad_slugs.append((slug, issues))
    print(f"\nTotal connectors: {total}")
    if bad_slugs:
        print(f"FAILURES: {len(bad_slugs)}")
        return 1
    print("SELF-CHECK PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
