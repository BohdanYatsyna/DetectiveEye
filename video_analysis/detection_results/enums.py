from enum import Enum


class DetectionStatus(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"


class ObjectsDetectorChoice(Enum):
    DEFAULT_DETECTRON2 = "Detectron2"
    DEFAULT_YOLOv8 = "YOLOv8"
