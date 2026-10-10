from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"


class ZeppelinLightTileTests(unittest.TestCase):
    def test_zeppelin_light_is_a_living_room_tile_and_summary_light(self):
        dashboard = DASHBOARD.read_text()
        living_room = dashboard.split(
            "  - type: custom:grid-layout\n    title: Living Room", 1
        )[1].split("  - type: custom:grid-layout\n    title: Kitchen", 1)[0]

        self.assertEqual(2, living_room.count("light.zeppelin_light"))
        self.assertIn("light_entity_5: light.zeppelin_light", living_room)
        self.assertIn("entity: light.zeppelin_light", living_room)
        self.assertIn("name: Zeppelin Light", living_room)
        self.assertIn("template: hemma_light", living_room)


if __name__ == "__main__":
    unittest.main()
