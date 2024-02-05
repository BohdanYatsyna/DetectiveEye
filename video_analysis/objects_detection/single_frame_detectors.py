from abc import ABC, abstractmethod
from typing import Any

from detectron2.engine import DefaultPredictor


class FrameObjectDetector(ABC):
    @abstractmethod
    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[tuple[str | None, float | None] | None]:
        """Detect objects on single video-frame"""


class Detectron2FrameObjectsDetector(FrameObjectDetector):
    def __init__(
            self, predictor: DefaultPredictor, objects_names: dict
    ) -> None:
        self.predictor = predictor
        self.objects_names = objects_names

    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[tuple[str | None, float | None] | None]:
        # Convert frame to RGB
        frame_rgb = frame[:, :, ::-1]

        detection_outputs = self.predictor(frame_rgb)
        predicted_classes = detection_outputs[
            "instances"
        ].pred_classes.tolist()
        prediction_scores = detection_outputs["instances"].scores.tolist()

        return [
            (self.objects_names[name], round(score, 4))
            for name, score in zip(predicted_classes, prediction_scores)
        ]
