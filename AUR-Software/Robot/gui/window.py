from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QPushButton
)
from PySide6.QtCore import Qt, Slot

from Robot.gui.camera_display import CameraWidget
from Robot.gui.coordinates_display import CoordinatesDisplay
from Robot.gui.target_coords_display import TargetCoordsDisplay
from Robot.gui.area_coords import AreaCalibrationWidget
from Robot.gui.coordinates_map import CoordinateMap  
from Robot.core.comm.client import setup
import Robot.core.comm.sub.coords as coords


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("Robot Control Panel")

        # --- Create widgets ---
        self.camera = CameraWidget()
        self.camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore
        self.coords_display = CoordinatesDisplay()
        self.target_display = TargetCoordsDisplay()
        self.area_calibration = AreaCalibrationWidget()
        self.map_widget = CoordinateMap()

        # --- Create the Show Map button ---
        self.show_map_btn = QPushButton("Hide Map")
        self.show_map_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.show_map_btn.clicked.connect(self.on_show_map_clicked)

        # --- Layout setup ---
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Top layout: status widgets + Show Map button
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.coords_display, 1)
        status_layout.addWidget(self.target_display, 1)
        status_layout.addWidget(self.area_calibration, 1)
        status_layout.addWidget(self.show_map_btn, 0)

        # Bottom layout: camera + map
        camera_map_layout = QHBoxLayout()
        camera_map_layout.addWidget(self.camera, 2)
        camera_map_layout.addWidget(self.map_widget, 1)

        # Add both sections
        main_layout.addLayout(status_layout, 1)
        main_layout.addLayout(camera_map_layout, 2)

        self.setCentralWidget(container)

        # --- Signals and connections ---
        def handle_coordinate_update(x: float, y: float):
            """Forward coordinates to all widgets"""
            print(f"MAIN: Forwarding coordinates - x={x:.2f}, y={y:.2f}")
            self.coords_display.update_coordinates(x, y)
            self.area_calibration.update_current_coordinates(x, y)
            self.map_widget.mark_point(x, y)

        setup(handle_coordinate_update)

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
        """Triggered when 4 points are recorded in AreaCalibrationWidget"""
        print(f"Area calibrated with coordinates: {coordinates}")

    def on_show_map_clicked(self):
        """Toggle the map's visibility"""
        if self.map_widget.isVisible():
            self.map_widget.hide()
            self.show_map_btn.setText("Show Map")
        else:
            self.map_widget.show()
            self.show_map_btn.setText("Hide Map")

    def resizeEvent(self, event):
        new_width = self.width()
        font = QFont("Consolas", int(new_width / 50), QFont.Bold) # type: ignore
        self.coords_display.setFont(font)
        super().resizeEvent(event)
