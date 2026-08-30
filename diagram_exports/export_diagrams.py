#!/usr/bin/env python3
"""把 9 张架构图 SVG 渲染导出为独立 SVG 文件，供后续转 PNG 发送到飞书。"""
import sys
from pathlib import Path

_WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_WORKSPACE))

from src.diagrams import render_all  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = render_all()
    for slug, svg in diagrams.items():
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.name} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()