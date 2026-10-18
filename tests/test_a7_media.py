import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ICON = ROOT / "config/www/hemma/icons/bw-a7-speaker-v1.svg"


class A7MediaDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DASHBOARD.read_text()
        cls.home = cls.source.split("title: Home", 1)[1].split("title: Living Room", 1)[0]
        cls.bedroom = cls.source.split("title: Bedroom", 1)[1].split("title: Bathroom", 1)[0]

    def test_home_media_panel_tile_and_shutdown_status_use_a7(self):
        self.assertIn("active_device_entity_21: media_player.192_168_1_42", self.home)
        self.assertIn("media_player_3: media_player.bedroom", self.home)
        self.assertEqual(2, self.home.count("media_player.bedroom"))
        self.assertEqual(1, self.home.count("media_player.192_168_1_42"))
        self.assertIn("name: B&W A7", self.home)
        self.assertIn("icon: bw-a7-speaker-v1", self.home)

    def test_bedroom_media_panel_and_tile_use_a7(self):
        self.assertIn("media_player_1: media_player.bedroom", self.bedroom)
        self.assertEqual(2, self.bedroom.count("media_player.bedroom"))
        self.assertIn("name: B&W A7", self.bedroom)
        self.assertIn("icon: bw-a7-speaker-v1", self.bedroom)

    def test_custom_a7_icon_is_present_and_monochrome(self):
        icon = ICON.read_text()
        self.assertIn('viewBox="0 0 24 24"', icon)
        self.assertIn('fill="white"', icon)
        self.assertNotIn("#000", icon)


if __name__ == "__main__":
    unittest.main()