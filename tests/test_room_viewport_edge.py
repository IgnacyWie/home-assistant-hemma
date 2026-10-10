from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
SCREEN_LAYOUT = ROOT / "config/dashboards/templates/includes/hemma_screen_layout.yaml"


class RoomViewportEdgeTests(unittest.TestCase):
    def test_shared_room_layout_does_not_force_viewport_width(self):
        layout = SCREEN_LAYOUT.read_text()
        self.assertNotIn("width: 100vw\n", layout)
        self.assertNotIn("max-width: 100vw\n", layout)
        self.assertIn("margin: 0\n", layout)
        self.assertIn("padding: 0\n", layout)

    def test_shared_room_layout_has_a_fixed_one_viewport_height(self):
        layout = SCREEN_LAYOUT.read_text()
        lines = [line.strip() for line in layout.splitlines()]
        self.assertEqual(2, lines.count("height: 100vh"))
        self.assertEqual(2, lines.count("min-height: 100vh"))
        self.assertEqual(2, lines.count("max-height: 100vh"))
        self.assertEqual(2, lines.count("overflow: hidden"))
        self.assertNotIn("min-height: 100svh\n", layout)
        self.assertNotIn("min-height: 100dvh\n", layout)
        self.assertNotIn("overflow: visible\n", layout)

    def test_all_six_room_views_use_the_shared_layout(self):
        dashboard = DASHBOARD.read_text()
        include = (
            "    layout: !include "
            "/config/dashboards/templates/includes/hemma_screen_layout.yaml\n"
        )
        self.assertEqual(6, dashboard.count(include))


if __name__ == "__main__":
    unittest.main()
