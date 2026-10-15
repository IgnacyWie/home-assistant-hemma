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

    def test_all_five_controls_use_the_new_living_room_remote(self):
        remote = self.remote_source()
        self.assertEqual(8, remote.count(f"device_id: {DEVICE_ID}"))
        for trigger in (
            "type: remote_button_short_press\n    subtype: turn_on\n    id: pause",
            "type: remote_button_long_press\n    subtype: turn_on\n    id: power_off",
            "type: remote_button_short_press\n    subtype: dim_up\n    id: volume_up",
            "type: remote_button_long_press\n    subtype: dim_up\n    id: volume_up",
            "type: remote_button_short_press\n    subtype: dim_down\n    id: volume_down",
            "type: remote_button_long_press\n    subtype: dim_down\n    id: volume_down",
            "type: remote_button_short_press\n    subtype: left\n    id: previous_or_left",
            "type: remote_button_short_press\n    subtype: right\n    id: next_or_right",
        ):
            self.assertIn(trigger, remote)

    def test_volume_buttons_follow_the_currently_playing_endpoint(self):
        remote = self.remote_source()
        self.assertIn("is_state('media_player.zeppelin', 'playing')", remote)
        self.assertIn("media_player.living_room_tv_2", remote)
        self.assertIn("action: media_player.volume_up", remote)
        self.assertIn("action: media_player.volume_down", remote)
        self.assertIn("entity_id: \"{{ active_volume_player }}\"", remote)

    def test_center_button_toggles_active_media_and_hold_turns_both_off(self):
        remote = self.remote_source()
        self.assertIn("action: media_player.media_play_pause", remote)
        self.assertIn("states('media_player.zeppelin') in ['playing', 'paused']", remote)
        self.assertIn("states('media_player.tv_w_salonie') in ['playing', 'paused']", remote)
        self.assertIn("last_changed", remote)
        self.assertIn("entity_id: \"{{ active_transport_player }}\"", remote)
        power_off = remote.split("trigger.id == 'power_off'", 1)[1]
        self.assertIn("action: media_player.turn_off", power_off)
        self.assertIn("entity_id: media_player.zeppelin", power_off)
        self.assertIn("entity_id: media_player.living_room_tv_2", power_off)

    def test_side_buttons_skip_music_or_navigate_the_tv(self):
        remote = self.remote_source()
        self.assertIn("action: media_player.media_previous_track", remote)
        self.assertIn("action: media_player.media_next_track", remote)
        self.assertIn("entity_id: media_player.zeppelin", remote)
        self.assertIn("action: remote.send_command", remote)
        self.assertIn("entity_id: remote.living_room_tv", remote)
        self.assertIn("command: DPAD_LEFT", remote)
        self.assertIn("command: DPAD_RIGHT", remote)


if __name__ == "__main__":
    unittest.main()
