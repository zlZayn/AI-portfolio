"""Rule-generation architecture for AI-schema-mapper."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "schema-mapper",
        "AI-schema-mapper rule reuse architecture",
        "A large table contracts to its unique values, AI writes a reusable rule asset, and local code applies it to every row.",
        height=500,
    )
    canvas.label(32, 32, "COMPLEXITY SHIFTS FROM ROW COUNT TO UNIQUE VALUES")

    canvas.connector(((224, 228), (288, 228)), "DEDUPLICATE", "accent", (256, 212))
    canvas.connector(((440, 228), (504, 228)), "ONE AI READ", "accent", (472, 212))
    canvas.connector(((672, 228), (736, 228)), "APPLY TO ALL ROWS", "default", (704, 212))
    canvas.connector(((824, 264), (824, 348), (672, 348)), "RESIDUALS", "dashed", (756, 332))
    canvas.connector(((504, 380), (468, 380), (468, 264), (588, 264)), "OPTIONAL REFINE", "dashed", (416, 364))

    canvas.node(40, 176, 184, 104, "1,500,000 rows", "full dirty table", "DATA", "muted")
    canvas.node(288, 192, 152, 72, "UNIQUE VALUES", "about 100 patterns", "CODE", "focal")
    canvas.node(504, 176, 168, 104, "Reusable rules", "map + inference", "AI ASSET", "store")
    canvas.node(736, 192, 176, 72, "APPLY TO ALL ROWS", "local bulk replace", "CODE")
    canvas.node(504, 344, 168, 72, "Residual detector", "unmapped values only", "CODE", "optional")

    canvas.annotation(40, 456, "AI cost is O(unique values). Local execution absorbs row scale.", 520)
    return canvas.render()
