import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"
DEVICE_ID = "a8940bb7824bdae5bfe525f2e61e95f3"


class LivingRoomTradfriMediaRemoteTests(unittest.TestCase):
    def remote_source(self):
        source = AUTOMATIONS.read_text()
        marker = "- id: 'living_room_tradfri_media_remote'"
        self.assertIn(marker, source)
        return source.split(marker, 1)[1].split("\n- id:", 1)[0]

    def center_source(self):
        source = AUTOMATIONS.read_text()
        marker = "- id: 'living_room_tradfri_center_button'"
        self.assertIn(marker, source)
        return source.split(marker, 1)[1].split("\n- id:", 1)[0]

    def test_all_five_controls_use_the_new_living_room_remote(self):
        remote = self.remote_source()
        self.assertEqual(6, remote.count(f"device_id: {DEVICE_ID}"))
        for trigger in (
            "type: remote_button_short_press\n    subtype: dim_up\n    id: volume_up",
            "type: remote_button_long_press\n    subtype: dim_up\n    id: volume_up",
            "type: remote_button_short_press\n    subtype: dim_down\n    id: volume_down",
            "type: remote_button_long_press\n    subtype: dim_down\n    id: volume_down",
            "type: remote_button_short_press\n    subtype: left\n    id: previous_or_left",
            "type: remote_button_short_press\n    subtype: right\n    id: next_or_right",
        ):
            self.assertIn(trigger, remote)

    def test_volume_buttons_only_control_zeppelin(self):
        remote = self.remote_source()
        self.assertIn("action: media_player.volume_up", remote)
        self.assertIn("action: media_player.volume_down", remote)
        self.assertEqual(4, remote.count("entity_id: media_player.zeppelin"))
        self.assertNotIn("living_room_tv", remote)
        self.assertNotIn("tv_w_salonie", remote)

    def test_center_button_distinguishes_single_and_double_press(self):
        center = self.center_source()
        self.assertEqual(2, center.count(f"device_id: {DEVICE_ID}"))
        self.assertIn("type: remote_button_short_press", center)
        self.assertIn("subtype: turn_on", center)
        self.assertIn("wait_for_trigger:", center)
        self.assertIn("milliseconds: 450", center)
        self.assertIn("{{ wait.completed }}", center)
        self.assertNotIn("media_player.turn_off", center)
        self.assertIn("mode: single", center)
        self.assertIn("action: media_player.media_play", center)
        self.assertIn("action: media_player.media_pause", center)
        self.assertNotIn("action: media_player.media_play_pause", center)
        self.assertIn("states(active_transport_player) == 'paused'", center)
        self.assertIn("states(active_transport_player) == 'playing'", center)
        self.assertIn("active_transport_player: media_player.zeppelin", center)
        self.assertIn("entity_id: media_player.zeppelin", center)
        self.assertIn("states(active_transport_player) not in ['playing', 'paused']", center)
        self.assertIn("action: script.turn_on", center)
        self.assertIn("entity_id: script.french_jazz_lounge", center)
        self.assertIn("action: music_assistant.transfer_queue", center)
        self.assertIn("source_player: media_player.bedroom", center)
        self.assertIn("auto_play: true", center)
        self.assertNotIn("living_room_tv", center)
        self.assertNotIn("tv_w_salonie", center)

    def test_side_buttons_only_skip_zeppelin_tracks(self):
        remote = self.remote_source()
        self.assertIn("action: media_player.media_previous_track", remote)
        self.assertIn("action: media_player.media_next_track", remote)
        self.assertEqual(4, remote.count("entity_id: media_player.zeppelin"))
        self.assertNotIn("remote.send_command", remote)
        self.assertNotIn("DPAD_LEFT", remote)
        self.assertNotIn("DPAD_RIGHT", remote)


if __name__ == "__main__":
    unittest.main()
