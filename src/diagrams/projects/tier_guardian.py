"""Layered arbitration flow for AI-tier-guardian."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "tier-guardian",
        "AI-tier-guardian layered arbitration",
        "Parallel shallow reviewers feed two zero-token code gates that release, block, or escalate content to human review.",
        height=640,
    )
    canvas.label(32, 32, "THREE LAYERS / TWO CODE-OWNED GATES")
    canvas.zone(152, 64, 232, 344, "Layer 1 / parallel")

    canvas.connector(((112, 220), (136, 220), (136, 132), (176, 132)))
    canvas.connector(((112, 236), (148, 236), (148, 340), (176, 340)))
    canvas.connector(((352, 132), (400, 132), (400, 220), (448, 220)))
    canvas.connector(((352, 340), (412, 340), (412, 284), (448, 284)))
    canvas.connector(((480, 196), (480, 108), (736, 108)), "PASS", "success", (624, 92))
    canvas.connector(((560, 252), (664, 252)), "ESCALATE", "accent", (612, 236))
    canvas.connector(((752, 288), (752, 332), (640, 332), (640, 364)))
    canvas.connector(((552, 420), (400, 420), (400, 572), (360, 572)), "PASS", "success", (472, 404))
    canvas.connector(((640, 476), (640, 536)), "BLOCK", "danger", (684, 520))
    canvas.connector(((728, 420), (828, 420), (828, 536)), "REVIEW", "default", (780, 404))

    canvas.label(32, 224, "INPUT TEXT", "eyebrow")
    canvas.node(176, 96, 176, 72, "Surface scanner", "patterns + risk", "AI", fit=True)
    canvas.node(176, 304, 176, 72, "Intent probe", "intent + confidence", "AI", fit=True)
    canvas.decision(480, 252, 160, 112, ("pre_filter", "CODE ARBITRATION"), "0 TOKEN", focal=True)
    canvas.node(736, 72, 160, 72, "Fast release", "shallow certainty", "PASS", "success", fit=True)
    canvas.node(664, 216, 176, 72, "Context judge", "culture + severity", "AI", fit=True)
    canvas.decision(640, 420, 176, 112, ("deep_judge", "CODE ARBITRATION"), "0 TOKEN", focal=True)
    canvas.node(216, 536, 144, 72, "Release", "low residual risk", "PASS", "success", fit=True)
    canvas.node(568, 536, 144, 72, "Auto block", "high confidence", "BLOCK", "danger", fit=True)
    canvas.node(744, 536, 168, 72, "Evidence to human", "D summarizes only", "REVIEW", fit=True)
    return canvas.render()
