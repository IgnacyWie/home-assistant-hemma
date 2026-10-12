from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "config/scenes.yaml"
HELPERS = ROOT / "config/packages/hemma_helpers.yaml"

LEAVE_HOME_TARGETS = {
    "light.bedroom_accent_bedroom",
    "light.living_room_accent_1",
    "light.living_room_2ch_wi_fi_switch_module_switch_2",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_1",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_2",
    "light.living_room_2ch_wi_fi_switch_module_switch_1",
    "light.living_room_balcony",
    "light.zeppelin_light",
    "light.bedroom_closet",
    "light.bathroom_led_bathroom",
    "light.3_in_1_controller_wifi_2_4g",
    "light.bedroom_ikea_of_sweden_grillplats_plug",
    "light.kitchen_1",
    "light.2ch_wi_fi_switch_module_3_switch_1",
    "light.2ch_wi_fi_switch_module_3_switch_2",
    "switch.ikea_of_sweden_grillplats_plug_2",
    "fan.kitchen_extractor_fan",
    "media_player.zeppelin",
}


class LeaveHomeSceneTests(unittest.TestCase):
    def test_scene_and_active_sensor_cover_the_exact_leave_home_targets(self):
        scenes = SCENES.read_text()
        leave_scene = scenes.split("- id: leave_home", 1)[1]
        scene_targets = set(
            re.findall(r"^    ([a-z_]+\.[a-z0-9_]+):$", leave_scene, re.MULTILINE)
        )
        self.assertEqual(LEAVE_HOME_TARGETS, scene_targets)

        helpers = HELPERS.read_text()
        active_sensor = helpers.split("- name: Leave Home Scene Active", 1)[1]
        for entity_id in LEAVE_HOME_TARGETS - {"media_player.zeppelin"}:
            self.assertIn(f"is_state('{entity_id}', 'off')", active_sensor)
        self.assertIn(
            "states('media_player.zeppelin') in ['off', 'idle', 'paused', 'standby']",
            active_sensor,
        )

    def test_bathroom_fan_is_explicitly_excluded(self):
        self.assertNotIn("fan.bathroom_fan_bathroom", SCENES.read_text())
        active_sensor = HELPERS.read_text().split(
            "- name: Leave Home Scene Active", 1
        )[1]
        self.assertNotIn("fan.bathroom_fan_bathroom", active_sensor)


if __name__ == "__main__":
    unittest.main()
