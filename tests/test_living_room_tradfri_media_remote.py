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

    def test_volume_buttons_follow_the_currently_playing_endpoint(self):
        remote = self.remote_source()
        self.assertIn("is_state('media_player.zeppelin', 'playing')", remote)
        self.assertIn("media_player.living_room_tv_2", remote)
        self.assertIn("action: media_player.volume_up", remote)
        self.assertIn("action: media_player.volume_down", remote)
        self.assertIn("entity_id: \"{{ active_volume_player }}\"", remote)

    def test_center_button_instantly_pauses_or_resumes_active_media(self):
        center = self.center_source()
        self.assertIn(f"device_id: {DEVICE_ID}", center)
        self.assertIn("type: remote_button_short_press", center)
        self.assertIn("subtype: turn_on", center)
        self.assertNotIn("wait_for_trigger:", center)
        self.assertNotIn("timeout:", center)
        self.assertNotIn("media_player.turn_off", center)
        self.assertIn("mode: restart", center)
        self.assertIn("action: media_player.media_play", center)
        self.assertIn("action: media_player.media_pause", center)
        self.assertNotIn("action: media_player.media_play_pause", center)
        self.assertIn("states(active_transport_player) == 'paused'", center)
        self.assertIn("states(active_transport_player) == 'playing'", center)
        self.assertIn("states('media_player.zeppelin') in ['playing', 'paused']", center)
        self.assertIn("states('media_player.tv_w_salonie') in ['playing', 'paused']", center)
        self.assertIn("last_changed", center)
        self.assertIn("entity_id: \"{{ active_transport_player }}\"", center)

    def test_music_assistant_tv_receiver_is_treated_as_zeppelin_display(self):
        remote = self.remote_source()
        self.assertIn("tv_music_assistant_display", remote)
        self.assertIn("state_attr('media_player.tv_w_salonie', 'app_name') == 'Music Assistant'", remote)
        self.assertIn("state_attr('media_player.tv_w_salonie', 'media_title') == 'Music Assistant'", remote)
        self.assertIn("and not tv_music_assistant_display", self.center_source())
        self.assertIn("tv_music_assistant_display and zeppelin_available", remote)
        self.assertIn("previous_or_left' and zeppelin_selected", remote)
        self.assertIn("next_or_right' and zeppelin_selected", remote)

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
