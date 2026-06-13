"""
AI Portfolio Builder
Python + Jinja2 -> single self-contained HTML file
"""

import yaml
import base64
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from generate_content import generate_all, table_css
from diagrams import render_all as render_diagrams

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR


def load_yaml(filename: str) -> dict:
    with open(str(CONTENT_DIR / filename), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _encode_img(img_file: Path) -> dict:
    with open(str(img_file), "rb") as f:
        data = base64.b64encode(f.read()).decode()
    mime = "png" if img_file.suffix[1:] == "png" else "jpeg"
    return {"data_uri": f"data:image/{mime};base64,{data}", "alt": img_file.stem}


def _img_key(name: str) -> str:
    """Strip trailing -top, -bottom, -middle to group related parts."""
    import re
    return re.sub(r"-(top|bottom|middle)$", "", name, flags=re.IGNORECASE)


def _stack_key(name: str) -> int:
    """Sort within stack: top before bottom before middle."""
    if name.endswith("-top"): return 0
    if name.endswith("-bottom"): return 2
    if name.endswith("-middle"): return 1
    return 0


def inline_images(projects: list, base_path: Path) -> None:
    for project in projects:
        img_dir = base_path / "images" / project["id"]
        items = {}
        if img_dir.exists():
            for img_file in sorted(img_dir.iterdir()):
                if img_file.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif"):
                    continue
                key = _img_key(img_file.stem)
                items.setdefault(key, []).append(_encode_img(img_file))

        # Sort within each stack group: top first, bottom last
        for key in items:
            items[key].sort(key=lambda x: _stack_key(x["alt"]))

        screenshots = []
        for key, group in items.items():
            if len(group) == 1:
                group[0]["type"] = "single"
                screenshots.append(group[0])
            else:
                # Multiple parts for same image -> stack vertically
                # Add seam markers between them
                stacked = []
                for i, img in enumerate(group):
                    stacked.append(img)
                    if i < len(group) - 1:
                        stacked.append({"type": "seam"})
                screenshots.append({"type": "stack", "items": stacked})
        project["screenshots"] = screenshots


def build() -> None:
    profile = load_yaml("profile.yaml")
    projects = load_yaml("projects.yaml")["projects"]

    inline_images(projects, ASSETS_DIR)

    # Auto-generate content from project source data
    generated = generate_all()
    for p in projects:
        g = generated.get(p["id"])
        if g:
            p["generated_content"] = g

    # Render Mermaid diagrams
    print("Rendering diagrams...")
    diagrams = render_diagrams()
    for p in projects:
        d = diagrams.get(p["id"])
        if d:
            p["diagram_svg"] = d

    with open(str(ASSETS_DIR / "style.css"), encoding="utf-8") as f:
        inline_css = f.read()
    inline_css += "\n" + table_css()
    with open(str(ASSETS_DIR / "script.js"), encoding="utf-8") as f:
        inline_js = f.read()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    base = env.get_template("base.html")
    hero_html = env.get_template("sections/hero.html").render(
        projects=projects, profile=profile
    )
    grid_html = env.get_template("sections/grid.html").render(projects=projects)
    project_htmls = [
        env.get_template("sections/project.html").render(project=p, projects=projects)
        for p in projects
    ]
    content = hero_html + grid_html + "".join(project_htmls)

    full_html = base.render(
        profile=profile, projects=projects, content=content,
        inline_css=inline_css, inline_js=inline_js
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "index.html"
    with open(str(out_path), "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Built: {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    if "--rebuild" in sys.argv:
        print("Rebuild flag set -- forcing full regeneration (cache ignored)")
    build()



