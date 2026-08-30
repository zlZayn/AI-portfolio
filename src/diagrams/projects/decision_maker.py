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

    canvas.node(48, 232, 160, 80, "CSV profile", "fields + samples", "CODE", "muted", fit=True)
    canvas.decision(300, 272, 128, 104, "Fingerprint", "cached?", focal=True)

    canvas.node(376, 104, 168, 80, "Cached signals", "scene + field codes", "0 TOKEN", "store", fit=True)
    canvas.node(360, 376, 144, 80, "Scene code", "one constrained code", "AI", fit=True)
    canvas.node(536, 376, 144, 80, "Prompt router", "scene allowlist", "CODE", fit=True)
    canvas.node(712, 376, 160, 80, "Field signals", "one char / field", "AI", fit=True)

    canvas.node(
        536,
        216,
        184,
        104,
        ("VALIDATE", "+ ASSEMBLE"),
        "operation registry",
        "CODE",
        "focal",
        fit=True,
    )
    canvas.node(768, 216, 144, 80, "Local execute", "quality report", "CODE", fit=True)
    canvas.node(768, 96, 144, 72, "Clean data", "deterministic", "OUTPUT", "success", fit=True)

    canvas.connector(((208, 272), (208, 328), (236, 328), (236, 272)))
    canvas.connector(((300, 220), (300, 144), (376, 144)), "HIT / 0 TOKEN", "accent", (336, 136))
    canvas.connector(((300, 324), (300, 416), (360, 416)), "MISS", label_at=(328, 408))
    canvas.connector(((440, 456), (440, 492), (608, 492), (608, 456)))
    canvas.connector(((680, 416), (712, 416)))
    # Cached → VALIDATE：末段从下往上到 B=320（direction=UP，箭头向上进入 B face），保证箭头空腔在 BOX 下方（外部）
    canvas.connector(((544, 144), (628, 144), (628, 356), (628, 320)), style="accent")
    canvas.connector(((768, 264), (628, 264), (628, 356), (628, 320)))
    canvas.connector(((720, 268), (768, 268)), style="accent")
    canvas.connector(((840, 216), (840, 172)), style="success")
    canvas.annotation(48, 568, "Full rows never go to AI; invalid signals fall back before execution.", 640)
    return canvas.render()
