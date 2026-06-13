"""
Mermaid diagram definitions for all 6 AI projects.
Renders .mmd files to SVG using mmdc (Mermaid CLI).

Color semantics (matching portfolio warm theme):
  input  External Interface       (#faf6ef / #d1d5db)
  proc   Runtime / Orchestration  (#fff7ed / #f97316)
  ai     Reasoning / Agent / KE   (#f5f3ff / #6366f1)
  dec    Router / Decision        (#fef3c7 / #d97706)
  ok     Result / Cache Hit       (#f0fdf4 / #16a34a)
  stop   Block / Halt             (#fef2f2 / #dc2626)
"""

import subprocess
import tempfile
import os
from pathlib import Path

PUPPETEER_CONFIG = Path(__file__).resolve().parent.parent / "config" / "puppeteer.json"
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
    return (
        _HEAD
        + """
    subgraph EXT["External Interface"]
        A[CSV Input]:::input
    end
    subgraph GOV["Runtime Governance"]
        B[Cache Router<br/>MD5 Fingerprint]:::dec
    end
    subgraph REA["Reasoning Layer"]
        C[Field Type<br/>Structured Output]:::ai
        D[Scene & Signal<br/>Code Classification]:::ai
    end
    subgraph ORC["Orchestration Logic"]
        E[Operation Chain<br/>Dispatch & Exec]:::proc
    end
    subgraph GOV2["Runtime Governance"]
        F[3-layer Code<br/>Validator]:::proc
    end

    A --> B
    B -->|Miss| C
    C --> D
    D --> E
    E --> F
    F --> G[Clean Output]:::ok
    B -->|Hit| G
"""
    )


def rag_embed() -> str:
    return (
        _HEAD
        + """
    subgraph BLD["Build Phase"]
        direction LR
        D1[Documents<br/>.txt / .md / .typ]:::proc --> D2[Smart Chunk<br/>Boundary Aware]:::proc
        D2 --> D3[Embedding<br/>Vector Index]:::ai
        D2 -.-> B25[BM25 Index<br/>jieba + rank-bm25]:::proc
        D3 --> D4[(Vector DB<br/>Long-Term Memory)]:::ok
    end
    subgraph PROTO["Protocol Layer"]
        MCP[MCP Server<br/>stdio transport]:::ai
    end
    subgraph QRY["Query Phase"]
        direction LR
        Q1[Question]:::input --> EN{Query<br/>Enhancer}:::dec
        EN -->|enhanced| RET[Hybrid Retrieval<br/>Vector + BM25<br/>RRF Fusion]:::proc
        EN -.->|original| LLM
        RET --> RR[Cross-Encoder<br/>Reranker]:::ai
        RR --> LLM[Answer Gen<br/>Remote LLM]:::ai
        LLM --> Q2[Answer]:::ok
    end
    D4 --> RET
    B25 --> RET
    MCP -.-> Q1
"""
    )


def schema_mapper() -> str:
    return (
        _HEAD
        + """
    subgraph EXT["External Interface"]
        A[Dirty CSV]:::input
    end
    subgraph TK["Core: Tool Ecosystem"]
        B[Unique Value<br/>Extractor]:::proc
        C[Atomic Tool<br/>AI Rule Gen]:::ai
    end
    subgraph ORC["Orchestration Logic"]
        D[Priority Mapping<br/>4-level Fallback]:::proc
    end
    subgraph RUNT["Runtime Base"]
        E[Bulk Replace<br/>Local Exec Engine]:::proc
    end

    A --> B
    B --> C
    C -->|JSON Rules| D
    D --> E
    A -.->|Raw bypass| E
    E --> F[Clean CSV]:::ok
"""
    )


def tool_calling() -> str:
    return (
        _HEAD
        + """
    subgraph AGE["Agent Entity"]
        U[Host: Claude Code<br/>Codex Desktop]:::input
    end
    subgraph PROTO["Protocol Layer"]
        direction LR
        MCP[MCP: JSON-RPC<br/>Tool Discovery]:::proc
        FC[Function Calling<br/>Direct API]:::proc
    end
    subgraph TK["Core: Tool Ecosystem"]
        REG[Atomic Tool<br/>Registry]:::ai
    end
    subgraph RUNT["Runtime Base"]
        S[Sandbox Exec<br/>30s Timeout]:::proc
        V[Dangerous Cmd<br/>Blocklist]:::stop
    end

    U --> MCP & FC
    MCP --> REG
    FC --> REG
    REG --> S
    S --> V
    V --> OUT[Tool Result]:::ok
"""
    )


def collaborate() -> str:
    return (
        _HEAD
        + """
    subgraph PLAN["Planning (Autonomous)"]
        direction LR
        G[User Goal]:::input
        P[Planner LLM]:::ai
        D{Decides<br/>N Stages, M Agents}:::dec
        C[Agent Config<br/>Role / Model / Prompt]:::ok
        V[JSON Schema<br/>x3 Retries]:::proc
    end

    subgraph EXEC["Execution (Sequential Pipeline)"]
        direction LR
        S1[Stage 1<br/>K Agents Parallel]:::proc
        B1[Bridge<br/>Context]:::ai
        S2[Stage 2<br/>M Agents Parallel]:::proc
        SN[.. N Stages<br/>Sequential]:::proc
    end

    SM[Final<br/>Summarizer]:::ai
    CT[Continue<br/>Follow-up]:::proc
    OUT[Answer]:::ok

    G --> P --> D --> C --> V
    V --> S1 --> B1 --> S2 --> SN --> SM --> CT --> OUT
"""
    )


def tier_guardian() -> str:
    return (
        _HEAD
        + """
    T[Input Text<br/>scene + locale]:::input

    subgraph L1["Layer 1 - Parallel"]
        direction LR
        A[Surface Scanner<br/>Pattern + Risk]:::ai
        B[Intent Probe<br/>Intent + Confidence]:::ai
    end

    PF{pre_filter<br/>0 token<br/>Pure Python}:::dec

    subgraph L2["Layer 2 - Sequential"]
        C[Context Judge<br/>CoT + Culture<br/>Thinking ON]:::ai
    end

    DJ{deep_judge<br/>0 token<br/>Pure Python}:::dec

    subgraph L3["Layer 3 - On Demand"]
        D[Evidence<br/>Summarizer<br/>Thinking OFF]:::ai
    end

    PASS[PASS<br/>Fast Release]:::ok
    BLK[BLOCK<br/>Auto Block]:::stop
    HR[Human<br/>Review]:::input

    T --> A & B
    A & B --> PF
    PF -->|PASS| PASS
    PF -->|ESCALATE| C
    C --> DJ
    DJ -->|PASS| PASS
    DJ -->|BLOCK| BLK
    DJ -->|REVIEW| D
    D --> HR
"""
    )


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
        "-i",
        str(mmd_file),
        "-o",
        str(svg_file),
        "-b",
        "transparent",
        "--width",
        "960",
        "--height",
        "320",
    ] + _puppeteer_flag()

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"  mmdc error: {result.stderr.strip()}")
        return f"<!-- mmdc failed: {result.stderr.strip()} -->"

    svg = svg_file.read_text(encoding="utf-8")

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
