from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


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
    def test_bathroom_fan_turns_off_after_45_minutes(self):
        block = automation_block(AUTOMATIONS.read_text(), "Bathroom Fan - Delay")

        self.assertIn("minutes: 45", block)
        self.assertIn("action: fan.turn_off", block)
        self.assertIn("entity_id: fan.bathroom_fan_bathroom", block)
        self.assertNotIn("minutes: 20", block)

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
