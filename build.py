#!/usr/bin/env python3
"""
Assemble all sources into a single self-contained HTML page.
Orchestrates: YAML data --> inline images --> data tables --> Mermaid diagrams --> Jinja2 render
"""

import yaml
import base64
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from src.data_tables import generate_all, table_css
from src.diagrams import render_all as render_diagrams

BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_PATH = BASE_DIR / "index.html"


def _load_yaml(filename: str) -> dict:
    with open(str(CONTENT_DIR / filename), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _encode_img(img_file: Path) -> dict:
    with open(str(img_file), "rb") as f:
        data = base64.b64encode(f.read()).decode()
    mime = "png" if img_file.suffix[1:] == "png" else "jpeg"
    return {"data_uri": f"data:image/{mime};base64,{data}", "alt": img_file.stem}


def _img_key(name: str) -> str:
    import re

    return re.sub(r"-(top|bottom|middle)$", "", name, flags=re.IGNORECASE)


def _stack_key(name: str) -> int:
    if name.endswith("-top"):
        return 0
    if name.endswith("-bottom"):
        return 2
    if name.endswith("-middle"):
        return 1
    return 0


def _inline_images(projects: list) -> None:
    for project in projects:
        img_dir = IMAGES_DIR / project["id"]
        items = {}
        if img_dir.exists():
            for img_file in sorted(img_dir.iterdir()):
                if img_file.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif"):
                    continue
                key = _img_key(img_file.stem)
                items.setdefault(key, []).append(_encode_img(img_file))

        for key in items:
            items[key].sort(key=lambda x: _stack_key(x["alt"]))

        screenshots = []
        for key, group in items.items():
            if len(group) == 1:
                group[0]["type"] = "single"
                screenshots.append(group[0])
            else:
                stacked = []
                for i, img in enumerate(group):
                    stacked.append(img)
                    if i < len(group) - 1:
                        stacked.append({"type": "seam"})
                screenshots.append({"type": "stack", "items": stacked})
        project["screenshots"] = screenshots


def assemble() -> None:
    profile = _load_yaml("profile.yaml")
    projects = _load_yaml("projects.yaml")["projects"]

    _inline_images(projects)

    generated = generate_all()
    for p in projects:
        g = generated.get(p["id"])
        if g:
            p["generated_content"] = g

    print("Rendering diagrams...")
    diagrams = render_diagrams()
    for p in projects:
        d = diagrams.get(p["id"])
        if d:
            p["diagram_svg"] = d

    with open(str(STATIC_DIR / "style.css"), encoding="utf-8") as f:
        inline_css = f.read()
    inline_css += "\n" + table_css()
    with open(str(STATIC_DIR / "script.js"), encoding="utf-8") as f:
        inline_js = f.read()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    base = env.get_template("base.html")
    hero_html = env.get_template("hero.html").render(projects=projects, profile=profile)
    grid_html = env.get_template("grid.html").render(projects=projects)
    project_htmls = [
        env.get_template("project.html").render(project=p, projects=projects)
        for p in projects
    ]
    content = hero_html + grid_html + "".join(project_htmls)

    full_html = base.render(
        profile=profile,
        projects=projects,
        content=content,
        inline_css=inline_css,
        inline_js=inline_js,
        build_time=datetime.now().strftime("%B %d, %Y %H:%M"),
    )

    with open(str(OUTPUT_PATH), "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Built: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    assemble()
