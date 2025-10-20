from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

class CoordinatesDisplay(QWidget):
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._coords_label = QLabel("X: 0 , Y: 0", self)
        self._coords_label.setAlignment(Qt.AlignLeft) # type: ignore
        self._coords_label.setFont(QFont("Consolas", 14, QFont.Bold)) # type: ignore

        self._status_label = QLabel("Trying to connect...")
        self._status_label.setAlignment(Qt.AlignRight) # type: ignore
        self._status_label.setStyleSheet("color: blue; font-size: 13px;")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self._coords_label)
        layout.addWidget(self._status_label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

    @Slot()
    def update_coordinates(self, x: float, y: float):
        self._coords_label.setText(f"X: {x:.2f} , Y: {y:.2f}")
        self.update_connection_status(True)

    @Slot(bool)
    def update_connection_status(self, connected: bool):
       if connected:
           self._status_label.setText("✅ Connected To The Robot")
           self._status_label.setStyleSheet("color: green; font-size: 13px;")
      