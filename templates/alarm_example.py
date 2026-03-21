"""
Security Alarm Example
"""

from ludwig.iot import Alarm, Sensor

alarm = Alarm()

alarm.add(Sensor.motion(pin=4), zone="living_room")
alarm.add(Sensor.door(pin=5), zone="front_door")
alarm.add(Sensor.window(pin=6), zone="bedroom")

alarm.siren(pin=17)


@alarm.on_triggered
def handle_alert(zone, sensor):
    print(f"🚨 ALERT: {zone}!")
    # alarm.send_sms("+1234567890", f"Alert in {zone}")


if __name__ == "__main__":
    print("🔒 Security Alarm System")
    alarm.arm()
    alarm.run()
