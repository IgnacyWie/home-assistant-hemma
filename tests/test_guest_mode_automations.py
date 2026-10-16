from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "config/packages/guest_mode.yaml"
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
ROOM_TEMPLATE = ROOT / "config/dashboards/templates/button_cards/cards/hemma_room.yaml"
BADGE_TEMPLATE = ROOT / "config/dashboards/templates/button_cards/badges/hemma_badge_guest_mode.yaml"


def _automations_by_id() -> dict[str, dict]:
    package = yaml.safe_load(PACKAGE.read_text())
    return {automation["id"]: automation for automation in package["automation"]}


def test_guest_mode_restores_and_guards_shared_leave_home_routine() -> None:
    package = yaml.safe_load(PACKAGE.read_text())
    guest = package["input_boolean"]["guest_mode"]
    assert "initial" not in guest

    automation = _automations_by_id()["guest_mode_leave_when_phone_disconnects"]
    assert automation["triggers"] == [
        {
            "trigger": "state",
            "entity_id": "sensor.ignacy_wi_fi_presence",
            "from": "home",
            "to": "not_home",
        }
    ]
    assert automation["conditions"] == [
        {
            "condition": "state",
            "entity_id": "input_boolean.guest_mode",
            "state": "off",
        }
    ]
    assert automation["actions"] == [
        {
            "action": "script.turn_on",
            "target": {"entity_id": "script.leave_home"},
        }
    ]


def test_wifi_reconnect_never_turns_lights_on() -> None:
    automations = _automations_by_id()
    assert "welcome_home_when_ignacy_reconnects_before_23" not in automations


def test_welcome_home_runs_twenty_minutes_before_sunset_only_when_home() -> None:
    automation = _automations_by_id()["welcome_home_twenty_minutes_before_sunset"]
    assert automation["triggers"] == [
        {"trigger": "sun", "event": "sunset", "offset": "-00:20:00"}
    ]
    assert automation["conditions"] == [
        {
            "condition": "state",
            "entity_id": "sensor.ignacy_wi_fi_presence",
            "state": "home",
        }
    ]
    assert automation["actions"] == [
        {
            "action": "scene.turn_on",
            "target": {"entity_id": "scene.welcome_home"},
        }
    ]


def test_home_dashboard_exposes_guest_mode_as_one_toggle_chip() -> None:
    dashboard = DASHBOARD.read_text()
    room_template = ROOM_TEMPLATE.read_text()
    badge = BADGE_TEMPLATE.read_text()

    assert dashboard.count("guest_mode_entity: input_boolean.guest_mode") == 1
    assert room_template.count("template: hemma_badge_guest_mode") == 1
    assert "service: input_boolean.toggle" in badge
    assert "var(--hemma-color-blue, #0A84FF)" in badge
    assert "background: var(--badge-background" in badge
    assert (ROOT / "config/www/hemma/icons/person.svg").is_file()
