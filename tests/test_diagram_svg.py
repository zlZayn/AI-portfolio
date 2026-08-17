import unittest

from src.diagrams.svg import Canvas
from src.diagrams.theme import THEME


def contrast_ratio(foreground: str, background: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [
            value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
            for value in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


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

    def test_connector_labels_render_above_nodes(self):
        canvas = Canvas("sample", "Sample", "Sample description.")
        canvas.connector(((40, 80), (240, 80)), "handoff")
        canvas.node(80, 40, 120, 80, "Node", tag="CODE")

        svg = canvas.render()

        self.assertLess(svg.index('class="node-box"'), svg.index('class="connector-label"'))

    def test_small_text_tokens_meet_normal_text_contrast(self):
        self.assertGreaterEqual(contrast_ratio(THEME.muted, THEME.paper), 4.5)
        self.assertGreaterEqual(contrast_ratio(THEME.accent_strong, THEME.paper), 4.5)


if __name__ == "__main__":
    unittest.main()
