import cv2
import cvzone.HandTrackingModule as htm

from src.utils.config_helper import Config
from src.utils.dk_connection import DKConnection
class FingerCounter:
    def __init__(self, config: Config):
        self.config = config
        self.detector = htm.HandDetector(
            detectionCon=self.config.detection_confidence,
            maxHands=self.config.max_hands,
        )
        
        self.fingers = []
        self.dk_connection = DKConnection()


    def process_frame(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        hands, frame = self.detector.findHands(frame)

        if hands:
            self.fingers = self.detector.fingersUp(hands[0])
            if self.fingers == [0, 0, 1, 0, 0]:
                self.fingers = [0, 0, 0, 0, 0]
            self.dk_connection.send_message(str(self.fingers))

        return frame
