from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "config/automations.yaml"


class CorridorBilresaAutomationTests(unittest.TestCase):
    def test_buttons_map_to_home_modes(self):
        source = AUTOMATIONS.read_text()
        automation = source.split("- id: 'corridor_bilresa_home_modes'", 1)[1]
        self.assertIn("entity_id: event.bilresa_dual_button_button_1", automation)
        self.assertIn("entity_id: event.bilresa_dual_button_button_2", automation)
        self.assertIn("id: welcome_home", automation)
        self.assertIn("id: leave_home", automation)
        self.assertIn("entity_id: scene.welcome_home", automation)
        self.assertIn("entity_id: script.leave_home", automation)


if __name__ == "__main__":
    unittest.main()