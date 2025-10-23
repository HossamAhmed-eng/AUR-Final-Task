import cv2
import numpy as np
from urllib.parse import parse_qs
from PySide6.QtCore import QObject, Signal, QThread, QMutex
import time

class QRWorker(QThread):
    frame_processed = Signal(object)  # Emits processed frame
    qr_detected = Signal(str, float, float)
    qr_ignored = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.detector = cv2.QRCodeDetector()
        self.last_text = ""
        self.is_processing = False
        self.current_frame = None
        self.mutex = QMutex()
        self.active = True
        self.frame_available = False
        
    def detect_color(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        lower_red = np.array([100, 0, 0])
        upper_red = np.array([255, 80, 80])
    
        lower_green = np.array([0, 100, 0])
        upper_green = np.array([80, 255, 80])
    
        lower_blue = np.array([0, 0, 100])
        upper_blue = np.array([80, 80, 255])
    
        mask_red = cv2.inRange(rgb, lower_red, upper_red)
        mask_green = cv2.inRange(rgb, lower_green, upper_green)
        mask_blue = cv2.inRange(rgb, lower_blue, upper_blue)

        # 🔹 ADD THIS: Morphological filtering to clean up noise
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)

        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)

        # Then count nonzero pixels
        red_pixels = cv2.countNonZero(mask_red)
        green_pixels = cv2.countNonZero(mask_green)
        blue_pixels = cv2.countNonZero(mask_blue)

    
        threshold = 500
    
        if red_pixels > threshold:
            return "red"
        elif green_pixels > threshold:
            return "green"
        elif blue_pixels > threshold:
            return "blue"
        else:
            return "unknown"
        
    def set_processing(self, enabled: bool):
        self.mutex.lock()
        self.is_processing = enabled
        if enabled:
            self.last_text = ""  # Reset to detect new QR codes
        self.mutex.unlock()

    def update_frame(self, frame):
        """Receive new frame from camera"""
        self.mutex.lock()
        if frame is not None:
            self.current_frame = frame.copy()
            self.frame_available = True
        else:
            self.frame_available = False
        self.mutex.unlock()

    def run(self):

        while self.active:
            self.mutex.lock()
            should_process = self.is_processing and self.frame_available
            frame = self.current_frame.copy() if self.frame_available else None # type: ignore
            self.mutex.unlock()
            
            if frame is not None and should_process:
                try:
                    processed_frame = self.process_frame(frame)
                    self.frame_processed.emit(processed_frame)
                        
                except Exception as e:
                    print(f"QR processing error: {e}")
            elif frame is not None:
                # Just pass through the frame if not processing
                self.frame_processed.emit(frame)
            
            time.sleep(0.01)

    def process_frame(self, frame):
        try:
            decoded_text, points, _ = self.detector.detectAndDecode(frame)

            if points is not None:
                points = points[0].astype(int)
                
                if len(points) < 3:
                    return frame
                    
                area = cv2.contourArea(points)
                if area <= 0:
                    return frame
                
                if self.detect_color(frame) !="blue":
                    cv2.putText(frame, "Ignored (Fake QR Box)", (points[0][0], points[0][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    self.last_text = ""
                    print(f"❌ FAKE QR: Coordinate QR on wrong color - {decoded_text}")
                    self.qr_ignored.emit("Fake QR - Wrong color")
                    return frame

                if decoded_text and 'X=' in decoded_text and 'Y=' in decoded_text:
                    print(f" Processing coordinate QR: {decoded_text}")
                    
                    # draw green outline
                    for i in range(len(points)):
                        cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

                    
                    if decoded_text and decoded_text != self.last_text:
                        self.last_text = decoded_text
                        print(f"Decoded QR Code before parsing: {decoded_text}")

                        try:
                            parsed = parse_qs(decoded_text)
                            x = float(parsed["X"][0])
                            y = float(parsed["Y"][0])
                            print(f"Decoded QR Code after parsing: {x} , {y}")
                            self.qr_detected.emit(decoded_text, x, y)
                            
                        except Exception as e:
                            print(f"Could not parse QR content: {e}")
                            self.qr_ignored.emit("Invalid QR format")

                    cv2.putText(frame, decoded_text, (points[0][0], points[0][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                else:
                    self.last_text = ""
            else:
                self.last_text = ""

        except Exception as e:
            print(f"QR detection error (continuing): {e}")
            
        return frame
    
    def stop(self):
        """Stop the worker thread safely"""
        self.active = False
        self.mutex.lock()
        self.current_frame = None
        self.frame_available = False
        self.mutex.unlock()
        self.wait(1000)

class QRProcessor(QObject):
    qr_detected = Signal(str, float, float)
    qr_ignored = Signal(str)
    status_update = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.worker = QRWorker()
        self.worker.frame_processed.connect(self.on_frame_processed)
        self.worker.qr_detected.connect(self.qr_detected)
        self.worker.qr_ignored.connect(self.qr_ignored)
        self.worker.start()
        self.processed_frame = None
        
    def set_processing(self, enabled: bool):
        self.worker.set_processing(enabled)
        if enabled:
            self.status_update.emit("QR Scanning: ON")
        else:
            self.status_update.emit("QR Scanning: OFF")
    
    def update_frame(self, frame):
        """Send frame to worker for processing"""
        if frame is not None:
            self.worker.update_frame(frame)
    
    def on_frame_processed(self, frame):
        """Receive processed frame from worker"""
        self.processed_frame = frame
    
    def get_processed_frame(self):
        """Get the latest processed frame"""
        return self.processed_frame
    
    def stop(self):
        """Stop the QR processor safely"""
        try:
            self.worker.stop()
        except Exception as e:
            print(f"Error stopping QR processor: {e}")
