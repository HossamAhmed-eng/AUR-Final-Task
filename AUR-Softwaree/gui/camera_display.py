import cv2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy,QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from cv_project import Camera  


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        
        self.camera_device = Camera()
        self.is_camera_on = False

       
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.start_btn = QPushButton("Start Camera")
        self.info_label = QLabel("Status: OFF")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; color: gray;")

        
        layout = QVBoxLayout()
        layout.addWidget(self.label, stretch=3)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

      
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        
        self.start_btn.clicked.connect(self.toggle_camera)

       
        self._show_placeholder()


    def toggle_camera(self):
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
        frame = self.camera_device.frame
        if frame is None:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimage = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # Scale while keeping aspect ratio
        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )


    def _show_placeholder(self):
        cat_img = cv2.imread("cat.jpg")  
        if cat_img is None:
            self.label.setText("Camera Off")
            return

        cat_img = cv2.cvtColor(cat_img, cv2.COLOR_BGR2RGB)
        h, w, ch = cat_img.shape
        bytes_per_line = ch * w
        qimage = QImage(cat_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        
if __name__ == "__main__":
    app = QApplication()
    w = CameraWidget()
    w.setWindowTitle("Camera")
    w.resize(1000, 600)
    w.show()
    app.exec()