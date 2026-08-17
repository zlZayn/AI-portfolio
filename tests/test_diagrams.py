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


if __name__ == "__main__":
    unittest.main()
