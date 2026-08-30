"""Adaptive orchestration architecture for AI-collaborate."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "collaborate",
        "AI-collaborate adaptive multi-agent orchestration",
        "A validated dynamic plan drives sequential stages with parallel colleagues. "
        "Focused bridge summaries, failure isolation, durable state, synthesis, and "
        "follow-up interaction form the complete orchestration loop.",
        height=800,
        typography="expanded",
    )
    canvas.label(32, 32, "ADAPTIVE ORCHESTRATION / VARIABLE DEPTH AND WIDTH")

    # Control plane: the model chooses topology; code validates and schedules it.
    canvas.zone(32, 64, 896, 168, "CONTROL PLANE")
    canvas.node(64, 112, 144, 80, "User goal", "human intent", "INPUT", "muted", fit=True)
    canvas.node(
        260,
        96,
        216,
        112,
        "Planner",
        "3 retries / schema checks",
        "LLM",
        "focal",
        fit=True,
    )
    canvas.node(
        528,
        96,
        176,
        112,
        ("DYNAMIC PLAN", "S1 ... SN"),
        "agents 1 ... K",
        "JSON",
        fit=True,
    )
    canvas.node(752, 112, 144, 80, "Dispatcher", "stage scheduler", "CODE", fit=True)
    canvas.connector(((208, 152), (260, 152)), "intent", label_at=(232, 144))
    canvas.connector(((476, 152), (528, 152)), "validated", "accent", (504, 144))
    canvas.connector(((704, 152), (752, 152)))

    # Execution plane: stages are barriers; colleagues inside each stage are parallel.
    canvas.zone(32, 268, 896, 292, "EXECUTION PLANE")
    canvas.zone(52, 308, 312, 220, "STAGE 1 / PARALLEL")
    canvas.node(68, 340, 136, 80, "Agent 1", "independent role", "THREAD", fit=True)
    canvas.node(216, 340, 136, 80, "Agent K", "independent role", "THREAD", fit=True)
    canvas.node(104, 456, 160, 68, "Stage outputs", "successful only", "FILES", "store", fit=True)
    canvas.connector(((136, 420), (136, 456)))
    canvas.connector(((300, 420), (300, 480), (264, 480)))

    canvas.node(
        384,
        336,
        228,
        116,
        ("FOCUSED", "BRIDGE"),
        "all prior success -> next stage",
        "CONTEXT",
        "focal",
        fit=True,
    )
    canvas.node(
        384,
        468,
        216,
        68,
        "FAILURE ISOLATION",
        "partial: continue / all: stop",
        "CODE",
        "danger",
        fit=True,
    )

    canvas.zone(624, 308, 304, 220, "STAGE N / PARALLEL")
    canvas.node(648, 340, 128, 80, "Agent 1", "bridged context", "THREAD", fit=True)
    canvas.node(792, 340, 128, 80, "Agent M", "bridged context", "THREAD", fit=True)
    canvas.node(704, 456, 160, 68, "Stage outputs", "successful only", "FILES", "store", fit=True)
    canvas.connector(((712, 420), (712, 456)))
    canvas.connector(((856, 420), (856, 456)))

    canvas.connector(((824, 192), (824, 248), (184, 248), (184, 340)), "launch S1", label_at=(248, 248))
    canvas.connector(((264, 480), (348, 480), (348, 452), (384, 452)), "completed", "accent", (312, 472))
    canvas.connector(((612, 396), (648, 396)), style="accent")

    # Durable state makes the same engine observable and resumable from CLI or Web.
    canvas.zone(32, 604, 896, 156, "SYNTHESIS / STATE / INTERACTION")
    canvas.node(56, 644, 168, 80, "Summary", "all successful runs", "LLM", "success", fit=True)
    canvas.node(272, 636, 208, 96, ("STATE.JSON", "+ OUTPUT FILES"), "plan / runs / bridges", "DURABLE", "store", fit=True)
    canvas.node(528, 644, 168, 80, "Web / SSE", "live view / recovery", "OBSERVE", fit=True)
    canvas.node(744, 644, 168, 80, "CONTINUE LOOP", "stored full context", "FOLLOW-UP", fit=True)

    canvas.connector(((184, 540), (184, 576), (112, 576), (112, 644)))
    canvas.connector(((776, 540), (776, 584), (168, 584), (168, 644)), "all successful runs", label_at=(472, 584))
    canvas.connector(((224, 684), (272, 684)))
    canvas.connector(((480, 684), (528, 684)), "recover", label_at=(504, 676))
    canvas.connector(((696, 684), (744, 684)))
    canvas.connector(((828, 644), (828, 600), (380, 600), (380, 636)), "read + persist", "dashed", (604, 596))
    return canvas.render()
