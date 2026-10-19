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
        cls.bathroom = automation_block(source, "bathroom_motion_night_led")
        cls.kitchen = automation_block(source, "kitchen_motion_after_sunset_light")
        cls.bedside = automation_block(source, "bedroom_bilresa_remote")

    def test_bathroom_motion_uses_sunset_offset_through_sunrise(self):
        self.assertIn(
            "entity_id: binary_sensor.myggspray_wrlss_mtn_sensor_occupancy",
            self.bathroom,
        )
        self.assertIn('offset: "-00:20:00"', self.bathroom)
        self.assertIn("event: sunrise", self.bathroom)
        self.assertIn('after_offset: "-00:20:00"', self.bathroom)
        self.assertIn("before: sunrise", self.bathroom)
        self.assertNotIn('at: "22:00:00"', self.bathroom)
        self.assertNotIn("now().hour >= 22 or now().hour < 6", self.bathroom)
        self.assertIn("is_state('switch.bathroom_lamp', 'off')", self.bathroom)
        self.assertEqual(self.bathroom.count("entity_id: light.bathroom_led_bathroom"), 2)
        self.assertIn("action: light.turn_on", self.bathroom)
        self.assertIn("action: light.turn_off", self.bathroom)

    def test_kitchen_motion_uses_the_same_sunset_offset_through_sunrise_window(self):
        self.assertIn(
            "entity_id: binary_sensor.kitchen_kitchen_motion_sensor_occupancy",
            self.kitchen,
        )
        self.assertIn('offset: "-00:20:00"', self.kitchen)
        self.assertIn("event: sunrise", self.kitchen)
        self.assertIn('after_offset: "-00:20:00"', self.kitchen)
        self.assertIn("before: sunrise", self.kitchen)
        self.assertNotIn("is_state('sun.sun', 'below_horizon')", self.kitchen)
        self.assertEqual(
            self.kitchen.count(
                "entity_id: light.kitchen_shelly2pmg4_d885ace4f060_output_1"
            ),
            2,
        )


    def test_bedside_remote_does_not_control_bathroom_led(self):
        self.assertNotIn("light.bathroom_led_bathroom", self.bedside)
        night_on_branch = self.bedside.split(
            "conditions: \"{{ trigger.id == 'turn_on' and nighttime }}\"", 1
        )[1].split("conditions: \"{{ trigger.id == 'turn_on' }}\"", 1)[0]
        self.assertIn("light.3_in_1_controller_wifi_2_4g", night_on_branch)
        self.assertIn("light.bedroom_ikea_of_sweden_grillplats_plug", night_on_branch)
        self.assertIn("light.bedroom_accent_bedroom", night_on_branch)


if __name__ == "__main__":
    unittest.main()