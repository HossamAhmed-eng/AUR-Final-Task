from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class AreaCalibrationWidget(QWidget):
    coordinates_updated = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.coordinates = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
        self.current_point_index = 0
        self.current_x = 0.0
        self.current_y = 0.0
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Record button with larger font
        self.record_btn = QPushButton("RECORD POINT 1")
        self.record_btn.clicked.connect(self.record_current_point)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Points display with larger font
        self.points_display = QLabel()
        self.points_display.setAlignment(Qt.AlignLeft) # type: ignore
        self.points_display.setStyleSheet("""
            background-color: #f8f9fa; 
            padding: 10px; 
            border-radius: 5px; 
            font-family: monospace;
            font-size: 12px;
            border: 1px solid #dee2e6;
            color: #495057;
        """)
        
        layout.addWidget(self.record_btn)
        layout.addWidget(self.points_display)
        
        # Initialize display
        self.update_display()
    
    def update_current_coordinates(self, x: float, y: float):
        """Update the current coordinates"""
        self.current_x = x
        self.current_y = y
    
    def record_current_point(self):
        """Record the current point"""
        # Store coordinates
        self.coordinates[self.current_point_index] = [self.current_x, self.current_y]
        
        # Move to next point
        self.current_point_index = (self.current_point_index + 1) % 4
        
        # Update display
        self.update_display()
        
        # Emit signal if completed
        if self.current_point_index == 0:
            self.coordinates_updated.emit(self.coordinates)
    
    def update_display(self):
        """Update the display"""
        # Update button
        point_names = ["1", "2", "3", "4"]
        self.record_btn.setText(f"RECORD POINT {point_names[self.current_point_index]}")
        
        # Update points display - larger but still compact
        points_text = ""
        for i, (x, y) in enumerate(self.coordinates):
            status = " ✅" if [x, y] != [0.0, 0.0] else " ❌"
            points_text += f"Point {i+1}: ({x:.2f}, {y:.2f}){status}\n"
        
        self.points_display.setText(points_text)
    
    def get_coordinates(self):
        return self.coordinates