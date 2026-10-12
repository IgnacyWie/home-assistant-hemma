from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ICON = ROOT / "config/www/hemma/icons/lightbulb-spot-v1.svg"


class KitchenLightTileTests(unittest.TestCase):
    def test_kitchen_lights_are_only_in_kitchen_view(self):
        dashboard = DASHBOARD.read_text()
        home = dashboard.split(
            "  - type: custom:grid-layout\n    title: Kitchen", 1
        )[0]
        kitchen = dashboard.split(
            "  - type: custom:grid-layout\n    title: Kitchen", 1
        )[1].split("  - type: custom:grid-layout\n    title: Bedroom", 1)[0]

        self.assertNotIn("light.kitchen_1", home)
        self.assertNotIn("light.2ch_wi_fi_switch_module_3_switch_1", home)
        self.assertNotIn("light.kitchen_shelly2pmg4_d885ace4f060_output_1", home)
        self.assertEqual(3, kitchen.count("light.kitchen_1"))
        self.assertEqual(3, kitchen.count("light.2ch_wi_fi_switch_module_3_switch_1"))
        self.assertEqual(
            3, kitchen.count("light.kitchen_shelly2pmg4_d885ace4f060_output_1")
        )
        self.assertIn("name: Kitchen 1", kitchen)
        self.assertIn("name: Kitchen 2", kitchen)
        self.assertGreaterEqual(kitchen.count("icon: lightbulb-spot-v1"), 2)
        self.assertIn("name: Kitchen LED", kitchen)
        self.assertIn("icon: led-strip-variant", kitchen)
        self.assertNotIn("icon: lightbulb-spot-v1", home)

        icon = ICON.read_text()
        self.assertIn('viewBox="0 0 24 24"', icon)
        self.assertIn('fill="#fff"', icon)


if __name__ == "__main__":
    unittest.main()
