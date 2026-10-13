from pathlib import Path
import json
import subprocess
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
POPUP = ROOT / "config/dashboards/templates/button_cards/popups/hemma_popup_climate.yaml"
ROOM = ROOT / "config/dashboards/templates/button_cards/cards/hemma_room.yaml"


def yaml_js_block(text: str, marker: str) -> str:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == marker)
    marker_indent = len(lines[start]) - len(lines[start].lstrip())
    block = []
    for line in lines[start + 1:]:
        indent = len(line) - len(line.lstrip())
        if line.strip() and indent <= marker_indent:
            break
        block.append(line)
    body = textwrap.dedent("\n".join(block)).strip()
    assert body.startswith("[[[") and body.endswith("]]]")
    return body[3:-3]


class ClimatePopupTests(unittest.TestCase):
    def test_room_badges_pass_room_temperature_and_humidity_to_popup(self):
        room = ROOM.read_text()
        self.assertGreaterEqual(
            room.count("variables.aqi_entity_temp || variables.temp_sensor_1"), 6
        )
        self.assertGreaterEqual(
            room.count("variables.aqi_entity_humidity || variables.humidity_sensor"), 6
        )

    def test_non_air_quality_popup_uses_climate_title(self):
        popup = POPUP.read_text()
        title_line = next(
            line.strip() for line in popup.splitlines() if line.strip().startswith("title: ")
        )
        self.assertIn("device_class", title_line)
        self.assertIn("filter.climate", title_line)
        self.assertIn("Climate", title_line)

    def test_temperature_and_humidity_build_climate_hero_and_chart(self):
        popup = POPUP.read_text()
        body = yaml_js_block(popup, "content: |")
        script = f"""
          const states = {{
            'sensor.temp': {{state:'25.2', attributes:{{device_class:'temperature', unit_of_measurement:'°C'}}}},
            'sensor.humidity': {{state:'59.98', attributes:{{device_class:'humidity', unit_of_measurement:'%'}}}},
          }};
          const variables = {{
            room_name:'Bedroom', entity_quality:null,
            entity_temp:'sensor.temp', entity_humidity:'sensor.humidity', sensors:[]
          }};
          const entity = {{entity_id:'sensor.temp', state:'25.2', attributes:states['sensor.temp'].attributes}};
          const hass = {{locale:{{time_format:'24', language:'en'}}, localize:()=>null}};
          const window = {{_hemmaUI:{{
            hero:(x)=>({{kind:'hero', ...x}}),
            legend:(x)=>({{kind:'legend', items:x}}),
            group:(x)=>({{kind:'group', items:x}}),
          }}}};
          const popup = (function() {{ {body} }})();
          const metric = popup.cards[0].custom_fields.metric.card;
          const hero = metric.custom_fields.head;
          const chart = metric.custom_fields.chart.card;
          const result = {{hero, series: chart.series.map(x => x.entity)}};
          console.log(JSON.stringify(result));
        """
        result = subprocess.run(
            ["node", "-"], input=script, text=True, capture_output=True
        )
        self.assertEqual(0, result.returncode, result.stderr)
        built = json.loads(result.stdout)
        self.assertEqual("Climate", built["hero"]["label"])
        self.assertEqual("25°C · 60% humidity", built["hero"]["value"])
        self.assertEqual(["sensor.temp", "sensor.humidity"], built["series"])


if __name__ == "__main__":
    unittest.main()
