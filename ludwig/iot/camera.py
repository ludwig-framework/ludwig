"""
Ludwig IoT - Camera for security and vision
"""

from typing import Any, Callable, Optional
from dataclasses import dataclass
import time


@dataclass
class Frame:
    """Video frame."""
    data: bytes
    width: int
    height: int
    timestamp: float


class Camera:
    """
    Camera for security and computer vision.
    
    Example:
        cam = Camera(resolution="1080p")
        
        # Take a photo
        photo = cam.capture()
        cam.save(photo, "snapshot.jpg")
        
        # Record video
        clip = cam.record(seconds=30)
        
        # Motion detection
        @cam.on_motion
        def handle_motion():
            clip = cam.record(seconds=10)
            storage.save(clip)
            cam.notify("Motion detected!")
        
        cam.run()
    """
    
    RESOLUTIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }
    
    def __init__(
        self,
        index: int = 0,
        resolution: str = "720p",
        fps: int = 30,
        name: str = None,
    ):
        self.index = index
        self.resolution = resolution
        self.fps = fps
        self.name = name or f"camera_{index}"
        
        self._width, self._height = self.RESOLUTIONS.get(resolution, (1280, 720))
        self._camera = None
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False
        self._motion_threshold = 5000
        self._last_frame = None
        
        self._init_camera()
    
    def _init_camera(self):
        """Initialize camera hardware."""
        try:
            import cv2
            self._camera = cv2.VideoCapture(self.index)
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
            self._camera.set(cv2.CAP_PROP_FPS, self.fps)
            self._cv2 = cv2
        except ImportError:
            print(f"[SIM] Camera {self.name} (OpenCV not available)")
            self._camera = None
            self._cv2 = None
    
    def capture(self) -> Optional[Frame]:
        """Capture a single frame."""
        if self._camera is None:
            # Simulation mode
            return Frame(
                data=b"",
                width=self._width,
                height=self._height,
                timestamp=time.time()
            )
        
        ret, frame = self._camera.read()
        if not ret:
            return None
        
        _, buffer = self._cv2.imencode('.jpg', frame)
        return Frame(
            data=buffer.tobytes(),
            width=self._width,
            height=self._height,
            timestamp=time.time()
        )
    
    def record(self, seconds: float = 10, filename: str = None) -> bytes:
        """
        Record video for specified duration.
        
        Returns video data or saves to file.
        """
        filename = filename or f"recording_{int(time.time())}.mp4"
        frames = []
        start = time.time()
        
        print(f"🎬 Recording for {seconds}s...")
        
        while time.time() - start < seconds:
            frame = self.capture()
            if frame:
                frames.append(frame)
            time.sleep(1 / self.fps)
        
        # Save video
        if self._cv2 and frames:
            fourcc = self._cv2.VideoWriter_fourcc(*'mp4v')
            out = self._cv2.VideoWriter(filename, fourcc, self.fps, (self._width, self._height))
            
            for frame in frames:
                img = self._cv2.imdecode(
                    __import__('numpy').frombuffer(frame.data, dtype='uint8'),
                    self._cv2.IMREAD_COLOR
                )
                out.write(img)
            
            out.release()
        
        print(f"🎬 Recorded {len(frames)} frames to {filename}")
        return filename
    
    def save(self, frame: Frame, filename: str):
        """Save a frame to file."""
        with open(filename, 'wb') as f:
            f.write(frame.data)
    
    def stream(self):
        """Generator that yields frames."""
        while True:
            frame = self.capture()
            if frame:
                yield frame
            time.sleep(1 / self.fps)
    
    # === Motion Detection ===
    
    def detect_motion(self, frame: Frame) -> bool:
        """Simple motion detection by comparing frames."""
        if self._last_frame is None:
            self._last_frame = frame
            return False
        
        if self._cv2 is None:
            return False
        
        import numpy as np
        
        # Decode frames
        curr = self._cv2.imdecode(np.frombuffer(frame.data, dtype='uint8'), 0)
        prev = self._cv2.imdecode(np.frombuffer(self._last_frame.data, dtype='uint8'), 0)
        
        # Calculate difference
        diff = self._cv2.absdiff(curr, prev)
        motion = np.sum(diff)
        
        self._last_frame = frame
        return motion > self._motion_threshold
    
    # === Events ===
    
    def on(self, event: str):
        """Register event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    @property
    def on_motion(self):
        """Handler for motion detection."""
        return self.on("motion")
    
    # === Notifications ===
    
    def notify(self, message: str, with_snapshot: bool = False):
        """Send notification."""
        print(f"📸 Camera notification: {message}")
        if with_snapshot:
            frame = self.capture()
            if frame:
                filename = f"alert_{int(time.time())}.jpg"
                self.save(frame, filename)
                print(f"   Snapshot: {filename}")
    
    # === Run Loop ===
    
    def run(self, detect_motion: bool = True):
        """Start camera loop with motion detection."""
        self._running = True
        print(f"📷 {self.name} monitoring...")
        
        try:
            while self._running:
                frame = self.capture()
                
                if detect_motion and frame and self.detect_motion(frame):
                    for handler in self._callbacks.get("motion", []):
                        handler()
                
                time.sleep(1 / self.fps)
        except KeyboardInterrupt:
            print(f"\n📷 {self.name} stopped")
        finally:
            self.release()
    
    def stop(self):
        """Stop the camera."""
        self._running = False
    
    def release(self):
        """Release camera resources."""
        if self._camera:
            self._camera.release()
    
    def __repr__(self):
        return f"Camera(index={self.index}, resolution={self.resolution})"
