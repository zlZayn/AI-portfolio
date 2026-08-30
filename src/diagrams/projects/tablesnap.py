"""Shared visual-understanding core for tablesnap."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "tablesnap",
        "tablesnap direct visual table extraction",
        "Hotkey captures and batch images converge on one local visual-language-model call and a shared XLSX exporter.",
        height=460,
    )
    canvas.label(32, 32, "TWO INPUT MODES / ONE VISUAL CORE")
    canvas.zone(320, 112, 608, 240, "Local processing boundary")

    canvas.connector(((224, 164), (280, 164), (280, 208), (368, 208)))
    canvas.connector(((224, 324), (296, 324), (296, 256), (368, 256)))
    canvas.connector(((560, 232), (624, 232)), style="accent")
    canvas.connector(((768, 232), (816, 232)))

    canvas.node(48, 128, 176, 72, "Hotkey capture", "drag screen region", "GUI", "muted", fit=True)
    canvas.node(48, 288, 176, 72, "Batch images", "PNG / JPG / WEBP", "FILES", "muted", fit=True)
    canvas.node(368, 192, 192, 80, "ONE VLM CALL", "Qwen3-VL via Ollama", "LOCAL AI", "focal", fit=True)
    canvas.node(624, 196, 144, 72, "PSV rows", "pipe-separated", "TEXT", "store", fit=True)
    canvas.node(816, 196, 112, 72, "XLSX", "openpyxl", "OUTPUT", "success", fit=True)
    canvas.annotation(360, 400, "NO OCR PIPELINE / NO LAYOUT RECONSTRUCTION", 520)
    return canvas.render()
