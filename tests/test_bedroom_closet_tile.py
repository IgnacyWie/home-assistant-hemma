from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"


class BedroomClosetTileTests(unittest.TestCase):
    def test_closet_light_is_in_bedroom_summary_and_tile(self):
        dashboard = DASHBOARD.read_text()
        bedroom = dashboard.split(
            "  - type: custom:grid-layout\n    title: Bedroom", 1
        )[1].split("  - type: custom:grid-layout\n    title: Bathroom", 1)[0]

        self.assertEqual(2, bedroom.count("light.bedroom_closet"))
        self.assertIn("light_entity_4: light.bedroom_closet", bedroom)
        self.assertIn("entity: light.bedroom_closet", bedroom)
        self.assertIn("name: Closet", bedroom)
        self.assertIn("icon: track-light", bedroom)
        self.assertIn("template: hemma_light", bedroom)


if __name__ == "__main__":
    unittest.main()
