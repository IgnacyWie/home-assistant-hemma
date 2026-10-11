from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ICON = ROOT / "config/www/hemma/icons/kitchen-extractor-v1.svg"


class KitchenFanTileTests(unittest.TestCase):
    def test_extractor_fan_is_in_kitchen_view(self):
        dashboard = DASHBOARD.read_text()
        kitchen = dashboard.split(
            "  - type: custom:grid-layout\n    title: Kitchen", 1
        )[1].split("  - type: custom:grid-layout\n    title: Bedroom", 1)[0]

        self.assertEqual(1, kitchen.count("fan.kitchen_fan_kitchen"))
        self.assertIn("template: hemma_fan", kitchen)
        self.assertIn("name: Extractor Fan", kitchen)
        self.assertIn("icon: kitchen-extractor-v1", kitchen)
        self.assertNotIn("icon: bathroom-extractor-v1", kitchen)

        icon = ICON.read_text()
        self.assertIn('viewBox="0 0 24 24"', icon)
        self.assertIn('fill="white"', icon)


if __name__ == "__main__":
    unittest.main()
