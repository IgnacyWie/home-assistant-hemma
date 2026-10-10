from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
NAVIGATION = ROOT / "config/dashboards/templates/includes/hemma_navbar_tablet.yaml"


class MusicAssistantViewTests(unittest.TestCase):
    def setUp(self):
        self.dashboard = DASHBOARD.read_text()
        self.navigation = NAVIGATION.read_text()

    def test_music_view_embeds_https_music_assistant(self):
        self.assertEqual(self.dashboard.count("    path: music\n"), 1)
        self.assertEqual(self.dashboard.count("      - type: iframe\n"), 1)
        self.assertIn(
            'url: "https://music.home.wie.dev/#/home?player=true&showFullscreenPlayer=true"',
            self.dashboard,
        )
        self.assertIn("        hide_background: true\n", self.dashboard)

    def test_shared_navigation_has_one_music_route(self):
        route = "        - url: /dashboard-hemma/music\n"
        self.assertEqual(self.navigation.count(route), 1)
        self.assertIn("          label: Music\n", self.navigation)
        self.assertIn("          icon: mdi:music-circle\n", self.navigation)


if __name__ == "__main__":
    unittest.main()