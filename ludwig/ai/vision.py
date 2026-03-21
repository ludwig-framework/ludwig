"""
Ludwig AI - Computer vision for object detection and tracking
"""

from typing import Any, Callable, Optional
from dataclasses import dataclass
import time


@dataclass
class Detection:
    """A detected object."""
    label: str
    confidence: float
    box: tuple[int, int, int, int]  # x, y, width, height
    
    @property
    def center(self) -> tuple[int, int]:
        """Center point of the detection."""
        x, y, w, h = self.box
        return (x + w // 2, y + h // 2)


class Vision:
    """
    Computer vision for object detection.
    
    Example:
        vision = Vision(camera=0, model="yolo")
        
        @vision.on_detect("person")
        def person_detected(detection):
            print(f"Person at {detection.center}")
            robot.turn_to(detection.center)
        
        @vision.on_detect("cat")
        def cat_detected(detection):
            robot.say("Hello kitty!")
        
        vision.run()
    """
    
    MODELS = {
        "yolo": "yolov8n.pt",
        "yolo-small": "yolov8s.pt",
        "yolo-medium": "yolov8m.pt",
        "yolo-large": "yolov8l.pt",
    }
    
    def __init__(
        self,
        camera: int = 0,
        model: str = "yolo",
        confidence: float = 0.5,
    ):
        self.camera_index = camera
        self.model_name = model
        self.confidence_threshold = confidence
        
        self._camera = None
        self._model = None
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False
        self._target: Optional[Detection] = None
        
        self._init()
    
    def _init(self):
        """Initialize camera and model."""
        try:
            import cv2
            self._cv2 = cv2
            self._camera = cv2.VideoCapture(self.camera_index)
        except ImportError:
            print("[SIM] Vision (OpenCV not available)")
            self._cv2 = None
            self._camera = None
        
        try:
            from ultralytics import YOLO
            model_path = self.MODELS.get(self.model_name, self.model_name)
            self._model = YOLO(model_path)
        except ImportError:
            print("[SIM] Vision (YOLO not available)")
            self._model = None
    
    def capture(self):
        """Capture a frame from camera."""
        if self._camera is None:
            return None
        
        ret, frame = self._camera.read()
        return frame if ret else None
    
    def detect(self, frame=None) -> list[Detection]:
        """
        Run object detection on frame.
        
        Args:
            frame: Image frame (captures from camera if not provided)
        
        Returns:
            List of Detection objects
        """
        if frame is None:
            frame = self.capture()
        
        if frame is None or self._model is None:
            # Simulation mode - return fake detections
            import random
            if random.random() < 0.1:
                return [Detection(
                    label="person",
                    confidence=0.8,
                    box=(100, 100, 200, 400)
                )]
            return []
        
        results = self._model(frame, verbose=False)
        detections = []
        
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < self.confidence_threshold:
                    continue
                
                cls = int(box.cls[0])
                label = self._model.names[cls]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                detections.append(Detection(
                    label=label,
                    confidence=conf,
                    box=(x1, y1, x2 - x1, y2 - y1)
                ))
        
        return detections
    
    def find(self, label: str, frame=None) -> Optional[Detection]:
        """Find a specific object."""
        detections = self.detect(frame)
        for det in detections:
            if det.label == label:
                return det
        return None
    
    @property
    def target(self) -> Optional[Detection]:
        """Current tracked target."""
        return self._target
    
    def track(self, label: str):
        """Start tracking an object type."""
        self._tracking_label = label
    
    # === Events ===
    
    def on(self, event: str):
        """Register event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    def on_detect(self, label: str):
        """
        Handler for when specific object is detected.
        
        Example:
            @vision.on_detect("person")
            def handle(detection):
                print(f"Person: {detection.confidence}")
        """
        return self.on(f"detect:{label}")
    
    # === Run Loop ===
    
    def run(self, display: bool = False):
        """
        Start vision processing loop.
        
        Args:
            display: Show video window with detections
        """
        self._running = True
        print("👁️  Vision processing started...")
        
        try:
            while self._running:
                frame = self.capture()
                detections = self.detect(frame)
                
                # Trigger callbacks for each detection
                for det in detections:
                    event = f"detect:{det.label}"
                    for handler in self._callbacks.get(event, []):
                        handler(det)
                    
                    # Also trigger generic "detect" event
                    for handler in self._callbacks.get("detect", []):
                        handler(det)
                
                # Update tracked target
                if hasattr(self, '_tracking_label'):
                    self._target = self.find(self._tracking_label)
                
                # Display window
                if display and self._cv2 and frame is not None:
                    for det in detections:
                        x, y, w, h = det.box
                        self._cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        self._cv2.putText(frame, f"{det.label}: {det.confidence:.2f}",
                                         (x, y-10), self._cv2.FONT_HERSHEY_SIMPLEX,
                                         0.5, (0, 255, 0), 2)
                    
                    self._cv2.imshow('Ludwig Vision', frame)
                    if self._cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                time.sleep(0.033)  # ~30 FPS
                
        except KeyboardInterrupt:
            print("\n👁️  Vision stopped")
        finally:
            self.release()
    
    def stop(self):
        """Stop vision processing."""
        self._running = False
    
    def release(self):
        """Release resources."""
        if self._camera:
            self._camera.release()
        if self._cv2:
            self._cv2.destroyAllWindows()
    
    def __repr__(self):
        return f"Vision(camera={self.camera_index}, model={self.model_name})"
