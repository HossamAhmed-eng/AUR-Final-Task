from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QApplication
)
from PySide6.QtCore import Qt

from Robot.gui.camera_display import CameraWidget
from Robot.gui.coordinates_display import CoordinatesDisplay
from Robot.gui.target_coords_display import TargetCoordsDisplay
from Robot.core.comm.client import setup
import Robot.core.comm.sub.coords as coords


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(900, 600)  #  Larger for three displays
        self.setWindowTitle("Robot Control Panel")

   
        self.camera = CameraWidget()
        self.camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
      
        self.coords_display = CoordinatesDisplay()
        
        
        self.target_display = TargetCoordsDisplay()


        container = QWidget()
        main_layout = QVBoxLayout(container)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.coords_display, 1)    # Current position
        status_layout.addWidget(self.target_display, 1)    # Target position
        
        header_layout = QHBoxLayout()
        header_layout.addLayout(status_layout)
        header_layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.camera)

        self.setCentralWidget(container)
        
        #Setup connection
        setup(self.coords_display.update_coordinates)
        
        # Connect camera to target display
        self.camera.target_coordinates_received.connect(self.target_display.update_target_coordinates)
        self.camera.qr_status_update.connect(self.target_display.update_status)

        self.show()

    def resizeEvent(self, event):
        new_width = self.width()
        font = QFont("Consolas", int(new_width / 50), QFont.Bold)
        self.coords_display.setFont(font)
        super().resizeEvent(event)