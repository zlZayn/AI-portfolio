#!/usr/bin/env python3
"""把 diagram_exports/ 下最新 SVG 统一转成 PNG（1920 宽），供视觉自检。"""
import pathlib
import sys

import cairosvg

OUT = pathlib.Path(__file__).resolve().parent
TARGETS = [OUT / f"{slug}.svg" for slug in sys.argv[1:]] if len(sys.argv) > 1 else sorted(OUT.glob("*.svg"))


def main() -> None:
    for svg in TARGETS:
        png = OUT / (svg.stem + ".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1920)
        print(f"rendered {png.name} ({png.stat().st_size}B)")


if __name__ == "__main__":
    main()