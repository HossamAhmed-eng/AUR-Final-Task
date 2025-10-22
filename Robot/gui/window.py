from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QApplication
)
from PySide6.QtCore import Qt, Slot

from Robot.gui.camera_display import CameraWidget
from Robot.gui.coordinates_display import CoordinatesDisplay
from Robot.gui.target_coords_display import TargetCoordsDisplay
from Robot.gui.area_coords import AreaCalibrationWidget
from Robot.core.comm.client import setup
import Robot.core.comm.sub.coords as coords


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 700)
        self.setWindowTitle("Robot Control Panel")

        # Widgets
        self.camera = CameraWidget()
        self.camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore

        self.coords_display = CoordinatesDisplay()
        self.target_display = TargetCoordsDisplay()
        self.area_calibration = AreaCalibrationWidget()

        # Central container
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Status layout (top section)
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.coords_display, 1)
        status_layout.addWidget(self.target_display, 1)
        status_layout.addWidget(self.area_calibration, 1)

        # Make the top section flexible but smaller than camera
        self.coords_display.setMaximumHeight(int(self.height() * 0.25))
        self.target_display.setMaximumHeight(int(self.height() * 0.25))
        self.area_calibration.setMaximumHeight(int(self.height() * 0.25))

        # Add layouts with stretch ratio 1 : 2
        main_layout.addLayout(status_layout, 1)
        main_layout.addWidget(self.camera, 2)

        self.setCentralWidget(container)

        # Setup coordinate update connection
        def handle_coordinate_update(x: float, y: float):
            """Forward coordinates to both displays"""
            self.coords_display.update_coordinates(x, y)
            self.area_calibration.update_current_coordinates(x, y)

        setup(handle_coordinate_update)

        # Connect signals
        self.camera.target_coordinates_received.connect(
            self.target_display.update_target_coordinates
        )
        self.camera.qr_status_update.connect(
            self.target_display.update_status
        )
        self.area_calibration.coordinates_updated.connect(self.on_area_calibrated)

        self.show()

    @Slot(list)
    def on_area_calibrated(self, coordinates):
        """Handle when area calibration is complete"""
        print(f"✅ Area calibrated with points: {coordinates}")

    def resizeEvent(self, event):
        """Adjust font size dynamically"""
        new_width = self.width()
        font = QFont("Consolas", int(new_width / 50), QFont.Bold) # type: ignore
        self.coords_display.setFont(font)
        super().resizeEvent(event)
