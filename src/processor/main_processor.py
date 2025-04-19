import cv2

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
from src.processor.finger_counter import FingerCounter
from src.utils.config_helper import Config
from src.utils.statics import LIGHT_GREEN


class ProcessorThread(QThread):
    frame_updated = pyqtSignal(QImage)

    def __init__(self, config: Config):
        super().__init__()

        self.config = config
        self.running = False

        self.finger_counter = FingerCounter(config)


    def start_camera(self):
        self.running = True
        if not self.isRunning():
            self.start()

    def stop_camera(self):
        self.running = False
        self.wait()

    def run(self):
        cap = cv2.VideoCapture(self.config.camera_index)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.camera_width)  # Genişlik
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.camera_height)  # Yükseklik

        if not cap.isOpened():
            print("Kamera açılamadı!")
            return

        while self.running:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            frame = self.finger_counter.process_frame(frame)

            if not ret:
                print("Kamera görüntüsü alınamadı!")
                break

            #self.draw_detections(frame)

            # OpenCV BGR formatından RGB formatına çevirme
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = rgb_frame.shape

            # Qt uyumlu görüntü formatına dönüştürme
            bytes_per_line = channels * width
            qt_image = QImage(
                rgb_frame.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGB888,
            )

            # Sinyal ile görüntüyü arayüze gönderme
            self.frame_updated.emit(qt_image)

        cap.release()
