from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "config/dashboards/templates/button_cards/badges"
ROOM = ROOT / "config/dashboards/templates/button_cards/cards/hemma_room.yaml"
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"


class ContextualHeaderTests(unittest.TestCase):
    def test_energy_uses_configurable_strict_threshold(self):
        energy = (BADGES / "hemma_badge_energy_group.yaml").read_text()
        room = ROOM.read_text()
        dashboard = DASHBOARD.read_text()
        self.assertIn("watts > Number(variables.prominence_threshold ?? 1000)", energy)
        self.assertIn("energy_prominence_threshold: 1000", room)
        self.assertIn("energy_prominence_threshold: 1000", dashboard)

    def test_alarm_supports_evening_context_but_is_persistent_in_home_and_bedroom(self):
        alarm = (BADGES / "hemma_badge_wake_alarm.yaml").read_text()
        dashboard = DASHBOARD.read_text()
        self.assertIn("evening_start: 18", alarm)
        self.assertIn("evening_end: 3", alarm)
        self.assertIn("variables.evening_only === false || evening", alarm)
        self.assertEqual(dashboard.count("wake_alarm_evening_only: false"), 2)

    def test_low_battery_only_appears_below_twenty_percent(self):
        battery = (BADGES / "hemma_badge_low_battery.yaml").read_text()
        dashboard = DASHBOARD.read_text()
        self.assertIn("threshold: 20", battery)
        self.assertIn("x.level < threshold", battery)
        self.assertIn("presence_battery_entity_1: sensor.phi_battery_level", dashboard)

    def test_devices_on_is_always_visible_without_presence_gating(self):
        active = (BADGES / "hemma_badge_active_devices.yaml").read_text()
        room = ROOM.read_text()
        dashboard = DASHBOARD.read_text()
        self.assertIn("enabled && configured.length", active)
        self.assertNotIn("enabled && configured.length && active", active)
        self.assertNotIn("leaving_entity", active)
        self.assertNotIn("active_devices_leaving_entity", room)
        self.assertNotIn("active_devices_leaving_entity", dashboard)

    def test_media_only_appears_during_playback(self):
        media = (BADGES / "hemma_badge_media_group.yaml").read_text()
        self.assertGreaterEqual(media.count("return ['playing','buffering'].includes(st);"), 3)
        self.assertNotIn("pc_count", media)


if __name__ == "__main__":
    unittest.main()