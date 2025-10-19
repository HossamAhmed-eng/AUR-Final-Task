import cv2
from threading import Thread
from time import sleep

class Camera:
    
    def __init__(self, index: int = 0):
        self._index = index
        self._cap = None
        self._is_open = False
        self._frame = None
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
        return self._frame

    @property
    def is_open(self) -> bool:
        """Return True if the camera is currently open."""
        return self._is_open
