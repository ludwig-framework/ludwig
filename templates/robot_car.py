"""
Robot Car Example - Obstacle avoidance robot
"""

from ludwig.iot import Robot, Sensor

robot = Robot.car(
    left={"forward": 17, "backward": 18, "enable": 12},
    right={"forward": 22, "backward": 23, "enable": 13},
)

robot.add_sensor("front", Sensor.ultrasonic(trigger=24, echo=25))


@robot.on_obstacle
def avoid_obstacle():
    print("🚧 Obstacle detected!")
    robot.stop()
    robot.backward(duration=0.5)
    robot.turn(90)
    robot.forward()


if __name__ == "__main__":
    print("🤖 Robot Car Starting...")
    robot.forward(speed=50)
    robot.run(obstacle_distance=20)
