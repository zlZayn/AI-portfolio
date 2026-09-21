"""Three escalating decision engines behind one code-owned gate."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "decision-maker",
        "AI-decision-maker three-engine routing",
        "A deterministic profile and fingerprint either reuse cached signals at zero token cost or escalate a judgement through three engines: local lookup, a probability engine, and a generative model. Code gates every confidence and owns every write.",
        height=640,
    )
    canvas.label(32, 32, "AI PROPOSES SIGNALS / CODE OWNS EVERY WRITE")
    canvas.zone(32, 64, 896, 536, "THREE ESCALATING ENGINES, ONE CODE-OWNED GATE")

    canvas.node(48, 288, 128, 80, "CSV profile", "fields + samples", "CODE", "muted")
    canvas.decision(264, 328, 128, 104, "Fingerprint", "cached?")

    canvas.node(400, 104, 208, 80, "Cached signals", "scene + field codes", "0 TOKEN", "store")

    canvas.node(400, 232, 208, 72, "System 0", "local lookup · 0 TOKEN", "CODE", "muted")
    canvas.node(400, 352, 208, 72, "System 1 · Jev", "probability, not text", "AI")
    canvas.node(400, 472, 208, 72, "System 2 · LLM", "generated text", "AI")

    canvas.decision(736, 388, 144, 104, "Gate", "CODE", focal=True)

    canvas.node(648, 224, 176, 88, ("VALIDATE", "+ ASSEMBLE"), "operation registry", "CODE")
    canvas.node(656, 104, 160, 72, "Local execute", "quality report", "CODE")
    canvas.node(832, 104, 96, 72, "Clean data", "deterministic", "OUTPUT", "success")

    canvas.connector(((176, 328), (200, 328)))
    canvas.connector(((264, 276), (264, 144), (400, 144)), "HIT / 0 TOKEN", "accent", (332, 128))
    canvas.connector(((328, 328), (364, 328), (364, 268), (400, 268)), "MISS", label_at=(344, 252))
    canvas.connector(((504, 304), (504, 352)))
    canvas.connector(((608, 388), (664, 388)))
    canvas.connector(((736, 336), (736, 312)), "accept", "success", (768, 328))
    canvas.connector(((736, 440), (736, 508), (608, 508)), "escalate", "accent", (700, 492))
    canvas.connector(((504, 544), (504, 576), (856, 576), (856, 268), (824, 268)))
    canvas.connector(((736, 224), (736, 176)), style="success")
    canvas.connector(((816, 140), (832, 140)), style="success")
    canvas.connector(((608, 144), (616, 144), (616, 268), (648, 268)))

    canvas.annotation(
        48,
        616,
        "Jev returns probabilities, not text — invalid codes are unrepresentable. "
        "Measured: 1.9–3.5× DeepSeek's cost.",
        800,
    )
    return canvas.render()
