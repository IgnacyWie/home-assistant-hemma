from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "config/packages/kitchen_lights.yaml"
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
LIGHT_TEMPLATE = (
    ROOT
    / "config/dashboards/templates/button_cards/cards/hemma_light.yaml"
)


class KitchenSpotsDashboardGroupTests(unittest.TestCase):
    def test_spots_group_is_dashboard_only(self):
        dashboard = DASHBOARD.read_text()

        self.assertFalse(PACKAGE.exists())
        self.assertNotIn("light.kitchen_spots", dashboard)

    def test_spots_tile_controls_all_three_and_holds_for_members(self):
        dashboard = DASHBOARD.read_text()
        kitchen = dashboard.split(
            "  - type: custom:grid-layout\n    title: Kitchen", 1
        )[1].split("  - type: custom:grid-layout\n    title: Bedroom", 1)[0]
        spots = kitchen.split(
            "            entity: light.kitchen_1\n            name: Spots", 1
        )[1].split("          - type: custom:button-card", 1)[0]

        self.assertIn("icon: lightbulb-spot-v1", spots)
        self.assertIn("group_rooms: false", spots)
        self.assertIn("room_name: Spots", spots)
        for entity_id in (
            "light.kitchen_1",
            "light.2ch_wi_fi_switch_module_3_switch_1",
            "light.2ch_wi_fi_switch_module_3_switch_2",
        ):
            self.assertEqual(3, spots.count(entity_id))

        self.assertIn("active_entities:", spots)
        self.assertIn("lights:", spots)
        self.assertIn("service: >", spots)
        self.assertIn("return anyOn ? 'light.turn_off' : 'light.turn_on';", spots)
        self.assertIn("target:", spots)
        self.assertNotIn("hold_action:", spots)

    def test_light_template_counts_explicit_popup_members(self):
        template = LIGHT_TEMPLATE.read_text()

        self.assertIn("const configured = Array.isArray(variables.lights)", template)
        self.assertIn("configured.length ? configured : units", template)


if __name__ == "__main__":
    unittest.main()
