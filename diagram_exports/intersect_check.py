"""Detect connectors whose segments cross any node body interior.

selfcheck.py only verifies start/end points are not inside a node body.
This script goes further: every polyline segment of every connector path
is tested for intersection with every node-mask rect's interior (with a
small inset margin so legitimate boundary touches do not count).

This catches real "line crossing a node body" problems that selfcheck misses.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.diagrams import DIAGRAMS  # noqa: E402

_MASK_RE = re.compile(
    r'<rect class="(?:node-mask|decision-mask-rect)" x="(-?\d+(?:\.\d+)?)" y="(-?\d+(?:\.\d+)?)" '
    r'width="(\d+(?:\.\d+)?)" height="(\d+(?:\.\d+)?)"[^/]*/>'
)
_CONN_PATH_RE = re.compile(
    r'<path[^>]*class="connector(?: connector-\w+)?"[^>]*d="([^"]+)"[^>]*/>'
)
# Arrow V: M x y L x y L x y  (exactly 3 points, all M/L)
_ARROW_RE = re.compile(r"^M\s[\d.\-]+\s[\d.\-]+ L [\d.\-]+ [\d.\-]+ L [\d.\-]+ [\d.\-]+$")

# tokenise path d: returns list of (x, y) from M/L only; Q skips control point.
def _path_points(d: str) -> list[tuple[float, float]]:
    tokens = d.replace(",", " ").split()
    pts: list[tuple[float, float]] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if not t or t[0] not in "MLQ":
            i += 1
            continue
        cmd = t[0]
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
        i += 1
        if i >= len(tokens):
            break
        y = float(tokens[i])
        if cmd in "ML":
            pts.append((x, y))
        elif cmd == "Q":
            i += 1
            if i + 1 >= len(tokens):
                break
            ex = float(tokens[i])
            ey = float(tokens[i + 1])
            i += 1
            pts.append((ex, ey))
        i += 1
    return pts


def _parse_bboxes(svg: str) -> list[tuple[float, float, float, float]]:
    out = []
    for m in _MASK_RE.finditer(svg):
        x, y, w, h = (float(v) for v in m.groups())
        out.append((x, y, w, h))
    return out


def _in_strict(p, b, inset=1.5):
    """Point strictly inside box, with inset margin so face touches don't count."""
    x, y = p
    bx, by, bw, bh = b
    return bx + inset < x < bx + bw - inset and by + inset < y < by + bh - inset


def _ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def _seg_inter(a, b, c, d):
    return _ccw(a, c, d) != _ccw(b, c, d) and _ccw(a, b, c) != _ccw(a, b, d)


def _seg_crosses_box(p1, p2, b):
    """True if segment p1->p2 passes through interior of box b.

    Uses dense sampling along the segment and checks if any sample is strictly
    inside the box (with an inset margin so face/corner touches do NOT count).
    This avoids false positives from segments that merely run along a face or
    touch a corner.
    """
    # Sample N points along the segment (excluding the endpoints themselves
    # to avoid counting face-touching endpoints as crossings).
    N = 24
    for k in range(1, N):
        t = k / N
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        if _in_strict((x, y), b):
            return True
    return False


def check_slug(slug: str, svg: str) -> list[str]:
    issues = []
    bboxes = _parse_bboxes(svg)
    if not bboxes:
        return ["no node bboxes detected"]
    paths = []
    for m in _CONN_PATH_RE.finditer(svg):
        d = m.group(1)
        if _ARROW_RE.match(d):
            continue
        paths.append(d)
    for i, d in enumerate(paths):
        pts = _path_points(d)
        if len(pts) < 2:
            continue
        for j in range(len(pts) - 1):
            p1, p2 = pts[j], pts[j + 1]
            for k, b in enumerate(bboxes):
                if _seg_crosses_box(p1, p2, b):
                    bx, by, bw, bh = b
                    issues.append(
                        f"conn#{i} seg{j} ({p1[0]:.0f},{p1[1]:.0f})->"
                        f"({p2[0]:.0f},{p2[1]:.0f}) crosses "
                        f"box(L{bx:.0f} T{by:.0f} R{bx+bw:.0f} B{by+bh:.0f})"
                    )
    return issues


def main() -> int:
    total = 0
    bad = []
    for slug, fn in DIAGRAMS.items():
        svg = fn()
        issues = check_slug(slug, svg)
        n = len([1 for _ in re.finditer(r'<path[^>]*class="connector connector-', svg)])
        total += n
        status = "OK" if not issues else f"BAD ({len(issues)} crosses)"
        print(f"[{status}] {slug}")
        for s in issues:
            print(f"    - {s}")
        if issues:
            bad.append(slug)
    print(f"\nTotal connectors: {total}")
    if bad:
        print(f"DIAGRAMS WITH CROSSINGS: {len(bad)}: {', '.join(bad)}")
        return 1
    print("NO NODE-BODY CROSSINGS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
