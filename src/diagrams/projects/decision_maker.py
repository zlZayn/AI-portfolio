"""Cache-aware decision architecture for AI-decision-maker."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "decision-maker",
        "AI-decision-maker cache-aware signal architecture",
        "A deterministic profile and fingerprint either reuse cached semantic signals or request two constrained AI codes. Code validates, assembles registered operations, and executes every data write locally.",
        height=600,
    )
    canvas.label(32, 32, "AI PROPOSES COMPACT SIGNALS / CODE OWNS EVERY WRITE")
    canvas.zone(32, 64, 896, 472, "DETERMINISTIC PIPELINE WITH CONSTRAINED AI")

    canvas.node(48, 232, 160, 80, "CSV profile", "fields + samples", "CODE", "muted")
    canvas.decision(280, 272, 128, 104, "Fingerprint", "cached?", focal=True)

    canvas.node(376, 104, 168, 80, "Cached signals", "scene + field codes", "0 TOKEN", "store")
    canvas.node(360, 376, 144, 80, "Scene code", "one constrained code", "AI")
    canvas.node(536, 376, 144, 80, "Prompt router", "scene allowlist", "CODE")
    canvas.node(712, 376, 160, 80, "Field signals", "one char / field", "AI")

    canvas.node(
        536,
        216,
        184,
        104,
        ("VALIDATE", "+ ASSEMBLE"),
        "operation registry",
        "CODE",
        "focal",
    )
    canvas.node(768, 216, 144, 80, "Local execute", "quality report", "CODE")
    canvas.node(768, 96, 144, 72, "Clean data", "deterministic", "OUTPUT", "success")

    canvas.connector(((208, 272), (216, 272)))
    canvas.connector(((280, 220), (280, 144), (376, 144)), "HIT / 0 TOKEN", "accent", (312, 128))
    canvas.connector(((280, 324), (280, 416), (360, 416)), "MISS", label_at=(312, 400))
    canvas.connector(((504, 416), (536, 416)))
    canvas.connector(((680, 416), (712, 416)))
    canvas.connector(((544, 144), (628, 144), (628, 216)), style="accent")
    canvas.connector(((792, 376), (792, 344), (628, 344), (628, 320)))
    canvas.connector(((720, 268), (768, 268)), style="accent")
    canvas.connector(((840, 216), (840, 168)), style="success")
    canvas.annotation(48, 568, "Full rows never go to AI; invalid signals fall back before execution.", 640)
    return canvas.render()
