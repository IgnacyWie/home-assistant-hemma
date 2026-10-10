import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SMART_ROW = ROOT / "config/custom_components/hemma/scripts/smart-row.js"


class SmartRowViewportEdgeTests(unittest.TestCase):
    def test_scrolling_host_reaches_the_right_viewport_edge(self):
        script = SMART_ROW.read_text()
        self.assertIn(
            "var(--hemma-entity-right-inset-current, "
            "var(--hemma-entity-right-inset-desktop, 0px))",
            script,
        )
        self.assertNotIn(
            "var(--hemma-entity-right-inset-desktop, "
            "var(--hemma-rail-left, var(--page-gutter, 8vw)))",
            script,
        )

    def test_scrolling_content_keeps_its_left_rail(self):
        script = SMART_ROW.read_text()
        self.assertIn(
            "--hsr-rail: var(--hemma-entity-left-inset-current, "
            "var(--hemma-entity-left-inset-desktop, "
            "var(--hemma-rail-left, var(--page-gutter, 8vw))))",
            script,
        )
        self.assertIn("scroll-padding-left: var(--hsr-rail);", script)
        self.assertIn("var(--hsr-rail);\n", script)


if __name__ == "__main__":
    unittest.main()
