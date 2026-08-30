"""Helper: given project render, inspect all node boxes and list existing connector points vs their source/target faces.

Reports: for each connector the SOURCE node (nearest box whose boundary touches points[0]) and the TARGET node (nearest box whose boundary touches points[-1]).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

import src.diagrams.svg as _svg

_orig_conn = _svg.Canvas.connector
_CAPTURED: list[tuple] = []


def _cap(self, points, label="", style="default", label_at=None):
    try:
        _orig_conn(self, points, label=label, style=style, label_at=label_at)
        _CAPTURED.append((points, label, style, None))
    except ValueError as e:
        _CAPTURED.append((points, label, style, str(e)))


_svg.Canvas.connector = _cap

from src.diagrams import DIAGRAMS  # noqa: E402

_MASK_RE = re.compile(
    r'<rect class="(?:node-mask|decision-mask-rect)" x="(-?\d+(?:\.\d+)?)" y="(-?\d+(?:\.\d+)?)" '
    r'width="(\d+(?:\.\d+)?)" height="(\d+(?:\.\d+)?)"[^/]*/>'
)
_TITLE_RE = re.compile(
    r'<text class="(?:node-title|decision-title)"[^>]*>(.*?)</text>', flags=re.S
)


def _boxes(svg: str):
    return [tuple(float(x) for x in m.groups()) for m in _MASK_RE.finditer(svg)]


def _titles(svg: str):
    return [re.sub(r"<[^>]+>", "", t) for t in _TITLE_RE.findall(svg)]


def _face(pt, b, tol=0.7):
    x, y = pt
    bx, by, bw, bh = b
    if abs(x - bx) <= tol and by - tol <= y <= by + bh + tol:
        return "L"
    if abs(x - (bx + bw)) <= tol and by - tol <= y <= by + bh + tol:
        return "R"
    if abs(y - by) <= tol and bx - tol <= x <= bx + bw + tol:
        return "T"
    if abs(y - (by + bh)) <= tol and bx - tol <= x <= bx + bw + tol:
        return "B"
    return None


def analyze(slug: str):
    global _CAPTURED
    _CAPTURED.clear()
    svg = DIAGRAMS[slug]()
    b = _boxes(svg)
    t = _titles(svg)
    print(f"\n=== {slug} ===")
    for i, (bx, by, bw, bh) in enumerate(b):
        name = t[i] if i < len(t) else "?"
        print(f"  box#{i:2d} {name[:36]:36s} L{bx:.0f} T{by:.0f} R{bx+bw:.0f} B{by+bh:.0f}")
    for ci, (pts, label, style, err) in enumerate(_CAPTURED):
        src_s = []
        tgt_s = []
        for i, box in enumerate(b):
            fs = _face(pts[0], box)
            if fs is not None:
                # outside correct side? points[1] should be on outside
                src_s.append((f"box#{i}", fs))
            ft = _face(pts[-1], box)
            if ft is not None:
                tgt_s.append((f"box#{i}", ft))
        src_bad = not src_s
        tgt_bad = not tgt_s
        # Check approach side for target
        tgt_ok_extra = ""
        if tgt_s:
            (boxref, face) = tgt_s[0]
            idx = int(boxref[4:])
            bx, by, bw, bh = b[idx]
            prev = pts[-2]
            last = pts[-1]
            dx = last[0] - prev[0]
            dy = last[1] - prev[1]
            # travel dir
            if dx and face == "R":
                ok = dx < 0  # approach from RIGHT (x>R) going LEFT into face
            elif dx and face == "L":
                ok = dx > 0  # approach from LEFT going RIGHT into face
            elif dy and face == "B":
                ok = dy < 0  # approach from BELOW going UP into B face
            elif dy and face == "T":
                ok = dy > 0  # approach from ABOVE going DOWN into T face
            else:
                ok = None
            tgt_ok_extra = f" approach_inside={ok if ok is not None else '?'}"
        status = "OK" if (not err and not src_bad and not tgt_bad) else "ERR"
        err_s = f" ERR={err}" if err else ""
        bad_s = ""
        if src_bad: bad_s += " SRC-OOB"
        if tgt_bad: bad_s += " TGT-OOB"
        segs = []
        for p0, p1 in zip(pts, pts[1:]):
            l = abs(p1[0] - p0[0]) + abs(p1[1] - p0[1])
            segs.append(str(l))
        p1_src = pts[1] if len(pts) > 1 else None
        print(f"  conn#{ci:2d} [{status:2s}] pts={pts} segs=({','.join(segs)}) src={src_s or 'NONE'} tgt={tgt_s or 'NONE'}{tgt_ok_extra}{bad_s}{err_s}")


for s in ["decision-maker", "schema-mapper", "tool-calling", "collaborate", "tier-guardian", "raw-to-guide", "imagora"]:
    analyze(s)
