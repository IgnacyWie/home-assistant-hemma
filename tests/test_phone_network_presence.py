from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "config/packages/phone_network_presence.yaml"
SCRIPT = ROOT / "config/shell/network_presence.sh"
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"
TARGET_ENTITY = "sensor.ignacy_wi_fi_presence"
PRIVATE_MAC_PATH = "/config/private/ignacy_phone_wifi_mac"


def test_wifi_presence_package_is_private_and_bounded() -> None:
    package = yaml.safe_load(PACKAGE.read_text())
    sensor = package["command_line"][0]["sensor"]

    assert sensor["unique_id"] == "ignacy_wifi_presence"
    assert sensor["scan_interval"] == 60
    assert sensor["command_timeout"] == 45
    assert PRIVATE_MAC_PATH in sensor["command"]

    script = SCRIPT.read_text()
    assert "192.168.1.0/24" in script
    assert "nmap -n -sn -PR" in script
    assert "printf 'home\\n'" in script
    assert "printf 'not_home\\n'" in script


def test_home_presence_chip_uses_wifi_presence_sensor_once() -> None:
    dashboard = DASHBOARD.read_text()
    home_block = dashboard.split("  - type: custom:grid-layout", 2)[1]

    assert home_block.count(f"presence_entity_1: {TARGET_ENTITY}") == 1
    assert "presence_entity_1: person.ignacy_wie" not in home_block
    assert dashboard.count(TARGET_ENTITY) == 1


def test_private_phone_mac_is_not_committed() -> None:
    repository_text = "\n".join(
        path.read_text(errors="ignore")
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )

    colon_mac = ":".join(("22", "A4", "04", "B1", "C7", "97"))
    compact_mac = "".join(("22", "A4", "04", "B1", "C7", "97"))
    assert colon_mac not in repository_text
    assert compact_mac not in repository_text
