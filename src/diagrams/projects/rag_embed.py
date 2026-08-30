"""Build and query architecture for AI-RAG-embed."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "rag-embed",
        "AI-RAG-embed build and query architecture",
        "Semantic chunks feed a hybrid index while enhanced and original questions follow deliberately separate paths.",
        height=560,
    )
    canvas.label(32, 32, "TWO BOUNDARIES / HOW TO CHUNK + HOW TO ASK")
    canvas.zone(32, 64, 896, 176, "Build boundary")
    canvas.zone(32, 272, 896, 240, "Query boundary")

    canvas.connector(((224, 148), (288, 148)))
    canvas.connector(((456, 148), (560, 148)), style="accent")
    canvas.connector(((224, 388), (280, 388), (280, 340)))
    canvas.connector(
        ((440, 340), (440, 272), (536, 272), (536, 304)),
        "ENHANCED QUERY",
        "accent",
        (488, 292),
    )
    canvas.connector(((656, 188), (656, 260), (572, 260), (572, 304)), "HYBRID INDEX", "default", (612, 244))
    canvas.connector(((656, 340), (704, 340)))
    canvas.connector(((784, 380), (784, 416)))
    canvas.connector(((144, 428), (144, 456), (704, 456)), "ORIGINAL QUESTION", "dashed", (424, 440))

    canvas.node(64, 112, 160, 72, "Documents", ".md / .txt / .typ", "SOURCE", "muted", fit=True)
    canvas.node(288, 112, 160, 72, "Semantic chunker", "headings keep meaning", "CODE", "focal", fit=True)
    canvas.node(560, 112, 192, 72, "Hybrid index", "vector + BM25", "STORE", "store", fit=True)
    canvas.node(64, 352, 160, 72, "Question", "conversation-aware", "INPUT", "muted", fit=True)
    canvas.node(280, 304, 160, 72, "Query enhancer", "retrieval wording", "AI", "focal", fit=True)
    canvas.node(488, 304, 168, 72, "Retrieve + RRF", "rank fusion", "CODE", fit=True)
    canvas.node(704, 304, 160, 72, "Cross-encoder", "optional rerank", "AI", "optional", fit=True)
    canvas.node(704, 416, 160, 72, "Answer LLM", "sees original question", "AI", fit=True)
    return canvas.render()
