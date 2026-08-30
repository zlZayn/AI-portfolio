"""Dual-mode image generation workbench architecture for Imagora."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "imagora",
        "Imagora dual-mode image generation workbench",
        "Contract-formatted prompts import as batch cards; classic form and "
        "infinite canvas share one task pipeline; generated results are stored "
        "by content hash and rebound as canvas nodes for chained iteration.",
        height=780,
        typography="expanded",
    )
    canvas.label(32, 32, "DUAL FRONTENDS / ONE PIPELINE / CONTRACT-DRIVEN PROMPTS")

    # Zone A: contract-driven prompt import above the interaction surfaces.
    canvas.zone(32, 64, 896, 180, "PROMPT CONTRACT")
    canvas.node(56, 108, 208, 100, "Multi-modal LLM", "contract output", "LLM", "optional", fit=True)
    canvas.node(360, 108, 224, 100, "Prompt Import", "paste → batch cards", "CONTRACT", "focal", fit=True)
    canvas.connector(((264, 156), (360, 156)), "FORMATTED", "accent")
    canvas.annotation(620, 136, "5 CAROUSEL + 8 DETAIL TEMPLATES", 240)
    canvas.annotation(620, 176, "ERRORS MARKED RED / NEVER GUESSED", 240)

    # Zone B: two interaction surfaces plus the compact rebound chain.
    canvas.zone(32, 276, 896, 220, "DUAL-MODE INTERACTION")
    canvas.node(56, 328, 156, 88, "Classic form", "instant submit", "FORM", "muted", fit=True)
    canvas.node(232, 320, 208, 104, "Infinite canvas", "nodes + edges, typed constraints", "CANVAS", "focal", fit=True)
    canvas.node(492, 336, 120, 72, "Prompt node", "chain step", "NODE", fit=True)
    canvas.node(648, 336, 120, 72, "Result node", "auto-image-node", "REBOUND", "success", fit=True)
    canvas.connector(((612, 372), (648, 372)))
    canvas.connector(((648, 372), (612, 372)), "RELINK", "dashed")
    canvas.connector(((180, 416), (180, 456), (232, 456), (232, 388)), "ONE-CLICK RESTORE", "dashed")

    # Zone C: one pipeline, the asset registry, and the only upstream.
    canvas.zone(32, 528, 896, 188, "ONE PIPELINE / ASSETS / UPSTREAM")
    canvas.node(56, 576, 136, 88, "TaskManager", "one queue / max 10", "QUEUE", "focal", fit=True)
    canvas.node(272, 576, 176, 88, "OpenAI-compatible API", "only external dependency", "UPSTREAM", "optional", fit=True)
    canvas.node(480, 576, 120, 88, "Image output", "generated image", "OUTPUT", "store", fit=True)
    canvas.node(664, 576, 176, 88, "Asset Registry", "content hash → .assets", "SHA-1", "store", fit=True)

    canvas.connector(((132, 416), (132, 576)), "submit")
    canvas.connector(((336, 424), (336, 512), (124, 512), (124, 576)), "run")
    canvas.connector(((204, 620), (272, 620)), "GENERATE", "accent")
    canvas.connector(((368, 576), (368, 540), (544, 540), (544, 576)), "IMAGE", "success")
    canvas.connector(((540, 576), (648, 576), (648, 372)), "REBOUND", "dashed")
    canvas.connector(((540, 664), (540, 696), (752, 696), (752, 664)), "STORE BY SHA1")

    canvas.annotation(32, 748, "WORKFLOW FILES STORE REGISTRY IDS / NEVER PATHS", 640)
    return canvas.render()