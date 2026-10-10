from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ICON = ROOT / "config/www/hemma/icons/balcony-v1.svg"


class LivingRoomBalconyTileTests(unittest.TestCase):
    def test_balcony_light_uses_a_dedicated_balcony_icon(self):
        dashboard = DASHBOARD.read_text()
        living_room = dashboard.split(
            "  - type: custom:grid-layout\n    title: Living Room", 1
        )[1].split("  - type: custom:grid-layout\n    title: Kitchen", 1)[0]

        self.assertEqual(3, living_room.count("light.living_room_balcony"))
        self.assertIn("entity: light.living_room_balcony", living_room)
        self.assertIn("name: Balcony", living_room)
        self.assertIn("icon: balcony-v1", living_room)
        self.assertNotIn("icon: square-ceiling-light", living_room)

        icon = ICON.read_text()
        self.assertIn('viewBox="0 0 24 24"', icon)
        self.assertIn('fill="#fff"', icon)


if __name__ == "__main__":
    unittest.main()
