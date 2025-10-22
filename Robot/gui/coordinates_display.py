from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

class CoordinatesDisplay(QWidget):
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Title
        self._title_label = QLabel("Current Position")
        self._title_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._title_label.setFont(QFont("Arial", 12, QFont.Bold)) # type: ignore
        self._title_label.setStyleSheet("color: #2E86AB; background-color: #F0F8FF; padding: 5px; border-radius: 5px;")

        #  Coordinates Display 
        self._coords_label = QLabel("X: 0.00 , Y: 0.00")
        self._coords_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._coords_label.setFont(QFont("Consolas", 14, QFont.Bold)) # type: ignore
        self._coords_label.setStyleSheet("""
            background-color: #F0F8FF; 
            padding: 8px; 
            border: 2px solid #2E86AB;
            border-radius: 8px;
            color: #2E86AB;
        """)

        # Status Label
        self._status_label = QLabel("Trying to connect...")
        self._status_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._status_label.setStyleSheet("color: #666; font-size: 12px; font-style: italic;")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self._title_label)
        layout.addWidget(self._coords_label)
        layout.addWidget(self._status_label)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        self.setLayout(layout)

    @Slot()
    def update_coordinates(self, x: float, y: float):
        self._coords_label.setText(f"X: {x:.2f} , Y: {y:.2f}")
        self.update_connection_status(True)

    @Slot(bool)
    def update_connection_status(self, connected: bool):
       if connected:
           self._status_label.setText("✅ Connected To The Robot")
           self._status_label.setStyleSheet("color: #228B22; font-size: 12px; font-weight: bold;")