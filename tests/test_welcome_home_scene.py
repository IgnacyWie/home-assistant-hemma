from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "config/scenes.yaml"
HELPERS = ROOT / "config/packages/hemma_helpers.yaml"

WELCOME_HOME_STATES = {
    "light.bedroom_accent_bedroom": "on",
    "light.living_room_accent_1": "on",
    "light.living_room_2ch_wi_fi_switch_module_switch_2": "on",
    "light.3_in_1_controller_wifi_2_4g": "on",
    "light.bedroom_ikea_of_sweden_grillplats_plug": "on",
    "light.zeppelin_light": "on",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_1": "off",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_2": "off",
    "light.living_room_2ch_wi_fi_switch_module_switch_1": "off",
    "light.living_room_balcony": "off",
    "switch.bathroom_lamp": "off",
    "light.kitchen_1": "off",
    "light.2ch_wi_fi_switch_module_3_switch_1": "off",
    "light.2ch_wi_fi_switch_module_3_switch_2": "off",
}


class WelcomeHomeSceneTests(unittest.TestCase):
    def test_scene_and_active_sensor_cover_the_exact_lighting_snapshot(self):
        scenes = SCENES.read_text()
        welcome_scene = scenes.split("- id: welcome_home", 1)[1].split(
            "- id: leave_home", 1
        )[0]
        scene_states = dict(
            re.findall(
                r'^    ([a-z_]+\.[a-z0-9_]+):\n      state: "(on|off)"$',
                welcome_scene,
                re.MULTILINE,
            )
        )
        self.assertEqual(WELCOME_HOME_STATES, scene_states)
        self.assertNotIn("media_player.zeppelin", welcome_scene)

        helpers = HELPERS.read_text()
        active_sensor = helpers.split("- name: Welcome Home Scene Active", 1)[1].split(
            "- name: Leave Home Scene Active", 1
        )[0]
        for entity_id, state in WELCOME_HOME_STATES.items():
            self.assertIn(f"is_state('{entity_id}', '{state}')", active_sensor)


if __name__ == "__main__":
    unittest.main()
