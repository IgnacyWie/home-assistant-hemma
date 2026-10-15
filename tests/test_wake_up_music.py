from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


class WakeUpMusicTests(unittest.TestCase):
    def test_wake_up_uses_shuffled_happy_jazz_bossa_nova_playlist(self):
        source = AUTOMATIONS.read_text()
        wake = source.split("- id: 'wake_up_music_zeppelin'", 1)[1].split(
            "- id: 'stop_wake_up_music'", 1
        )[0]
        self.assertIn("spotify://playlist/6j2DUZglv11u2UgCdozFXM", wake)
        self.assertIn("media_type: playlist", wake)
        self.assertIn("enqueue: replace", wake)
        self.assertIn("action: media_player.shuffle_set", wake)
        self.assertIn("shuffle: true", wake)
        self.assertNotIn("Guten Morgen Sonnenschein", wake)
        self.assertNotIn("Nana Mouskouri", wake)


if __name__ == "__main__":
    unittest.main()
