"""
Smart Home Example
"""

from ludwig.iot import Home, Light, Sensor

home = Home()

living = home.room("living_room")
living.add(Light(pin=17, name="ceiling", dimmable=True))
living.add(Sensor.motion(pin=4))

bedroom = home.room("bedroom")
bedroom.add(Light(pin=18, name="main"))


@home.at("sunset")
def evening_mode():
    living.light("ceiling").on()
    living.light("ceiling").brightness(70)


@home.at("23:00")
def bedtime():
    home.all_lights_off()


@home.when(lambda: living.motion.read())
def motion_light():
    if not living.light("ceiling").is_on:
        living.light("ceiling").on()


if __name__ == "__main__":
    print("🏠 Smart Home System")
    home.run()
