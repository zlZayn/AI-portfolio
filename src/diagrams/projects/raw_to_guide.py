"""Role-scoped data flow for ai-batch-raw-to-offline-guide."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "raw-to-guide",
        "Raw research to offline guide data flow",
        "Authors, AI, the build system, and readers exchange increasingly structured artifacts governed by one Schema contract.",
        height=520,
    )
    canvas.label(32, 32, "ONE CONTRACT / FOUR OWNERS / FIVE DATA SHAPES")
    for index, (label, y) in enumerate(
        (("AUTHOR", 96), ("AI", 184), ("BUILD SYSTEM", 272), ("READER", 360))
    ):
        canvas.lane(32, y, 896, 88, label, tinted=index % 2 == 0)

    steps = ((240, "01", "COLLECT"), (384, "02", "ORGANIZE"), (528, "03", "CONTRACT"),
             (672, "04", "BUILD"), (816, "05", "USE"))
    for x, number, label in steps:
        canvas.step_header(x, 56, number, label, focal=number == "03")

    canvas.connector(((296, 136), (384, 136), (384, 192)))
    canvas.connector(((440, 224), (528, 224), (528, 280)), style="accent")
    canvas.connector(((584, 316), (616, 316)), style="accent")
    canvas.connector(((728, 316), (816, 316), (816, 368)))

    canvas.node(184, 104, 112, 64, "Raw sources", "notes + screenshots", "FILES", "muted")
    canvas.node(328, 192, 112, 64, "Markdown", "deduped topics", "AI / FL")
    canvas.node(472, 280, 112, 72, "SCHEMA CONTRACT", "JSON + ID refs", "AI / JSON", "focal")
    canvas.node(616, 280, 112, 72, "Indexes + SPA", "Jinja2 build", "CODE / TB")
    canvas.node(760, 368, 112, 64, "OFFLINE H5", "23 routes", "WEB", "success")
    canvas.annotation(40, 488, "Schema constrains AI output and defines what the generator may consume.", 680)
    return canvas.render()
