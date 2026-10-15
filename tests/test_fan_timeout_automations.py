from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"
BATHROOM_PACKAGE = ROOT / "config/packages/bathroom_fan_humidity.yaml"


def automation_block(text: str, alias: str) -> str:
    marker = f"  alias: {alias}\n"
    start = text.index(marker)
    block_start = text.rfind("\n- id:", 0, start)
    if block_start == -1:
        block_start = 0
    else:
        block_start += 1
    block_end = text.find("\n- id:", start)
    return text[block_start:] if block_end == -1 else text[block_start:block_end]


class FanTimeoutAutomationTests(unittest.TestCase):
    def test_bathroom_fan_uses_humidity_control_and_sixty_minute_failsafe(self):
        package = BATHROOM_PACKAGE.read_text()

        self.assertIn("id: bathroom_fan_humidity_control", package)
        self.assertIn("sensor.timmerflotte_temp_hmd_sensor_humidity_2", package)
        self.assertIn("sensor.timmerflotte_temp_hmd_sensor_humidity", package)
        self.assertIn("bathroom | float(0) >= ([65, bedroom | float(0) + 7] | max)", package)
        self.assertIn("bathroom | float(0) <= bedroom | float(0) + 3", package)
        self.assertIn('for: "00:03:00"', package)
        self.assertIn('for: "00:10:00"', package)
        self.assertIn('duration: "01:00:00"', package)
        self.assertIn("restore: true", package)
        self.assertIn("entity_id: fan.bathroom_fan_bathroom", package)
        self.assertIn("action: fan.turn_on", package)
        self.assertIn("action: fan.turn_off", package)
        self.assertNotIn("00:45:00", package)
        self.assertNotIn("Bathroom Fan - Delay", AUTOMATIONS.read_text())

    def test_kitchen_fan_turns_off_after_60_minutes_at_either_speed(self):
        block = automation_block(
            AUTOMATIONS.read_text(), "Kitchen Extractor Fan - 60-minute timeout"
        )

        self.assertIn("entity_id: fan.kitchen_extractor_fan", block)
        self.assertIn("to: 'on'", block)
        self.assertIn("minutes: 60", block)
        self.assertIn("action: fan.turn_off", block)
        self.assertIn("mode: restart", block)


if __name__ == "__main__":
    unittest.main()
