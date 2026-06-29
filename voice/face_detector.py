import threading
import time
import cv2
import os
from PySide6.QtCore import QObject, Signal


class FaceBridge(QObject):
    face_signal = Signal()


class FaceDetector(threading.Thread):
    def __init__(self, controller, device_index=0):
        super().__init__()
        self.controller = controller
        self.running = True

        self.bridge = FaceBridge()
        self.bridge.face_signal.connect(self.controller.on_face_detected)

        self.cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)

        # ★ 絶対パスで読み込む
        cascade_path = os.path.join(os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            print("[FaceDetector] Cascade load error:", cascade_path)
            self.face_cascade = None

        self.last_detect = 0
        self.cooldown = 5.0
        self.daemon = True

    def run(self):
        print("[FaceDetector] Thread started")

        while self.running:
            ret, frame = self.cap.read()
            if not ret or self.face_cascade is None:
                time.sleep(0.1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(80, 80))

            if len(faces) > 0:
                if not getattr(self.controller, "is_playing", False):
                    now = time.time()
                    if now - self.last_detect > self.cooldown:
                        print("[FaceDetector] Face detected → p1")
                        self.last_detect = now
                        self.bridge.face_signal.emit()

            time.sleep(0.05)

        print("[FaceDetector] Thread ended")

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        print("[FaceDetector] Stop requested")
