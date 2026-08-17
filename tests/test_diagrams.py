import unittest

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
            "schema-mapper": ("UNIQUE VALUES", "APPLY TO ALL ROWS"),
            "tool-calling": ("ONE REGISTRY", "TWO PROTOCOLS"),
            "tablesnap": ("ONE VLM CALL", "NO OCR PIPELINE"),
        }
        for project_id, phrases in expected.items():
            for phrase in phrases:
                self.assertIn(phrase, self.diagrams[project_id])

    def test_role_based_diagrams_show_ownership_and_handoffs(self):
        collaborate = self.diagrams["collaborate"]
        self.assertIn("PARALLEL WITHIN", collaborate)
        self.assertIn("BRIDGE CONTEXT", collaborate)
        guide = self.diagrams["raw-to-guide"]
        self.assertIn("SCHEMA CONTRACT", guide)
        self.assertIn("OFFLINE H5", guide)


if __name__ == "__main__":
    unittest.main()
