from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
SCREEN_LAYOUT = ROOT / "config/dashboards/templates/includes/hemma_screen_layout.yaml"


class RoomViewportEdgeTests(unittest.TestCase):
    def test_shared_room_layout_reaches_the_viewport_edge(self):
        layout = SCREEN_LAYOUT.read_text()
        self.assertIn("width: 100vw\n", layout)
        self.assertIn("max-width: 100vw\n", layout)
        self.assertIn("margin: 0\n", layout)
        self.assertIn("padding: 0\n", layout)

    def test_all_six_room_views_use_the_shared_layout(self):
        dashboard = DASHBOARD.read_text()
        include = (
            "    layout: !include "
            "/config/dashboards/templates/includes/hemma_screen_layout.yaml\n"
        )
        self.assertEqual(6, dashboard.count(include))


if __name__ == "__main__":
    unittest.main()
