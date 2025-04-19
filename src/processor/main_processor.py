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

    def draw_detections(self, frame):
        """
        Tespit edilen nesneleri çizer
        """
        if self.config.ballon_detection_is_active:
            # returns: x1, y1, x2, y2, track_id, prob, color
            for data in self.dh_baloon_detection.get_loc_info():
                if data is not None:
                    x1, y1, x2, y2, track_id, conf, color = data
                    cv2.rectangle(frame, (x1, y1), (x2, y2), LIGHT_GREEN, 2)
                    print(f"track_id: {track_id}, color: {color}")
                    cv2.putText(
                        frame,
                        f"{track_id} {conf} {Color(color).name}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        LIGHT_GREEN,
                        2,
                    )

        if self.config.ocr_is_active:
            for data in self.dh_text_detection.get_loc_info():
                if data is not None:
                    x1, y1, x2, y2, prob, text = data
                    print(data)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), LIGHT_GREEN, 2)
                    cv2.putText(
                        frame,
                        f"{text} {prob}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        LIGHT_GREEN,
                        2,
                    )
