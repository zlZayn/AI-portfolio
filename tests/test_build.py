import tempfile
import unittest
from pathlib import Path

import build
from src.data_tables import generate_all
from src.diagrams import render_all


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

    def test_exported_diagrams_match_the_rendered_svg(self):
        with tempfile.TemporaryDirectory() as directory:
            build.assemble(Path(directory) / "index.html")

        diagrams = render_all()
        self.assertEqual(
            {path.name for path in build.DIAGRAMS_DIR.glob("*.svg")},
            {f"{slug}.svg" for slug in diagrams},
        )
        for slug, svg in diagrams.items():
            exported = (build.DIAGRAMS_DIR / f"{slug}.svg").read_text(encoding="utf-8")
            self.assertEqual(exported, svg, f"{slug}.svg differs from the embedded markup")

    def test_repeated_builds_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.html"
            second = Path(directory) / "second.html"

            build.assemble(first)
            build.assemble(second)

            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
