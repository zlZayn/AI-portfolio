import unittest
from pathlib import Path

from src.diagrams import render_all


EXPECTED_IDS = {
    "decision-maker",
    "rag-embed",
    "schema-mapper",
    "tool-calling",
    "collaborate",
    "tier-guardian",
    "tablesnap",
    "raw-to-guide",
    "imagora",
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

    def test_architecture_diagrams_preserve_their_distinguishing_mechanisms(self):
        expected = {
            "rag-embed": ("ENHANCED QUERY", "ORIGINAL QUESTION"),
            "schema-mapper": ("UNIQUE VALUES", "FULL ROWS BYPASS AI", "Schema check"),
            "tool-calling": ("ONE REGISTRY", "TWO PROTOCOLS"),
            "tablesnap": ("ONE VLM CALL", "NO OCR PIPELINE"),
        }
        for project_id, phrases in expected.items():
            for phrase in phrases:
                self.assertIn(phrase, self.diagrams[project_id])

    def test_collaborate_shows_adaptive_orchestration_architecture(self):
        collaborate = self.diagrams["collaborate"]
        for phrase in (
            "CONTROL PLANE",
            "DYNAMIC PLAN",
            "STAGE 1 / PARALLEL",
            "STAGE N / PARALLEL",
            "FOCUSED",
            "BRIDGE",
            "FAILURE ISOLATION",
            "STATE.JSON",
            "CONTINUE LOOP",
        ):
            self.assertIn(phrase, collaborate)
        self.assertIn("diagram-typography-expanded", collaborate)

    def test_schema_governed_delivery_shows_contract_and_output(self):
        guide = self.diagrams["raw-to-guide"]
        self.assertIn("SCHEMA CONTRACT", guide)
        self.assertIn("OFFLINE H5", guide)

    def test_imagora_shows_dual_mode_workbench_architecture(self):
        imagora = self.diagrams["imagora"]
        for phrase in (
            "DUAL FRONTENDS",
            "Classic form",
            "Infinite canvas",
            "TaskManager",
            "Asset Registry",
            "SHA-1",
            "RELINK",
        ):
            self.assertIn(phrase, imagora)
        self.assertIn("diagram-typography-expanded", imagora)

    def test_every_svg_has_accessible_metadata_and_no_mermaid_artifacts(self):
        for project_id, svg in self.diagrams.items():
            self.assertTrue(svg.startswith("<svg"), project_id)
            self.assertIn('role="img"', svg)
            self.assertIn(f'id="{project_id}-title"', svg)
            self.assertIn(f'id="{project_id}-desc"', svg)
            self.assertNotIn("mermaid", svg.lower())
            self.assertNotIn("foreignObject", svg)

    def test_mobile_diagrams_keep_the_native_canvas_width(self):
        stylesheet = Path("static/style.css").read_text(encoding="utf-8")
        self.assertIn("min-width: 960px;", stylesheet)
        self.assertIn("editorial-diagram-collaborate", stylesheet)
        self.assertIn("min-width: 1120px;", stylesheet)


if __name__ == "__main__":
    unittest.main()
