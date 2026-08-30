"""Dual-protocol architecture for AI-tool-calling."""

from ..svg import Canvas


def render() -> str:
    canvas = Canvas(
        "tool-calling",
        "AI-tool-calling dual-protocol architecture",
        "MCP and direct Function Calling adapters share one tool registry before handlers enter guarded execution paths.",
        height=520,
    )
    canvas.label(32, 32, "TWO PROTOCOLS / ONE TOOL DEFINITION")
    canvas.zone(32, 64, 352, 384, "Protocol adapters")
    canvas.zone(408, 64, 520, 384, "Shared runtime")
    canvas.zone(640, 284, 176, 148, "Guarded execution")

    canvas.connector(((176, 148), (240, 148)))
    canvas.connector(((176, 340), (240, 340)))
    canvas.connector(((368, 148), (400, 148), (400, 212), (440, 212)))
    canvas.connector(((368, 340), (408, 340), (408, 260), (440, 260)))
    canvas.connector(((616, 236), (664, 236), (664, 148)), style="accent")
    canvas.connector(((736, 188), (736, 320)), "CODE TOOLS", "default", (776, 252))
    canvas.connector(((812, 356), (876, 356), (876, 292)), style="default")
    canvas.connector(((808, 148), (876, 148), (876, 216)), "READ ONLY", "dashed", (848, 132))

    canvas.node(48, 112, 128, 72, "MCP host", "JSON-RPC", "CLIENT", "muted", fit=True)
    canvas.node(240, 112, 128, 72, "MCP adapter", "server tools", "PROTO", fit=True)
    canvas.node(48, 304, 128, 72, "Agent API", "tool_calls", "CLIENT", "muted", fit=True)
    canvas.node(240, 304, 128, 72, "FC adapter", "JSON schema", "PROTO", fit=True)
    canvas.node(440, 196, 176, 80, "ONE REGISTRY", "Zod definition once", "CORE", "focal", fit=True)
    canvas.node(664, 112, 144, 72, "Tool handlers", "9 atomic tools", "TOOLS", fit=True)
    canvas.node(660, 320, 152, 72, "Policy + timeout", "blocklist / 30s", "GUARD", fit=True)
    canvas.node(824, 216, 104, 72, "Result", "string", "OUTPUT", "success", fit=True)
    canvas.annotation(48, 484, "TWO PROTOCOLS change transport, not tool ownership.", 480)
    return canvas.render()
