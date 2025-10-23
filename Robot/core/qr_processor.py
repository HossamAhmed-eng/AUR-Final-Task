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

                if decoded_text and 'X=' in decoded_text and 'Y=' in decoded_text:
                    print(f" Processing coordinate QR: {decoded_text}")
                    
                    # draw green outline
                    for i in range(len(points)):
                        cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

                    # --- COMMENTED OUT: fake QR detection ---
                    # if not self.background_is_green(frame, points):
                    #     cv2.putText(frame, "Ignored (Fake QR Box)", (points[0][0], points[0][1] - 10),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    #     self.last_text = ""
                    #     print(f"❌ FAKE QR: Coordinate QR on wrong color - {decoded_text}")
                    #     self.qr_ignored.emit("Fake QR - Wrong color")
                    #     return frame
                    # ---------------------------------------

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

    # --- COMMENTED OUT: background color check (used for fake QR detection) ---
    # def background_is_green(self, frame, points, margin=10, green_threshold=1.3):
    #     try:
    #         x_min = max(int(np.min(points[:, 0])) - margin, 0)
    #         x_max = min(int(np.max(points[:, 0])) + margin, frame.shape[1])
    #         y_min = max(int(np.min(points[:, 1])) - margin, 0)
    #         y_max = min(int(np.max(points[:, 1])) + margin, frame.shape[0])

    #         region = frame[y_min:y_max, x_min:x_max]
    #         if region.size == 0:
    #             return False

    #         avg_color = np.mean(region, axis=(0, 1))
    #         blue, green, red = avg_color
    #         return green > green_threshold * ((red + blue) / 2)
    #     except Exception as e:
    #         print(f"Background color check error: {e}")
    #         return False
    # --------------------------------------------------------------------------

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
