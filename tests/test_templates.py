"""Compile CLI templates and cover the APIs they use."""

import ast
import os
import subprocess
import tempfile

from ludwig.ai import Assistant
from ludwig.cli import create_project
from ludwig.core import App
from ludwig.iot import Light, Relay, Sensor
from ludwig.iot.alarm import Alarm
import ludwig.cli as cli


def test_all_cli_templates_parse():
    templates = [
        value
        for name, value in vars(cli).items()
        if name.startswith("TEMPLATE_") and isinstance(value, str)
    ]
    assert len(templates) >= 10
    for code in templates:
        ast.parse(code)


def test_generated_projects_parse():
    with tempfile.TemporaryDirectory() as tmpdir:
        for template in (
            "basic",
            "api",
            "chatbot",
            "door-lock",
            "led",
            "weather-station",
        ):
            path = os.path.join(tmpdir, template)
            create_project(path, template)
            with open(os.path.join(path, "app.py")) as f:
                ast.parse(f.read())


def test_assistant_ask_alias():
    assistant = Assistant(name="Bot")
    reply = assistant.ask("hello")
    assert isinstance(reply, str)
    assert len(reply) > 0


def test_light_rgb_template_api():
    led = Light(pin=18, type="ws2812b", count=60)
    led.set_color(255, 0, 0)
    led.set_brightness(50)
    led.effect("rainbow")
    assert led.is_on
    assert led._color == (255, 0, 0)
    assert led._brightness == 50
    assert led.count == 60


def test_sensor_hardware_aliases():
    temperature = Sensor("dht22", pin=4)
    humidity = Sensor("dht22", pin=4, reading="humidity")
    pressure = Sensor("bmp280", pin=5)
    light = Sensor("ldr", pin=6)

    assert temperature.sensor_type == "temperature"
    assert humidity.sensor_type == "humidity"
    assert pressure.sensor_type == "pressure"
    assert light.sensor_type == "light"
    assert isinstance(temperature.read(), (int, float))
    assert isinstance(humidity.read(), (int, float))
    assert isinstance(pressure.read(), (int, float))
    assert isinstance(light.read(), (int, float))


def test_relay_is_on_property():
    lock = Relay(pin=11)
    assert lock.is_on is False
    lock.on()
    assert lock.is_on is True


def test_app_sunset_normalizes_to_clock_time():
    app = App()

    @app.at("sunset")
    def evening():
        pass

    interval, func = app._tasks[0]
    assert interval == "at:sunset"
    assert func is evening


def test_cli_version():
    result = subprocess.run(
        ["python", "-m", "ludwig.cli", "version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Ludwig" in result.stdout


def test_alarm_pin():
    alarm = Alarm(code="1234")
    alarm.exit_delay = 0
    alarm.arm()
    assert alarm.disarm("0000") is False
    assert alarm.is_armed
    assert alarm.disarm("1234") is True
    assert not alarm.is_armed
