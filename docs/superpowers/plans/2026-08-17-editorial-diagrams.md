# Editorial Diagrams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace eight Mermaid flowcharts with responsive, accessible editorial SVG diagrams based on `cathrynlavery/diagram-design`.

**Architecture:** Preserve the public `src.diagrams.render_all()` contract while converting `src/diagrams.py` into a package. A small SVG canvas owns escaping, theme tokens, accessible metadata, orthogonal routing, nodes, decisions, zones, and annotations; project modules contain declarative content and hand-tuned 4 px grid layouts.

**Tech Stack:** Python 3.12 standard library, Jinja2, inline SVG/CSS, `unittest`, browser screenshot inspection.

---

## File Structure

- Create `src/diagrams/__init__.py`: diagram registry and public rendering contract.
- Create `src/diagrams/theme.py`: portfolio-aligned semantic design tokens.
- Create `src/diagrams/svg.py`: accessible SVG canvas and reusable primitives.
- Create `src/diagrams/projects/*.py`: one layout module per project.
- Create `tests/test_diagram_svg.py`: primitive-level tests.
- Create `tests/test_diagrams.py`: registry and project-story contract tests.
- Modify `static/style.css`: responsive diagram integration.
- Modify `build.py`, `pyproject.toml`, `README.md`, `ARCHITECTURE.md`: remove Mermaid language and document the new build.
- Delete `src/diagrams.py`, `config/puppeteer.json`: remove obsolete renderer and configuration.
- Rebuild `index.html`: generated portfolio output.

### Task 1: SVG Foundation

**Files:**
- Create: `tests/test_diagram_svg.py`
- Create: `src/diagrams/theme.py`
- Create: `src/diagrams/svg.py`

- [ ] **Step 1: Write failing primitive tests**

```python
import unittest

from src.diagrams.svg import Canvas


class CanvasTests(unittest.TestCase):
    def test_svg_is_accessible_and_escapes_text(self):
        canvas = Canvas("sample", "A & B", "Shows <data> safely.")
        canvas.node(40, 40, 160, 64, "Input & rules", tag="CODE")
        svg = canvas.render()
        self.assertIn('role="img"', svg)
        self.assertIn('aria-labelledby="sample-title sample-desc"', svg)
        self.assertIn("A &amp; B", svg)
        self.assertIn("&lt;data&gt;", svg)

    def test_connector_rejects_diagonal_segments(self):
        canvas = Canvas("sample", "Sample", "Sample description.")
        with self.assertRaises(ValueError):
            canvas.connector(((40, 40), (80, 60)))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the missing module failure**

Run: `uv run python -m unittest tests.test_diagram_svg -v`

Expected: `ModuleNotFoundError: No module named 'src.diagrams.svg'`.

- [ ] **Step 3: Implement the theme and canvas API**

`theme.py` defines one immutable `Theme` with `paper`, `surface`, `ink`, `muted`, `soft`, `rule`, `accent`, `accent_tint`, `success`, and `danger` values. `svg.py` defines:

```python
class Canvas:
    def __init__(self, slug: str, title: str, description: str,
                 width: int = 960, height: int = 520): ...
    def zone(self, x: int, y: int, width: int, height: int, label: str): ...
    def node(self, x: int, y: int, width: int, height: int, title: str,
             subtitle: str = "", tag: str = "", kind: str = "default"): ...
    def decision(self, cx: int, cy: int, width: int, height: int,
                 title: str, subtitle: str = ""): ...
    def connector(self, points: tuple[tuple[int, int], ...],
                  label: str = "", style: str = "default"): ...
    def annotation(self, x: int, y: int, text: str): ...
    def render(self): ...
```

Implementation rules:

- Escape every user-facing string with `html.escape(..., quote=True)`.
- Prefix marker, title, and description IDs with `slug`.
- Emit background/zones, then connectors, then nodes, then annotations.
- Validate coordinates on the 4 px grid.
- Reject any connector segment where both x and y change.
- Round orthogonal corners with 8 px quadratic bends.
- Use `width="100%"`, a fixed `viewBox`, and `preserveAspectRatio="xMidYMid meet"`.

- [ ] **Step 4: Run primitive tests**

Run: `uv run python -m unittest tests.test_diagram_svg -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit the foundation**

```bash
git add src/diagrams/theme.py src/diagrams/svg.py tests/test_diagram_svg.py
git commit -m "feat: add editorial svg primitives"
```

### Task 2: Registry And Decision Diagrams

**Files:**
- Create: `src/diagrams/__init__.py`
- Create: `src/diagrams/projects/__init__.py`
- Create: `src/diagrams/projects/decision_maker.py`
- Create: `src/diagrams/projects/tier_guardian.py`
- Create: `tests/test_diagrams.py`

- [ ] **Step 1: Write failing registry and story tests**

```python
import unittest

from src.diagrams import render_all


EXPECTED_IDS = {
    "decision-maker", "rag-embed", "schema-mapper", "tool-calling",
    "collaborate", "tier-guardian", "tablesnap", "raw-to-guide",
}


class DiagramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.diagrams = render_all()

    def test_registry_contains_all_projects(self):
        self.assertEqual(set(self.diagrams), EXPECTED_IDS)

    def test_decision_diagrams_explain_code_owned_branching(self):
        self.assertIn("0 TOKEN", self.diagrams["decision-maker"])
        self.assertIn("CODE ARBITRATION", self.diagrams["tier-guardian"])
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_decision_diagrams_explain_code_owned_branching -v`

Expected: import or assertion failure before the new registry exists.

- [ ] **Step 3: Implement both top-down flowcharts**

`decision_maker.render()` uses at most nine nodes:

```text
CSV profile -> Fingerprint cached?
hit -> Clean output (0 TOKEN)
miss -> Scene code (AI) -> Signal sequence (AI) -> Validate codes
     -> Assemble operations -> Local execution -> Clean output
```

`tier_guardian.render()` uses at most nine primary nodes:

```text
Input -> A/B parallel -> pre_filter (CODE ARBITRATION)
PASS -> Fast release
ESCALATE -> Context judge -> deep_judge (CODE ARBITRATION)
PASS / BLOCK / Human evidence
```

Use diamonds only for actual decisions, label every outgoing branch, and accent the zero-token decision point rather than every AI node.

- [ ] **Step 4: Run the focused story test**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_decision_diagrams_explain_code_owned_branching -v`

Expected: pass.

- [ ] **Step 5: Commit decision diagrams**

```bash
git add src/diagrams/__init__.py src/diagrams/projects tests/test_diagrams.py
git commit -m "feat: add editorial decision diagrams"
```

### Task 3: Four Architecture Diagrams

**Files:**
- Create: `src/diagrams/projects/rag_embed.py`
- Create: `src/diagrams/projects/schema_mapper.py`
- Create: `src/diagrams/projects/tool_calling.py`
- Create: `src/diagrams/projects/tablesnap.py`
- Modify: `src/diagrams/__init__.py`
- Modify: `tests/test_diagrams.py`

- [ ] **Step 1: Add failing architecture-story assertions**

```python
def test_architecture_diagrams_preserve_their_distinguishing_mechanisms(self):
    expected = {
        "rag-embed": ("ENHANCED QUERY", "ORIGINAL QUESTION"),
        "schema-mapper": ("UNIQUE VALUES", "APPLY TO ALL ROWS"),
        "tool-calling": ("ONE REGISTRY", "TWO PROTOCOLS"),
        "tablesnap": ("ONE VLM CALL", "NO OCR PIPELINE"),
    }
    for project_id, phrases in expected.items():
        for phrase in phrases:
            self.assertIn(phrase, self.diagrams[project_id])
```

- [ ] **Step 2: Run the new test and verify failure**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_architecture_diagrams_preserve_their_distinguishing_mechanisms -v`

Expected: missing project key or phrase.

- [ ] **Step 3: Implement zoned architecture layouts**

- `rag_embed`: BUILD and QUERY zones; merge vector/BM25 into one Hybrid Index node; preserve enhanced-query-to-retrieval and original-question-to-answer paths.
- `schema_mapper`: compress full rows to unique values, create a durable Rules artifact, apply locally to all rows; show optional refinement as a dashed secondary route.
- `tool_calling`: MCP and Function Calling adapters converge on ONE REGISTRY; a dashed trust boundary encloses validation, timeout, blocklist, and tool execution.
- `tablesnap`: Hotkey Capture and Batch Files converge on ONE VLM CALL and PSV-to-XLSX export; place `NO OCR PIPELINE` as the single editorial annotation.

Each diagram stays at nine nodes or fewer, uses at most three zones, and uses no diagonal connector.

- [ ] **Step 4: Run architecture-story tests**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_architecture_diagrams_preserve_their_distinguishing_mechanisms -v`

Expected: pass.

- [ ] **Step 5: Commit architecture diagrams**

```bash
git add src/diagrams tests/test_diagrams.py
git commit -m "feat: add project architecture diagrams"
```

### Task 4: Complex Architecture Diagrams

**Files:**
- Create: `src/diagrams/projects/collaborate.py`
- Create: `src/diagrams/projects/raw_to_guide.py`
- Modify: `src/diagrams/__init__.py`
- Modify: `tests/test_diagrams.py`

- [ ] **Step 1: Add failing architecture-story tests**

```python
def test_collaborate_shows_adaptive_orchestration_architecture(self):
    collaborate = self.diagrams["collaborate"]
    self.assertIn("CONTROL PLANE", collaborate)
    self.assertIn("FAILURE ISOLATION", collaborate)
    self.assertIn("STATE.JSON", collaborate)

def test_schema_governed_delivery_shows_contract_and_output(self):
    guide = self.diagrams["raw-to-guide"]
    self.assertIn("SCHEMA CONTRACT", guide)
    self.assertIn("OFFLINE H5", guide)
```

- [ ] **Step 2: Run the new test and verify failure**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_collaborate_shows_adaptive_orchestration_architecture -v`

Expected: missing project key or phrase.

- [ ] **Step 3: Implement architecture layouts**

`collaborate` uses control, execution, and durable interaction planes. It shows a validated dynamic plan, sequential stage barriers with parallel workers, focused bridge context, failure isolation, synthesis, state recovery, SSE observation, and the continue loop.

`raw_to_guide` shows AI authoring, a Schema-governed reference validation loop, and the build path from valid JSON through maps, indexes, backrefs, Jinja2, and the Offline H5. The Schema Contract is focal because it governs both trust and generation.

- [ ] **Step 4: Run all diagram tests**

Run: `uv run python -m unittest tests.test_diagram_svg tests.test_diagrams -v`

Expected: all tests pass and `render_all()` returns eight SVG strings.

- [ ] **Step 5: Commit complex architecture diagrams**

```bash
git add src/diagrams tests/test_diagrams.py
git commit -m "feat: add complex editorial architecture diagrams"
```

### Task 5: Replace Mermaid In The Build

**Files:**
- Delete: `src/diagrams.py`
- Delete: `config/puppeteer.json`
- Modify: `build.py`
- Modify: `pyproject.toml`
- Modify: `static/style.css`
- Modify: `tests/test_diagrams.py`

- [ ] **Step 1: Add failing build-contract tests**

```python
def test_every_svg_has_accessible_metadata_and_no_mermaid_artifacts(self):
    for project_id, svg in self.diagrams.items():
        self.assertTrue(svg.startswith("<svg"), project_id)
        self.assertIn('role="img"', svg)
        self.assertIn(f'id="{project_id}-title"', svg)
        self.assertIn(f'id="{project_id}-desc"', svg)
        self.assertNotIn("mermaid", svg.lower())
        self.assertNotIn("foreignObject", svg)
```

- [ ] **Step 2: Run the contract test before cleanup**

Run: `uv run python -m unittest tests.test_diagrams.DiagramTests.test_every_svg_has_accessible_metadata_and_no_mermaid_artifacts -v`

Expected: pass for new package output; the filesystem scan in the next step still finds old Mermaid files.

- [ ] **Step 3: Remove obsolete runtime and update integration**

- Delete the old single-file renderer and Puppeteer configuration.
- Change `build.py` module text from Mermaid diagrams to editorial SVG diagrams.
- Change the `pyproject.toml` description to `Self-contained HTML portfolio showcasing AI projects with editorial SVG diagrams`.
- Update `.project-diagram` CSS to provide stable responsive sizing, `overflow-x: auto` fallback, and a minimum readable mobile width without card chrome or shadows.

- [ ] **Step 4: Verify source cleanup and build**

Run: `rg -n "Mermaid|mmdc|puppeteer" build.py src config pyproject.toml`

Expected: no matches.

Run: `uv run python build.py`

Expected: eight diagram-rendered messages and a rebuilt `index.html`, with no subprocess or renderer errors.

- [ ] **Step 5: Commit build migration**

```bash
git add -A src/diagrams.py config/puppeteer.json build.py pyproject.toml static/style.css index.html
git commit -m "refactor: replace mermaid diagram pipeline"
```

### Task 6: Documentation And Visual Verification

**Files:**
- Modify: `README.md`
- Modify: `ARCHITECTURE.md`
- Modify: `index.html` if rebuilt after visual corrections.

- [ ] **Step 1: Synchronize documentation**

Update README requirements/build wording and replace the Mermaid section in `ARCHITECTURE.md` with:

- the new `src/diagrams/` package tree;
- the shared-theme/shared-primitives/project-layout separation;
- the four selected visual grammars and why each is used;
- the preserved `render_all()` contract;
- the accessibility, 4 px grid, orthogonal connector, and focal-accent rules;
- the fact that diagram rendering has no Mermaid, Node.js, Chrome, or Puppeteer dependency.

- [ ] **Step 2: Run all automated checks**

Run: `uv run python -m unittest discover -s tests -v`

Expected: all tests pass.

Run: `uv run python build.py`

Expected: successful rebuild.

Run: `git diff --check`

Expected: no whitespace errors.

- [ ] **Step 3: Inspect desktop and mobile renders**

Open the built site through a local HTTP server and capture each project diagram at approximately 1440x1000 and 390x844. Check every diagram for clipped text, overlapping connectors, hidden arrowheads, inconsistent focal accents, horizontal page overflow, and unreadable mobile labels.

- [ ] **Step 4: Correct visual defects and rerun checks**

Make only diagram/layout CSS corrections supported by the screenshot findings. Rerun unit tests, build, desktop screenshots, and mobile screenshots until all eight diagrams pass.

- [ ] **Step 5: Review synchronization and commit**

Run: `git diff -- README.md ARCHITECTURE.md src/diagrams static/style.css build.py pyproject.toml`

Expected: documentation matches code names and dependencies; no obsolete Mermaid statements remain.

```bash
git add README.md ARCHITECTURE.md src/diagrams static/style.css build.py pyproject.toml index.html tests
git commit -m "docs: document editorial diagram architecture"
```

### Task 7: Final Quality Gate

**Files:**
- Verify only; modify diagram sources only if a check fails.

- [ ] **Step 1: Run repository-wide debt scan**

Run: `rg -n "TODO|FIXME|HACK|Mermaid|mmdc|puppeteer" . -g '!index.html' -g '!docs/superpowers/**' -g '!**/.git/**' -g '!**/.venv/**'`

Expected: no diagram-pipeline debt markers or obsolete Mermaid references.

- [ ] **Step 2: Run final tests and build**

Run: `uv run python -m unittest discover -s tests -v`

Expected: all tests pass.

Run: `uv run python build.py`

Expected: successful output containing all eight accessible SVG diagrams.

- [ ] **Step 3: Inspect the final diff and status**

Run: `git diff --check && git status --short`

Expected: no whitespace errors; only intentional implementation or generated-output changes remain.
