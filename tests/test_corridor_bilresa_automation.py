from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


class CorridorBilresaAutomationTests(unittest.TestCase):
    def test_buttons_map_to_home_modes(self):
        source = AUTOMATIONS.read_text()
        automation = source.split("- id: 'corridor_bilresa_home_modes'", 1)[1]
        self.assertIn("entity_id: event.bilresa_dual_button_button_1", automation)
        self.assertIn("entity_id: event.bilresa_dual_button_button_2", automation)
        self.assertIn("id: welcome_home", automation)
        self.assertIn("id: leave_home", automation)
        self.assertNotIn("attribute: event_type", automation)
        self.assertIn("trigger.to_state.attributes.event_type == 'multi_press_1'", automation)
        self.assertIn("trigger.to_state.attributes.event_type == 'multi_press_2'", automation)
        self.assertIn("entity_id: scene.welcome_home", automation)
        self.assertIn("entity_id: script.french_jazz_lounge", automation)
        self.assertIn("entity_id: script.leave_home", automation)

    def test_french_jazz_lounge_script_replaces_music_on_zeppelin(self):
        scripts = (ROOT / "config/scripts.yaml").read_text()
        lounge = scripts.split("french_jazz_lounge:", 1)[1].split("leave_home:", 1)[0]
        self.assertIn("action: music_assistant.play_media", lounge)
        self.assertIn("entity_id: media_player.zeppelin", lounge)
        self.assertIn("spotify://playlist/75tpCkAq8iJogkzHn7q6AW", lounge)
        self.assertIn("media_type: playlist", lounge)
        self.assertIn("enqueue: replace", lounge)
        self.assertIn("action: media_player.shuffle_set", lounge)
        self.assertIn("shuffle: true", lounge)


if __name__ == "__main__":
    unittest.main()