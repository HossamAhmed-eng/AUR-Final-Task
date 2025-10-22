import os
import cv2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap

from Robot.core.cv import Camera

class CameraWidget(QWidget):
    #  ADD BOTH SIGNALS
    target_coordinates_received = Signal(float, float)
    qr_status_update = Signal(str)  #  ADD THIS MISSING SIGNAL
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.camera_device = Camera()
        
        # TEMPORARY: Don't initialize QR processor yet
        self.qr_processor = None
        self.is_camera_on = False
        self.is_qr_scanning = False
        self.last_raw_frame = None
        self.cleaning_up = False

        #  UI Elements 
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter) # type: ignore
        self.label.setStyleSheet("background-color: black;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore

        self.start_btn = QPushButton("Start Camera")
        self.qr_btn = QPushButton("Start QR Scanning")
        self.qr_btn.setEnabled(False)
        
        self.info_label = QLabel("Status: Camera OFF | QR Scanning: OFF")
        self.info_label.setAlignment(Qt.AlignCenter) # type: ignore
        self.info_label.setStyleSheet("font-size: 14px; color: gray;")

        #  Layout
        layout = QVBoxLayout(self)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.qr_btn)
        
        layout.addWidget(self.label, stretch=3)
        layout.addLayout(button_layout)
        layout.addWidget(self.info_label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        #  Timer 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.setInterval(40)

        # Button connections 
        self.start_btn.clicked.connect(self.toggle_camera)
        self.qr_btn.clicked.connect(self.toggle_qr_scanning)

        self._show_placeholder()

    def toggle_camera(self):
        """Start or stop the camera feed."""
        if self.cleaning_up:
            return
            
        if not self.is_camera_on:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        """Start camera and related components"""
        print(" Starting camera...")
        try:
            if not self.camera_device.start():
                self.label.setText("❌ Failed to open camera")
                self.info_label.setText("Status: Camera ERROR")
                print("❌ Camera failed to start")
                return

            self.is_camera_on = True
            self.start_btn.setText("Stop Camera")
            self.qr_btn.setEnabled(True)
            self.info_label.setText("Status: Camera ON | QR Scanning: OFF")
            self.timer.start()
            print(" Camera started successfully")
            
            # NOW initialize QR processor after camera is working
            self.initialize_qr_processor()
            
        except Exception as e:
            print(f" Camera start error: {e}")
            self.label.setText(" Camera Error")
            self.info_label.setText("Status: Camera ERROR")

    def initialize_qr_processor(self):
        """Initialize QR processor only after camera is working"""
        print(" Initializing QR processor...")
        try:
            from Robot.core.qr_processor import QRProcessor
            self.qr_processor = QRProcessor()
            
            # Connect QR processor signals
            self.qr_processor.qr_detected.connect(self.on_qr_detected)
            self.qr_processor.qr_ignored.connect(self.on_qr_ignored)
            self.qr_processor.status_update.connect(self.on_status_update)
            
            print(" QR processor initialized successfully")
            
        except Exception as e:
            print(f" QR processor initialization failed: {e}")
            self.qr_btn.setEnabled(False)
            self.info_label.setText("Status: Camera ON | QR ERROR")

    def stop_camera(self):
        """Stop camera and clean up resources SAFELY"""
        if self.cleaning_up:
            return
            
        self.cleaning_up = True
        
        
        self.timer.stop()
        
        
    
        if self.qr_processor:
            self.is_qr_scanning = False
            self.qr_processor.set_processing(False)

        

        self.camera_device.stop()

        

        self.last_raw_frame = None
        

        self.is_camera_on = False
        self.start_btn.setText("Start Camera")
        self.qr_btn.setText("Start QR Scanning")
        self.qr_btn.setEnabled(False)
        self.qr_btn.setStyleSheet("")
        self.info_label.setText("Status: Camera OFF | QR Scanning: OFF")
        
        self._show_placeholder()
        

        self.cleaning_up = False

    def toggle_qr_scanning(self):
        """Toggle QR code scanning on/off."""
        if not self.is_camera_on or self.cleaning_up or not self.qr_processor:
            return
            
        self.is_qr_scanning = not self.is_qr_scanning
        self.qr_processor.set_processing(self.is_qr_scanning)
        
        if self.is_qr_scanning:
            self.qr_btn.setText("Stop QR Scanning")
            self.qr_btn.setStyleSheet("background-color: #ff4444; color: white;")
        else:
            self.qr_btn.setText("Start QR Scanning")
            self.qr_btn.setStyleSheet("")
  
    def update_frame(self):
        """Main frame update loop"""
        if not self.is_camera_on or self.cleaning_up:
            return
            
        try:
            # Get frame from camera
            frame = self.camera_device.frame
            if frame is None:
                return
                
            self.last_raw_frame = frame

            if self.is_qr_scanning and self.qr_processor:
                self.qr_processor.update_frame(frame)
                

                processed_frame = self.qr_processor.get_processed_frame()
                if processed_frame is not None:
                    self.display_frame(processed_frame)
                    return
            

            self.display_frame(frame)
            
        except Exception as e:
            print(f" Frame update error: {e}")
            if not self.cleaning_up:
                self.stop_camera()

    def display_frame(self, frame):
        """Display a frame in the QLabel"""
        if frame is None:
            return
            
        try:
            # Convert to RGB for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimage = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888) # type: ignore
            pixmap = QPixmap.fromImage(qimage)

            self.label.setPixmap(
                pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.IgnoreAspectRatio, # type: ignore
                    Qt.SmoothTransformation # type: ignore
                )
            )
        except Exception as e:
            print(f"❌ Display frame error: {e}")


    def on_qr_detected(self, text: str, x: float, y: float):
        """Handle detected QR code with coordinates"""
        print(f"✅ Valid QR detected: {text} -> X: {x}, Y: {y}")
        self.target_coordinates_received.emit(x, y)
        self.qr_status_update.emit(f"✅ Target acquired: X={x:.2f}, Y={y:.2f}")

    def on_qr_ignored(self, reason: str):
        """Handle ignored QR code"""
        print(f"❌ QR ignored: {reason}")
        self.qr_status_update.emit(f"❌ {reason}")

    def on_status_update(self, status: str):
        """Update status message"""
        if self.is_camera_on and not self.cleaning_up:
            current_text = self.info_label.text()
            camera_status = current_text.split("|")[0]
            self.info_label.setText(f"{camera_status} | {status}")
            self.qr_status_update.emit(status)

    def _show_placeholder(self):
        """Display a static placeholder image or text when the camera is off."""
        placeholder_path = os.path.join(os.path.dirname(__file__), "pic.jpg")
        pic_img = cv2.imread(placeholder_path)

        if pic_img is None:
            self.label.setText("Camera Off")
            return

        try:
            pic_img = cv2.cvtColor(pic_img, cv2.COLOR_BGR2RGB)
            h, w, ch = pic_img.shape
            bytes_per_line = ch * w
            qimage = QImage(pic_img.data, w, h, bytes_per_line, QImage.Format_RGB888) # type: ignore
            pixmap = QPixmap.fromImage(qimage)

            self.label.setPixmap(
                pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.IgnoreAspectRatio, # type: ignore
                    Qt.SmoothTransformation # type: ignore
                )
            )
        except Exception:
            self.label.setText("Camera Off")

    def closeEvent(self, event):
        """Clean up when widget is closed"""
        print(" Closing camera widget...")
        if self.is_camera_on:
            self.stop_camera()
        super().closeEvent(event)