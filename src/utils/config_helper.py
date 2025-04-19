from src.utils.yaml_serializable import YamlSerializable


class Config(YamlSerializable):
    def __init__(self):
        self.camera_index = 0
        self.camera_height = 640
        self.camera_width = 640
        self.detection_confidence = 0.65
        self.max_hands = 1

    def __str__(self):
        return (
            f"Config i:{self.camera_index} h:{self.camera_height} w:{self.camera_width}"
        )
