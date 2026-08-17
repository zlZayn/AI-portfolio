"""Schema-governed authoring and build architecture for raw-to-guide."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "raw-to-guide",
        "Raw research to offline guide schema architecture",
        "AI turns raw research into thirteen linked JSON datasets. One Schema contract governs validation and generation; valid data becomes lookup maps, bidirectional indexes, and a self-contained offline application.",
        height=620,
    )
    canvas.label(32, 32, "ONE SCHEMA GOVERNS AUTHORING, VALIDATION, AND GENERATION")
    canvas.zone(32, 64, 896, 240, "AUTHORING + VALIDATION")
    canvas.zone(32, 344, 896, 212, "BUILD + OFFLINE DELIVERY")

    canvas.node(48, 120, 144, 80, "Raw research", "notes + screenshots", "HUMAN", "muted")
    canvas.node(240, 120, 144, 80, "AI authoring", "normalize entities", "AI")
    canvas.node(432, 112, 160, 96, "13 JSON files", "IDs + typed refs", "DATA", "store")
    canvas.node(672, 112, 176, 96, "Reference validator", "integrity + symmetry", "CODE")
    canvas.node(432, 228, 160, 72, "SCHEMA CONTRACT", "entities + relations", "TRUST", "focal")

    canvas.node(264, 396, 192, 88, "Schema generator", "load + Jinja2 render", "CODE")
    canvas.node(520, 396, 176, 88, ("Maps + indexes", "+ backrefs"), "O(1) linked lookup", "BUILD", "store")
    canvas.node(760, 396, 152, 88, "OFFLINE H5", "23 routes / one file", "DELIVER", "success")

    canvas.connector(((192, 160), (240, 160)))
    canvas.connector(((384, 160), (432, 160)), style="accent")
    canvas.connector(((592, 160), (672, 160)))
    canvas.connector(((512, 228), (512, 216), (760, 216), (760, 208)), "VALIDATES", "accent", (640, 216))
    canvas.connector(((672, 128), (640, 128), (640, 88), (312, 88), (312, 120)), "FIX INVALID REFS", "dashed", (476, 88))
    canvas.connector(((760, 208), (760, 328), (360, 328), (360, 396)), "VALID DATA", "success", (560, 312))
    canvas.connector(((512, 300), (512, 360), (408, 360), (408, 396)), "DRIVES BUILD", "accent", (460, 344))
    canvas.connector(((456, 440), (520, 440)))
    canvas.connector(((696, 440), (760, 440)))
    canvas.annotation(48, 592, "AI output is provisional; only Schema-valid references reach the generator.", 680)
    return canvas.render()
