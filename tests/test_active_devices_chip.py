from pathlib import Path
import re
import subprocess
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ROOM_TEMPLATE = ROOT / "config/dashboards/templates/button_cards/cards/hemma_room.yaml"
TEMPLATE = ROOT / "config/dashboards/templates/button_cards/badges/hemma_badge_active_devices.yaml"

ACTIVE_DEVICE_IDS = {
    "light.bedroom_accent_bedroom",
    "light.living_room_accent_1",
    "light.living_room_2ch_wi_fi_switch_module_switch_2",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_1",
    "light.living_room_2ch_wi_fi_switch_module_2_switch_2",
    "light.living_room_2ch_wi_fi_switch_module_switch_1",
    "light.living_room_balcony",
    "light.3_in_1_controller_wifi_2_4g",
    "light.bedroom_ikea_of_sweden_grillplats_plug",
    "switch.ikea_of_sweden_grillplats_plug_2",
    "fan.bathroom_fan_bathroom",
    "media_player.zeppelin",
    "media_player.living_room_tv_2",
}


class ActiveDevicesChipTests(unittest.TestCase):
    def test_home_replaces_leave_home_chip_and_temporary_cards(self):
        dashboard = DASHBOARD.read_text()
        room_template = ROOM_TEMPLATE.read_text()
        home_view = dashboard.split("  - type: custom:grid-layout\n    title: Living Room", 1)[0]

        self.assertIn("active_devices_enabled: true", home_view)
        self.assertIn("template: hemma_badge_active_devices", room_template)
        self.assertNotIn("scene_label_2: Leave Home", home_view)
        self.assertNotIn("type: conditional", home_view)

    def test_chip_covers_the_exact_leave_home_allowlist(self):
        dashboard = DASHBOARD.read_text()
        configured = set(re.findall(r"active_device_entity_\d+:\s+([^\s#]+)", dashboard))
        self.assertEqual(ACTIVE_DEVICE_IDS, configured)

    def test_chip_has_live_summary_individual_controls_and_all_off(self):
        template = TEMPLATE.read_text()

        self.assertIn("Everything off", template)
        self.assertNotIn("leaving_entity", template)
        self.assertIn("enabled && configured.length && active", template)
        self.assertIn("devices on", template)
        self.assertIn("lights on", template)
        self.assertIn("What's still on?", template)
        self.assertIn("service: 'script.turn_on'", template)
        self.assertIn("all_off_entity: script.leave_home", template)
        self.assertIn("service: 'homeassistant.turn_off'", template)
        self.assertGreaterEqual(template.count("triggers_update: all"), 1)
        self.assertIn("hidden:", template)

    def test_popup_and_summary_javascript_parse(self):
        template = TEMPLATE.read_text()

        def yaml_block(marker):
            lines = template.splitlines()
            start = next(i for i, line in enumerate(lines) if line.strip() == marker)
            marker_indent = len(lines[start]) - len(lines[start].lstrip())
            block = []
            for line in lines[start + 1:]:
                indent = len(line) - len(line.lstrip())
                if line.strip() and indent <= marker_indent:
                    break
                block.append(line)
            body = textwrap.dedent("\n".join(block)).strip()
            self.assertTrue(body.startswith("[[[") and body.endswith("]]]"))
            return body[3:-3]

        for marker in ("content: |", "name: |"):
            result = subprocess.run(
                ["node", "--check", "-"],
                input=f"function validate() {{\n{yaml_block(marker)}\n}}\n",
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
