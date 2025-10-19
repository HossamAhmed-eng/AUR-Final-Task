from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QApplication
)
from PySide6.QtCore import Qt

from Robot.gui.camera_display import CameraWidget
from Robot.gui.coordinates_display import CoordinatesDisplay
from Robot.core.comm.client import setup
import Robot.core.comm.sub.coords as coords


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)
        self.setWindowTitle("Robot Control Panel")

        # --- Camera widget ---
        self.camera = CameraWidget()
        self.camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore
        
        # --- Coordinates & connection display ---
        self.coords_display = CoordinatesDisplay()


        # --- Layout setup ---
        container = QWidget()
        main_layout = QVBoxLayout(container)
        header_layout = QHBoxLayout()
        setup(self.coords_display.update_coordinates)

        header_layout.addWidget(self.coords_display)
        header_layout.setAlignment(Qt.AlignTop) # type: ignore

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.camera)

        self.setCentralWidget(container)
        self.show()

    def resizeEvent(self, event):
        new_width = self.width()
        font = QFont("Consolas", int(new_width / 40), QFont.Bold) # type: ignore
        self.coords_display.setFont(font)
        super().resizeEvent(event)
