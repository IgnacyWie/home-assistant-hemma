from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "config/dashboards/templates/button_cards/badges"
NEUTRAL_PILL = "background: var(--badge-background, rgba(10,12,14,0.65))"


class ChipColorConventionTests(unittest.TestCase):
    def badge(self, name):
        return (BADGES / name).read_text()

    def assert_neutral_pill(self, name):
        self.assertIn(NEUTRAL_PILL, self.badge(name))

    def test_action_and_scene_chips_use_orange_icons(self):
        for name in ("hemma_badge_scene.yaml", "hemma_badge_cinema.yaml"):
            with self.subTest(name=name):
                text = self.badge(name)
                self.assert_neutral_pill(name)
                self.assertIn("background: '#FF9500'", text)

    def test_energy_chips_are_neutral(self):
        for name in ("hemma_badge_energy.yaml", "hemma_badge_energy_group.yaml"):
            with self.subTest(name=name):
                text = self.badge(name)
                self.assertIn("--hemma-badge-info-color", text)
        self.assert_neutral_pill("hemma_badge_energy_group.yaml")

    def test_presence_uses_green_only_for_home_state(self):
        for name in ("hemma_badge_presence.yaml", "hemma_badge_presence_group.yaml"):
            with self.subTest(name=name):
                text = self.badge(name)
                self.assertIn("--hemma-badge-healthy-color", text)
                self.assertIn("rgba(255,255,255,0.10)", text)
                self.assertIn("- --hemma-badge-icon-bg: >", text)
                self.assertNotIn("    img_cell:\n      - background: >", text)
        self.assert_neutral_pill("hemma_badge_presence_group.yaml")

    def test_circle_backgrounds_use_the_base_template_css_variable(self):
        # hemma_badge_base sets #img-cell background with !important, so child
        # templates must set its CSS variable rather than styles.img_cell.
        for name in (
            "hemma_badge_energy_group.yaml",
            "hemma_badge_low_battery.yaml",
            "hemma_badge_active_devices.yaml",
        ):
            with self.subTest(name=name):
                text = self.badge(name)
                self.assertIn("--hemma-badge-icon-bg", text)
                self.assertNotIn("    img_cell:\n      - background:", text)

    def test_enabled_alarm_uses_scheduled_blue(self):
        text = self.badge("hemma_badge_wake_alarm.yaml")
        self.assert_neutral_pill("hemma_badge_wake_alarm.yaml")
        self.assertIn("--hemma-badge-scheduled-color, #0A84FF", text)
        self.assertIn("entity?.state === 'on'", text)

    def test_attention_chips_use_red_icons(self):
        for name in ("hemma_badge_low_battery.yaml", "hemma_badge_active_devices.yaml"):
            with self.subTest(name=name):
                text = self.badge(name)
                self.assert_neutral_pill(name)
                self.assertIn("--hemma-badge-attention-color, #FF453A", text)


if __name__ == "__main__":
    unittest.main()
