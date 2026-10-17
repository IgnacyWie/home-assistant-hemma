from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


def automation_block(text: str, automation_id: str) -> str:
    marker = f"- id: '{automation_id}'"
    start = text.index(marker)
    end = text.find("\n- id:", start + len(marker))
    return text[start:] if end == -1 else text[start:end]


class BathroomMotionAutomationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = AUTOMATIONS.read_text()
        cls.motion = automation_block(source, "bathroom_motion_night_led")
        cls.bedside = automation_block(source, "bedroom_bilresa_remote")

    def test_motion_controls_only_the_bathroom_led_overnight(self):
        self.assertIn(
            "entity_id: binary_sensor.myggspray_wrlss_mtn_sensor_occupancy",
            self.motion,
        )
        self.assertIn('at: "22:00:00"', self.motion)
        self.assertIn("now().hour >= 22 or now().hour < 6", self.motion)
        self.assertIn("is_state('switch.bathroom_lamp', 'off')", self.motion)
        self.assertEqual(self.motion.count("entity_id: light.bathroom_led_bathroom"), 2)
        self.assertIn("action: light.turn_on", self.motion)
        self.assertIn("action: light.turn_off", self.motion)

    def test_bedside_off_branch_does_not_turn_off_bathroom_led(self):
        off_branch = self.bedside.split(
            "conditions: \"{{ trigger.id == 'turn_off' }}\"", 1
        )[1]
        self.assertNotIn("light.bathroom_led_bathroom", off_branch)
        night_on_branch = self.bedside.split(
            "conditions: \"{{ trigger.id == 'turn_on' and nighttime }}\"", 1
        )[1].split("conditions: \"{{ trigger.id == 'turn_on' }}\"", 1)[0]
        self.assertIn("light.bathroom_led_bathroom", night_on_branch)


if __name__ == "__main__":
    unittest.main()