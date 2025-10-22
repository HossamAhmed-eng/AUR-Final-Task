from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class AreaCalibrationWidget(QWidget):
    coordinates_updated = Signal(list)  # Emits the 4 coordinates when complete
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]  # 2D list for 4 points
        self.current_point_index = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("Area Calibration")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        # Status label
        self.status_label = QLabel("Click 'Record Point' to start calibration")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: blue; font-size: 12px;")
        
        # Current coordinates display
        self.coords_label = QLabel("Current: (0, 0)")
        self.coords_label.setAlignment(Qt.AlignCenter)
        self.coords_label.setStyleSheet("color: gray; font-size: 11px;")
        
        # Record button
        self.record_btn = QPushButton("Record Point 1")
        self.record_btn.clicked.connect(self.record_current_point)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Reset button
        self.reset_btn = QPushButton("Reset Calibration")
        self.reset_btn.clicked.connect(self.reset_calibration)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        # Points display
        self.points_display = QLabel("Points: \n1: (0, 0)\n2: (0, 0)\n3: (0, 0)\n4: (0, 0)")
        self.points_display.setStyleSheet("background-color: #f5f5f5; padding: 10px; border-radius: 5px; font-family: monospace;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.coords_label)
        layout.addWidget(self.record_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.points_display)
        
        self.update_display()
    
    def update_current_coordinates(self, x: float, y: float):
        """Update the current coordinates display"""
        self.current_x = x
        self.current_y = y
        self.coords_label.setText(f"Current: ({x:.2f}, {y:.2f})")
    
    def record_current_point(self):
        """Record the current point and move to next index"""
        if hasattr(self, 'current_x') and hasattr(self, 'current_y'):
            # Store current coordinates
            self.coordinates[self.current_point_index] = [self.current_x, self.current_y]
            
            # Move to next point (cycle with %4)
            self.current_point_index = (self.current_point_index + 1) % 4
            
            self.update_display()
            
            # Check if we completed the cycle
            if self.current_point_index == 0:
                self.status_label.setText("✅ Calibration complete! All 4 points recorded")
                self.status_label.setStyleSheet("color: green; font-size: 12px;")
                self.coordinates_updated.emit(self.coordinates)
    
    def reset_calibration(self):
        """Reset all coordinates and start over"""
        self.coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.current_point_index = 0
        self.status_label.setText("Calibration reset. Click 'Record Point' to start")
        self.status_label.setStyleSheet("color: blue; font-size: 12px;")
        self.update_display()
    
    def update_display(self):
        """Update all UI elements"""
        # Update button text
        point_names = ["Point 1 (Top-Left)", "Point 2 (Top-Right)", 
                      "Point 3 (Bottom-Right)", "Point 4 (Bottom-Left)"]
        self.record_btn.setText(f"Record {point_names[self.current_point_index]}")
        
        # Update status
        if self.current_point_index > 0:
            progress = f"({self.current_point_index}/4 points recorded)"
            self.status_label.setText(f"Recording {point_names[self.current_point_index]} {progress}")
            self.status_label.setStyleSheet("color: orange; font-size: 12px;")
        
        # Update points display
        points_text = "Points:\n"
        for i, (x, y) in enumerate(self.coordinates):
            status = " ✓" if [x, y] != [0, 0] else " ⏳"
            points_text += f"{i+1}: ({x:.2f}, {y:.2f}){status}\n"
        self.points_display.setText(points_text)
    
    def get_coordinates(self):
        """Get the current coordinates list"""
        return self.coordinates