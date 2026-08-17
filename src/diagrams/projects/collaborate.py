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
    canvas.node(64, 112, 144, 80, "User goal", "human intent", "INPUT", "muted")
    canvas.node(
        260,
        96,
        216,
        112,
        "Planner",
        "3 retries / schema checks",
        "LLM",
        "focal",
    )
    canvas.node(
        528,
        96,
        176,
        112,
        ("DYNAMIC PLAN", "S1 ... SN"),
        "agents 1 ... K",
        "JSON",
    )
    canvas.node(752, 112, 144, 80, "Dispatcher", "stage scheduler", "CODE")
    canvas.connector(((208, 152), (260, 152)), "intent", label_at=(232, 144))
    canvas.connector(((476, 152), (528, 152)), "validated", "accent", (504, 144))
    canvas.connector(((704, 152), (752, 152)))

    # Execution plane: stages are barriers; colleagues inside each stage are parallel.
    canvas.zone(32, 268, 896, 292, "EXECUTION PLANE")
    canvas.zone(52, 308, 264, 220, "STAGE 1 / PARALLEL")
    canvas.node(72, 348, 108, 80, "Agent 1", "independent role", "THREAD")
    canvas.node(188, 348, 108, 80, "Agent K", "independent role", "THREAD")
    canvas.node(104, 448, 160, 68, "Stage outputs", "successful only", "FILES", "store")
    canvas.connector(((124, 428), (124, 448)))
    canvas.connector(((244, 428), (244, 436), (184, 436), (184, 448)))

    canvas.node(
        372,
        336,
        216,
        116,
        ("FOCUSED", "BRIDGE"),
        "all prior success -> next stage",
        "CONTEXT",
        "focal",
    )
    canvas.node(
        372,
        468,
        216,
        68,
        "FAILURE ISOLATION",
        "partial: continue / all: stop",
        "CODE",
        "danger",
    )

    canvas.zone(644, 308, 264, 220, "STAGE N / PARALLEL")
    canvas.node(664, 348, 108, 80, "Agent 1", "bridged context", "THREAD")
    canvas.node(780, 348, 108, 80, "Agent M", "bridged context", "THREAD")
    canvas.node(696, 448, 160, 68, "Stage outputs", "successful only", "FILES", "store")
    canvas.connector(((720, 428), (720, 448)))
    canvas.connector(((836, 428), (836, 436), (776, 436), (776, 448)))

    canvas.connector(((824, 192), (824, 248), (184, 248), (184, 348)), "launch S1", label_at=(248, 248))
    canvas.connector(((264, 480), (332, 480), (332, 396), (372, 396)), "completed", "accent", (332, 456))
    canvas.connector(((588, 396), (620, 396), (620, 332), (720, 332), (720, 348)), style="accent")

    # Durable state makes the same engine observable and resumable from CLI or Web.
    canvas.zone(32, 604, 896, 156, "SYNTHESIS / STATE / INTERACTION")
    canvas.node(56, 644, 168, 80, "Summary", "all successful runs", "LLM", "success")
    canvas.node(272, 636, 208, 96, ("STATE.JSON", "+ OUTPUT FILES"), "plan / runs / bridges", "DURABLE", "store")
    canvas.node(528, 644, 168, 80, "Web / SSE", "live view / recovery", "OBSERVE")
    canvas.node(744, 644, 168, 80, "CONTINUE LOOP", "stored full context", "FOLLOW-UP")

    canvas.connector(((184, 516), (184, 576), (112, 576), (112, 644)))
    canvas.connector(((776, 516), (776, 584), (168, 584), (168, 644)), "all successful runs", label_at=(472, 584))
    canvas.connector(((224, 684), (272, 684)))
    canvas.connector(((480, 684), (528, 684)), "recover", label_at=(504, 676))
    canvas.connector(((696, 684), (744, 684)))
    canvas.connector(((828, 724), (828, 748), (376, 748), (376, 732)), "read + persist", "dashed", (604, 748))
    return canvas.render()
