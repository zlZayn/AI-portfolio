import tempfile
import unittest
from pathlib import Path

import build
from src.data_tables import generate_all


class BuildTests(unittest.TestCase):
    def test_versioned_snapshots_generate_every_data_table(self):
        generated = generate_all()

        self.assertEqual(
            set(generated),
            {"decision-maker", "schema-mapper", "tier-guardian"},
        )
        self.assertIn("Medical Data", generated["decision-maker"])
        self.assertIn("Quality Report", generated["schema-mapper"])
        self.assertIn("Batch Test Results", generated["tier-guardian"])

    def test_repeated_builds_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.html"
            second = Path(directory) / "second.html"

            build.assemble(first)
            build.assemble(second)

            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
