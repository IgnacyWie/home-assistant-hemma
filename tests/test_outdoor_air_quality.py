from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "config/packages/open_meteo_air_quality.yaml"
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"


class OutdoorAirQualityTests(unittest.TestCase):
    def test_package_uses_home_location_without_api_key(self):
        package = PACKAGE.read_text()
        self.assertIn("air-quality-api.open-meteo.com/v1/air-quality", package)
        self.assertIn("state_attr('zone.home', 'latitude')", package)
        self.assertIn("state_attr('zone.home', 'longitude')", package)
        self.assertNotIn("api_key", package.lower())
        self.assertIn("scan_interval: 1800", package)

    def test_package_exposes_aqi_and_particulate_sensors(self):
        package = PACKAGE.read_text()
        for unique_id in (
            "open_meteo_european_aqi",
            "open_meteo_pm2_5",
            "open_meteo_pm10",
            "outdoor_air_quality",
        ):
            self.assertEqual(1, package.count(f"unique_id: {unique_id}"))
        for category in ("good", "fair", "moderate", "poor", "very poor", "bad"):
            self.assertIn(category, package)

    def test_air_quality_is_bound_only_to_home_view(self):
        dashboard = DASHBOARD.read_text()
        home_start = dashboard.index("title: Home")
        living_room_start = dashboard.index("title: Living Room", home_start)
        home = dashboard[home_start:living_room_start]
        bindings = (
            "quality_sensor: sensor.outdoor_air_quality",
            "aqi_entity_pm25: sensor.open_meteo_pm2_5",
            "aqi_entity_pm10: sensor.open_meteo_pm10",
            "aqi_room_name: Outdoor",
        )
        for binding in bindings:
            self.assertEqual(1, dashboard.count(binding))
            self.assertIn(binding, home)

        bedroom_start = dashboard.index("title: Bedroom")
        bathroom_start = dashboard.index("title: Bathroom", bedroom_start)
        bedroom = dashboard[bedroom_start:bathroom_start]
        for binding in bindings:
            self.assertNotIn(binding, bedroom)


if __name__ == "__main__":
    unittest.main()
