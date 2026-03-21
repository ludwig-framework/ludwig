"""
Garden Automation Example
"""

from ludwig.iot import Garden

garden = Garden()

garden.add_plant("tomatoes", moisture_pin=0, pump_pin=17, threshold=30)
garden.add_plant("herbs", moisture_pin=1, pump_pin=18, threshold=40)


@garden.check_every(hours=1)
def hourly_check(plant):
    if plant.needs_water:
        plant.water(seconds=10)
        garden.log(f"Watered {plant.name}")


@garden.at("06:00")
def morning_report():
    for plant in garden.plants:
        print(f"{plant.name}: {plant.moisture}%")


if __name__ == "__main__":
    print("🌿 Garden Automation")
    garden.run()
