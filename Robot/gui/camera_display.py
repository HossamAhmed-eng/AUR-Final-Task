import os
import cv2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap

from Robot.core.cv import Camera  
  
class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.camera_device = Camera()
        self.is_camera_on = False

        # --- UI Elements ---
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter) # type: ignore
        self.label.setStyleSheet("background-color: black;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore

        self.start_btn = QPushButton("Start Camera")
        self.info_label = QLabel("Status: OFF")
        self.info_label.setAlignment(Qt.AlignCenter) # type: ignore
        self.info_label.setStyleSheet("font-size: 14px; color: gray;")

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(self.label, stretch=3)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.info_label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        # --- Timer for updating camera frames ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # --- Button connections ---
        self.start_btn.clicked.connect(self.toggle_camera)

        # --- Initial placeholder image ---
        self._show_placeholder()

    def toggle_camera(self):
        """Start or stop the camera feed."""
        if not self.is_camera_on:
            if not self.camera_device.start():
                self.label.setText("❌ Failed to open camera")
                self.info_label.setText("Status: ERROR")
                return

            self.is_camera_on = True
            self.start_btn.setText("Stop Camera")
            self.info_label.setText("Status: ON")
            self.timer.start(30)
        else:
            self.is_camera_on = False
            self.timer.stop()
            self.camera_device.stop()
            self.start_btn.setText("Start Camera")
            self.info_label.setText("Status: OFF")
            self._show_placeholder()

    def update_frame(self):
        """Fetch the latest frame from the camera and display it."""
        frame = self.camera_device.frame
        if frame is None:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimage = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888) # type: ignore
        pixmap = QPixmap.fromImage(qimage)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.IgnoreAspectRatio, # type: ignore
                Qt.SmoothTransformation # type: ignore
            )
        )
       

    def _show_placeholder(self):
        """Display a static placeholder image or text when the camera is off."""
        placeholder_path = os.path.join(os.path.dirname(__file__), "pic.jpg")
        pic_img = cv2.imread(placeholder_path)

        if pic_img is None:
            self.label.setText("Camera Off")
            return

        pic_img = cv2.cvtColor(pic_img, cv2.COLOR_BGR2RGB)
        h, w, ch = pic_img.shape
        bytes_per_line = ch * w
        qimage = QImage(pic_img.data, w, h, bytes_per_line, QImage.Format_RGB888) # type: ignore
        pixmap = QPixmap.fromImage(qimage)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.IgnoreAspectRatio, # type: ignore
                Qt.SmoothTransformation # type: ignore
            )
        )
        