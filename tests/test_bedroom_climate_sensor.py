from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "config/dashboards/hemma/hemma.yaml"


class BedroomClimateSensorTests(unittest.TestCase):
    def test_timmerflotte_temperature_and_humidity_are_only_in_bedroom(self):
        dashboard = DASHBOARD.read_text()
        bedroom = dashboard.split(
            "  - type: custom:grid-layout\n    title: Bedroom", 1
        )[1].split("  - type: custom:grid-layout\n    title: Bathroom", 1)[0]

        temperature = "sensor.timmerflotte_temp_hmd_sensor_temperature"
        humidity = "sensor.timmerflotte_temp_hmd_sensor_humidity"

        self.assertEqual(1, dashboard.count(temperature))
        self.assertEqual(1, dashboard.count(humidity))
        self.assertIn(f"temp_sensor_1: {temperature}", bedroom)
        self.assertIn(f"humidity_sensor: {humidity}", bedroom)
        self.assertIn("temp_unit: 'C'", bedroom)


if __name__ == "__main__":
    unittest.main()
