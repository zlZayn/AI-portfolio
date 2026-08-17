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
