"""Rule-authoring and local-execution architecture for AI-schema-mapper."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "schema-mapper",
        "AI-schema-mapper rule authoring and local execution",
        "Only unique values reach AI to create a reusable rule asset. The untouched full table follows a local execution path through mapping, cross-field inference, final polishing, schema validation, and quality reporting.",
        height=620,
    )
    canvas.label(32, 32, "AI UNDERSTANDS PATTERNS ONCE / CODE EXECUTES N ROWS")
    canvas.zone(32, 64, 896, 216, "RULE AUTHORING / SMALL DATA")
    canvas.zone(32, 320, 896, 236, "LOCAL EXECUTION / FULL DATA")

    canvas.node(56, 128, 160, 80, "Dirty table", "1,500,000 rows", "SOURCE", "muted")
    canvas.node(288, 112, 168, 112, "UNIQUE VALUES", "about 100 patterns", "DEDUP", "focal")
    canvas.node(528, 112, 168, 112, "Rule generator", "mapping + inference", "AI")
    canvas.node(768, 128, 144, 80, "RULE ASSET", "auto_rules.json", "REUSE", "store")

    canvas.node(264, 372, 168, 88, "Local mapper", "lookup over all rows", "CODE")
    canvas.node(488, 372, 176, 88, ("Inference", "+ final polish"), "deterministic rules", "CODE")
    canvas.node(720, 372, 176, 88, "Schema check", "completeness + types", "CODE")
    canvas.node(608, 492, 136, 64, "Clean CSV", "final data", "OUTPUT", "success")
    canvas.node(776, 492, 136, 64, "Quality report", "compliance", "REPORT", "store")

    canvas.connector(((216, 168), (288, 168)), "DEDUP", "accent", (252, 152))
    canvas.connector(((456, 168), (528, 168)), "ONE AI READ", "accent", (492, 96))
    canvas.connector(((696, 168), (768, 168)))
    canvas.connector(((136, 208), (136, 348), (348, 348), (348, 372)), "FULL ROWS BYPASS AI", "dashed", (220, 304))
    canvas.connector(((840, 208), (840, 304), (400, 304), (400, 372)), "REUSABLE RULES", "accent", (620, 288))
    canvas.connector(((432, 416), (488, 416)))
    canvas.connector(((664, 416), (720, 416)))
    canvas.connector(((808, 460), (808, 476), (676, 476), (676, 492)), style="success")
    canvas.connector(((840, 460), (840, 492)))
    canvas.connector(((896, 400), (920, 400), (920, 256), (612, 256), (612, 224)), "OPTIONAL REFINE", "dashed", (792, 240))
    canvas.annotation(48, 592, "Token cost follows unique values; row scale stays entirely local.", 600)
    return canvas.render()
