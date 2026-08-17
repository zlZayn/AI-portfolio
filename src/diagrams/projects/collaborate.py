"""Role-scoped process for AI-collaborate."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "collaborate",
        "AI-collaborate staged multi-agent process",
        "A planner defines sequential stages, agents execute in parallel inside each stage, and bridge summaries carry focused context forward.",
        height=580,
    )
    canvas.label(32, 32, "SEQUENTIAL STAGES / PARALLEL COLLEAGUES")
    for index, (label, y) in enumerate(
        (("USER", 96), ("PLANNER", 176), ("AGENT POOL", 256), ("BRIDGE", 336), ("SUMMARIZER", 416))
    ):
        canvas.lane(32, y, 896, 80, label, tinted=index % 2 == 0)

    steps = ((216, "01", "GOAL"), (344, "02", "PLAN"), (472, "03", "STAGE 1"),
             (600, "04", "BRIDGE"), (728, "05", "STAGE N"), (856, "06", "DELIVER"))
    for x, number, label in steps:
        canvas.step_header(x, 56, number, label, focal=number == "04")

    canvas.connector(((272, 136), (344, 136), (344, 184)))
    canvas.connector(((400, 216), (472, 216), (472, 264)))
    canvas.connector(((536, 296), (600, 296), (600, 344)), style="accent")
    canvas.connector(((656, 376), (728, 376), (728, 328)), style="accent")
    canvas.connector(((792, 296), (856, 296), (856, 424)))

    canvas.node(160, 104, 112, 64, "Goal", "human intent", "INPUT", "muted")
    canvas.node(288, 184, 112, 64, "Plan JSON", "N stages", "PLANNER")
    canvas.node(408, 264, 128, 64, ("Agent xK", "PARALLEL WITHIN"), "stage outputs", "POOL")
    canvas.node(544, 344, 112, 64, "BRIDGE CONTEXT", "focused handoff", "AI", "focal")
    canvas.node(664, 264, 128, 64, ("Agent xM", "PARALLEL WITHIN"), "next outputs", "POOL")
    canvas.node(800, 424, 112, 64, "Final answer", "synthesized", "SUMMARY", "success")
    canvas.annotation(40, 544, "Stages wait for context. Colleagues inside a stage do not wait for each other.", 720)
    return canvas.render()
