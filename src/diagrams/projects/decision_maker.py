"""Decision flow for AI-decision-maker."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "decision-maker",
        "AI-decision-maker signal chain",
        "A cache branch bypasses AI calls while misses use constrained AI signals followed by code validation and local execution.",
        height=520,
    )
    canvas.label(32, 32, "SIGNAL CHAIN / COLD PATH + CACHE BYPASS")

    canvas.connector(((176, 240), (192, 240)))
    canvas.connector(((256, 192), (256, 112), (384, 112)), "HIT / 0 TOKEN", "accent", (316, 96))
    canvas.connector(((256, 288), (256, 368), (328, 368)), "MISS", "default", (284, 352))
    canvas.connector(((544, 112), (672, 112), (672, 208)))
    canvas.connector(((472, 368), (504, 368)))
    canvas.connector(((648, 368), (680, 368)))
    canvas.connector(((752, 336), (752, 304), (672, 304), (672, 272)))
    canvas.connector(((752, 240), (792, 240)), style="accent")

    canvas.node(32, 208, 144, 64, "CSV profile", "fields + samples", "INPUT", "muted")
    canvas.decision(256, 240, 128, 96, "Fingerprint", "cached?", focal=True)
    canvas.node(384, 80, 160, 64, "Operation plan", "cached signals", "CODE")
    canvas.node(328, 336, 144, 64, "Scene code", "one code", "AI")
    canvas.node(504, 336, 144, 64, "Signal sequence", "one char / field", "AI")
    canvas.node(680, 336, 144, 64, "Validate signals", "whitelist + fallback", "CODE")
    canvas.node(592, 208, 160, 64, "Local execution", "registered operations", "CODE", "focal")
    canvas.node(792, 208, 136, 64, "Clean data", "deterministic", "OUTPUT", "success")

    canvas.annotation(40, 468, "AI proposes compact signals. Code validates and owns every write.", 560)
    return canvas.render()
