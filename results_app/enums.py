from enum import Enum

class DetectionStatus(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"
