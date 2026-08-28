"""Dual-mode image generation workbench architecture for Imagora."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "imagora",
        "Imagora dual-mode image generation workbench",
        "Classic form and infinite canvas share one task pipeline. "
        "Results are stored in the asset registry by content hash and "
        "rebound as new canvas nodes for chained iteration.",
        height=720,
        typography="expanded",
    )
    canvas.label(32, 32, "DUAL FRONTENDS / ONE PIPELINE / ASSETS BY CONTENT HASH")

    # Zone 1: two interaction surfaces; results rebound into the canvas.
    canvas.zone(32, 64, 896, 200, "INTERACTION / DUAL MODE")
    canvas.node(56, 112, 168, 84, "Classic form", "instant submit", "FORM", "muted")
    canvas.node(240, 96, 240, 100, "Infinite canvas", "nodes + edges, typed constraints", "CANVAS", "focal")
    canvas.node(500, 104, 136, 76, "Prompt node", "step in the chain", "NODE")
    canvas.node(680, 104, 136, 76, "Result node", "auto-image-node", "REBOUND", "success")
    canvas.connector(((636, 144), (680, 144)))
    canvas.connector(((804, 180), (804, 216), (568, 216), (568, 180)), "RELINK", "dashed")

    # Zone 2: one unified backend pipeline behind both frontends.
    canvas.zone(32, 296, 896, 168, "UNIFIED BACKEND / ONE TASK PIPELINE")
    canvas.node(56, 336, 168, 96, "TaskManager", "one queue / max 10 workers", "QUEUE", "focal")
    canvas.node(252, 336, 176, 96, "Asset Registry", "content hash -> .assets", "SHA-1", "store")
    canvas.node(468, 336, 168, 96, "History ledger", "generation.jsonl", "JSONL", "store")
    canvas.node(664, 336, 192, 96, "Window allocator", "server-side ids / netstat truth", "MULTI")

    # Zone 3: the only external dependency, wrapped in one module.
    canvas.zone(32, 500, 896, 164, "ONLY EXTERNAL DEPENDENCY")
    canvas.node(368, 548, 184, 88, "OpenAI-compatible API", "image edits endpoint", "UPSTREAM", "optional")

    canvas.connector(((140, 196), (140, 336)), "submit")
    canvas.connector(((360, 196), (360, 284), (152, 284), (152, 336)), "run")
    canvas.connector(((140, 432), (140, 492), (460, 492), (460, 548)), "generate", "accent")
    canvas.connector(((552, 592), (880, 592), (880, 104), (748, 104)), "image", "success", (688, 592))
    canvas.connector(((748, 180), (748, 268), (340, 268), (340, 336)), "store by sha1")
    canvas.connector(((296, 336), (296, 244), (360, 244), (360, 196)), "ref by id", "dashed")

    canvas.annotation(32, 688, "WORKFLOW FILES STORE REGISTRY IDS / NEVER FILE PATHS", 640)
    return canvas.render()