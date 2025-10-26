import cv2
from threading import Thread, Lock
from time import sleep

class Camera:
    def __init__(self, index: int = 1):
        self._index = "http://192.168.1.7:8080/video"
        self._cap = None
        self._is_open = False
        self._frame = None
        self._frame_lock = Lock()  # Add thread safety
        self._running = False
        self._thread = None

    def start(self) -> bool:
        """Initialize and start the camera capture thread."""
        if self._is_open:
            return True

        self._cap = cv2.VideoCapture(self._index)
        if not self._cap.isOpened():
            self._is_open = False
            return False

        self._is_open = True
        self._running = True

        self._thread = Thread(target=self._frame_loop, daemon=True)
        self._thread.start()

        return True

    def stop(self):
        """Stop the camera and release resources."""
        self._running = False
        if self._cap:
            self._cap.release()
            self._cap = None
        self._is_open = False

    def _frame_loop(self):
        """Continuously capture frames while the camera is running."""
        while self._running and self._cap:
            success, frame = self._cap.read()
            if success:
                with self._frame_lock:
                    self._frame = frame
            else:
                # Try to reopen if frame capture fails
                sleep(0.5)
                self._cap.release()
                self._cap.open(self._index)
            sleep(0.02)  # Limit FPS (~50 FPS max)

    @property
    def frame(self):
        """Return the most recent frame captured."""
        with self._frame_lock:
            return self._frame.copy() if self._frame is not None else None

    @property
    def is_open(self) -> bool:
        """Return True if the camera is currently open."""
        return self._is_open