"""
Computer Vision Example
Requires: pip install ludwig[vision]
"""

from ludwig.ai import Vision

vision = Vision(camera=0, model="yolo")


@vision.on_detect("person")
def person_detected(detection):
    print(f"👤 Person at {detection.center} ({detection.confidence:.2%})")


@vision.on_detect("cat")
def cat_spotted(detection):
    print(f"🐱 Cat spotted!")


if __name__ == "__main__":
    print("👁️ Computer Vision")
    vision.run(display=True)
