import cv2
import winsound
import os
import sys
import numpy as np
from urllib.parse import parse_qs
from RobotGui.core.cv import Camera

class QRCodeScanner:
    def __init__(self, camera_index=1):
        self.cap = cv2.VideoCapture(camera_index)
        self.detector = cv2.QRCodeDetector()
        self.last_text = ""
        self.silence_opencv_warnings()

    def silence_opencv_warnings(self):
        """Suppress OpenCV debug logs."""
        try:
            cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_SILENT)
        except Exception:
            sys.stderr = open(os.devnull, 'w')

    def background_is_green(self, frame, points, margin=10, green_threshold=1.3):
        x_min = max(int(np.min(points[:, 0])) - margin, 0)
        x_max = min(int(np.max(points[:, 0])) + margin, frame.shape[1])
        y_min = max(int(np.min(points[:, 1])) - margin, 0)
        y_max = min(int(np.max(points[:, 1])) + margin, frame.shape[0])

        region = frame[y_min:y_max, x_min:x_max]
        if region.size == 0:
            return False

        avg_color = np.mean(region, axis=(0, 1))
        blue, green, red = avg_color
        return green > green_threshold * ((red + blue) / 2)

    def process_frame(self, frame):
        """Detect and decode QR code from a single frame."""
        decoded_text, points, _ = self.detector.detectAndDecode(frame)

        if points is not None:
            points = points[0].astype(int)

            # draw green outline
            for i in range(len(points)):
                cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

            # check green background
            if not self.background_is_green(frame, points):
                cv2.putText(frame, "Ignored (Fake QR Box)", (points[0][0], points[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                self.last_text = ""
                return frame

            # Handle decoded text
            if decoded_text and decoded_text != self.last_text:
                self.last_text = decoded_text
                print(f"Decoded QR Code before parsing: {decoded_text}")

                try:
                    parsed = parse_qs(decoded_text)
                    x = float(parsed["X"][0])
                    y = float(parsed["Y"][0])
                    print(f"Decoded QR Code after parsing: {x} , {y}")
                    winsound.Beep(1000, 100)
                except Exception:
                    print("Could not parse QR content.")

            # Display decoded text
            cv2.putText(frame, decoded_text, (points[0][0], points[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        else:
            self.last_text = ""

        return frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = self.process_frame(frame)
            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    scanner = QRCodeScanner(camera_index=1)
    scanner.run()
