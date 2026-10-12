from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "config/packages/kitchen_fan.yaml"


class KitchenFanPackageTests(unittest.TestCase):
    def test_two_tuya_channels_are_wrapped_as_one_two_speed_fan(self):
        package = PACKAGE.read_text()

        self.assertIn('name: "Kitchen Extractor Fan"', package)
        self.assertIn("unique_id: kitchen_extractor_fan", package)
        self.assertIn("speed_count: 2", package)
        self.assertGreaterEqual(
            package.count("switch.2ch_wi_fi_switch_module_4_switch_1"), 4
        )
        self.assertGreaterEqual(
            package.count("switch.2ch_wi_fi_switch_module_4_switch_2"), 4
        )
        self.assertIn("percentage <= 50", package)
        self.assertIn("percentage > 0", package)

    def test_speed_changes_use_break_before_make_interlocking(self):
        package = PACKAGE.read_text()

        self.assertIn("action: switch.turn_off", package)
        self.assertIn("milliseconds: 500", package)
        self.assertIn("id: speed_1_on", package)
        self.assertIn("id: speed_2_on", package)
        self.assertIn("mode: restart", package)


if __name__ == "__main__":
    unittest.main()
