"""
Mermaid diagram definitions for all 6 AI projects.
Renders .mmd files to SVG using mmdc (Mermaid CLI).

Design system — matches portfolio warm theme:
  input   warm-cream  / gray border   (#faf6ef / #d1d5db)
  proc    warm-orange / orange border  (#fff7ed / #f97316)
  ai      light-purple/ indigo border  (#f5f3ff / #6366f1)
  dec     warm-amber   / amber border   (#fef3c7 / #d97706)
  ok      light-green  / green border   (#f0fdf4 / #16a34a)
  stop    light-red    / red border     (#fef2f2 / #dc2626)
"""

import subprocess
import tempfile
import os
from pathlib import Path

PUPPETEER_CONFIG = Path(__file__).parent / "puppeteer-config.json"
MMDC_CMD = "mmdc.cmd"


def _puppeteer_flag() -> list[str]:
    if PUPPETEER_CONFIG.exists():
        return ["-p", str(PUPPETEER_CONFIG)]
    return []


_HEAD = """%%{init: {"flowchart": {"htmlLabels": true, "curve": "linear"}}}%%
flowchart LR
  classDef input fill:#faf6ef,stroke:#d1d5db,stroke-width:2px,color:#2d2b55,font-size:14px
  classDef proc fill:#fff7ed,stroke:#f97316,stroke-width:2px,color:#7c2d12,font-size:14px
  classDef ai fill:#f5f3ff,stroke:#6366f1,stroke-width:2px,color:#3b0764,font-size:14px
  classDef dec fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#7c2d12,font-size:14px
  classDef ok fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-size:14px
  classDef stop fill:#fef2f2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d,font-size:14px
"""


def decision_maker() -> str:
    return _HEAD + """
    A[CSV Input]:::input --> B[Profile<br/>fingerprint]:::proc
    B --> C{Cache?}:::dec
    C -->|Hit| H[Execute<br/>Stages 4-5]:::ok
    H --> I[Clean Output]:::input
    C -->|Miss| D[Scene AI<br/>1 char code]:::ai
    D --> E[Route<br/>assemble prompt]:::proc
    E --> F[Field AI<br/>signal sequence]:::ai
    F --> G[Assemble<br/>operation chain]:::proc
    G --> H
"""


def rag_embed() -> str:
    return _HEAD + """
    subgraph BLD["Build Phase"]
        direction LR
        D1[Documents]:::proc --> D2[Chunk<br/>smart boundaries]:::proc
        D2 --> D3[Embed]:::ai
        D3 --> D4[(Vector DB)]:::ok
    end
    subgraph QRY["Query Phase"]
        direction LR
        Q1[Question]:::input --> Q2{Enhance?}:::ai
        Q2 -->|rewritten| Q3[Retrieve<br/>Hybrid + RRF]:::proc
        Q3 --> Q4[Answer LLM]:::ai
        Q1 -.->|original| Q4
    end
    D4 --> Q3
"""


def schema_mapper() -> str:
    return _HEAD + """
    A[Dirty CSV<br/>rows]:::input --> B[Extract<br/>unique values]:::proc
    B --> C{AI Rule Gen<br/>1-2 calls}:::ai
    C --> D[""" + '"' + r"""JSON Rules"""+ '"' + """]:::ok
    A --> E[Local Exec<br/>0 tokens]:::ok
    D --> E
    E --> F[Polish]:::proc --> G[Clean CSV]:::input
"""


def tool_calling() -> str:
    return _HEAD + """
    subgraph TC["Direct Mode"]
        direction LR
        U[User]:::input --> A[Agent<br/>streaming loop]:::proc
        A --> L[OpenAI API]:::ai
        L --> T1[Execute Tool]:::ok
    end
    subgraph MP["MCP Mode"]
        direction LR
        MC[MCP Client]:::input --> MS[MCP Server<br/>stdio]:::proc
        MS --> T2[Use Tool]:::ok
    end
    Shared[[registerTool<br/>one codebase]]:::proc
    T1 -.-> Shared
    T2 -.-> Shared
"""


def collaborate() -> str:
    return _HEAD + """
    Goal[Goal]:::input --> Plan[Plan<br/>LLM Planner]:::ai
    Plan --> D["Dispatch<br/>N Agents / Stage<br/>(parallel)"]:::ai
    D --> B[Bridge<br/>summarize]:::ok
    B --> S[Synthesize<br/>final answer]:::ai
    S --> C[Continue<br/>follow-up]:::proc
    C -.->|loop| Plan
"""


def tier_guardian() -> str:
    return _HEAD + """
    T[Input Text]:::input --> L1["Layer 1<br/>A + B parallel"]:::ai
    L1 --> G1{pre_filter<br/>0 tokens}:::dec
    G1 -->|PASS ≈90%| PASS[PASS]:::ok
    G1 -->|escalate| L2["Layer 2<br/>C context judge"]:::ai
    L2 --> G2{deep_judge<br/>0 tokens}:::dec
    G2 -->|PASS| PASS
    G2 -->|BLOCK| BLK[BLOCK]:::stop
    G2 -->|REVIEW| L3["Layer 3<br/>D evidence"]:::ai
    L3 --> HR[Human Review]:::dec
"""


DIAGRAMS = {
    "decision-maker": decision_maker,
    "rag-embed": rag_embed,
    "schema-mapper": schema_mapper,
    "tool-calling": tool_calling,
    "collaborate": collaborate,
    "tier-guardian": tier_guardian,
}


def render_mermaid(mmd_text: str) -> str:
    """Write Mermaid text to temp file, render with mmdc, return SVG string."""
    tmp_dir = Path(tempfile.mkdtemp())
    mmd_file = tmp_dir / "diagram.mmd"
    svg_file = tmp_dir / "diagram.svg"
    mmd_file.write_text(mmd_text, encoding="utf-8")

    cmd = [
        MMDC_CMD,
        "-i", str(mmd_file),
        "-o", str(svg_file),
        "-b", "transparent",
        "--width", "900",
        "--height", "240",
    ] + _puppeteer_flag()

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"  mmdc error: {result.stderr.strip()}")
        return f"<!-- mmdc failed: {result.stderr.strip()} -->"

    svg = svg_file.read_text(encoding="utf-8")

    # Post-process: match SVG font to web page system font
    svg = svg.replace(
        'font-family:"trebuchet ms",verdana,arial,sans-serif',
        'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif',
    )

    for f in [mmd_file, svg_file]:
        f.unlink(missing_ok=True)
    tmp_dir.rmdir()

    return svg


def render_all() -> dict[str, str]:
    """Render all 6 Mermaid diagrams, return {project_id: svg_string}."""
    result = {}
    for pid, fn in DIAGRAMS.items():
        mmd = fn()
        svg = render_mermaid(mmd)
        result[pid] = svg
        print(f"  [{pid}] diagram rendered ({len(svg)} bytes)")
    return result


if __name__ == "__main__":
    from pathlib import Path
    os.chdir(Path(__file__).parent)
    svgs = render_all()
    for pid, svg in svgs.items():
        out = Path("output") / f"{pid}.svg"
        out.write_text(svg, encoding="utf-8")
        print(f"  saved {out}")
