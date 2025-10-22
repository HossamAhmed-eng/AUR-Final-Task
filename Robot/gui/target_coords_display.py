from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

class TargetCoordsDisplay(QWidget):
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # --- Title ---
        self._title_label = QLabel("Target Coordinates")
        self._title_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._title_label.setFont(QFont("Arial", 12, QFont.Bold)) # type: ignore
        self._title_label.setStyleSheet("color: #A23B72; background-color: #FFF0F5; padding: 5px; border-radius: 5px;")

        # --- Coordinates Display ---
        self._coords_label = QLabel("X: -- , Y: --")
        self._coords_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._coords_label.setFont(QFont("Consolas", 14, QFont.Bold)) # type: ignore
        self._coords_label.setStyleSheet("""
            background-color: #FFF0F5; 
            padding: 8px; 
            border: 2px solid #A23B72;
            border-radius: 8px;
            color: #A23B72;
        """)

        # --- Status Label ---
        self._status_label = QLabel("Waiting for QR code...")
        self._status_label.setAlignment(Qt.AlignCenter) # type: ignore
        self._status_label.setStyleSheet("color: #666; font-size: 12px; font-style: italic;")

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(self._title_label)
        layout.addWidget(self._coords_label)
        layout.addWidget(self._status_label)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        self.setLayout(layout)

    @Slot(float, float)
    def update_target_coordinates(self, x: float, y: float):
        """Update target coordinates from QR code"""
        self._coords_label.setText(f"X: {x:.2f} , Y: {y:.2f}")
        self._status_label.setText(f"✅ Target acquired from QR")
        self._status_label.setStyleSheet("color: #228B22; font-size: 12px; font-weight: bold;")

    @Slot()
    def clear_target_coordinates(self):
        """Clear target coordinates"""
        self._coords_label.setText("X: -- , Y: --")
        self._status_label.setText("Waiting for QR code...")
        self._status_label.setStyleSheet("color: #666; font-size: 12px; font-style: italic;")

    @Slot(str)
    def update_status(self, status: str):
        #"""Update status message"""
        #if "Fake QR" in status:
        #    self._status_label.setText("❌ Fake QR - Wrong color box")
        #    self._status_label.setStyleSheet("color: #DC143C; font-size: 12px; font-weight: bold;")
        #elif "Invalid QR" in status:
        #    self._status_label.setText("❌ Invalid QR format")
        #    self._status_label.setStyleSheet("color: #FF8C00; font-size: 12px; font-weight: bold;")
        #else:
        self._status_label.setText(status)
        self._status_label.setStyleSheet("color: #666; font-size: 12px;")