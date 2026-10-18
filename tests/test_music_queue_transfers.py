import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


class MusicQueueTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = AUTOMATIONS.read_text()
        cls.bedside = source.split("- id: 'bedroom_bilresa_remote'", 1)[1].split(
            "\n- id:", 1
        )[0]
        cls.living_room = source.split(
            "- id: 'living_room_tradfri_center_button'", 1
        )[1].split("\n- id:", 1)[0]

    def test_bedside_double_on_transfers_zeppelin_queue_to_a7(self):
        self.assertIn("type: remote_button_double_press", self.bedside)
        self.assertIn("subtype: dim_up\n    id: turn_on_double", self.bedside)
        branch = self.bedside.split(
            "conditions: \"{{ trigger.id == 'turn_on_double' }}\"", 1
        )[1].split("conditions: \"{{ trigger.id == 'turn_off_double' }}\"", 1)[0]
        self.assertIn("action: music_assistant.transfer_queue", branch)
        self.assertIn("entity_id: media_player.bedroom", branch)
        self.assertIn("source_player: media_player.zeppelin", branch)
        self.assertIn("auto_play: true", branch)
        self.assertNotIn("action: light.turn_on", branch)

    def test_bedside_off_turns_off_lights_and_pauses_native_a7_when_playing(self):
        branch = self.bedside.split(
            "conditions: \"{{ trigger.id == 'turn_off' }}\"", 1
        )[1]
        self.assertIn("action: light.turn_off", branch)
        self.assertIn("entity_id: media_player.192_168_1_42", branch)
        self.assertIn('state: "playing"', branch)
        self.assertIn("action: media_player.media_pause", branch)
        self.assertNotIn("entity_id: media_player.bedroom", branch)

    def test_living_room_double_center_transfers_a7_queue_to_zeppelin(self):
        self.assertIn("wait_for_trigger:", self.living_room)
        self.assertIn("milliseconds: 450", self.living_room)
        branch = self.living_room.split("conditions: \"{{ wait.completed }}\"", 1)[1].split(
            "default:", 1
        )[0]
        self.assertIn("action: music_assistant.transfer_queue", branch)
        self.assertIn("entity_id: media_player.zeppelin", branch)
        self.assertIn("source_player: media_player.bedroom", branch)
        self.assertIn("auto_play: true", branch)


if __name__ == "__main__":
    unittest.main()