from abc import ABC, abstractmethod
from typing import Any

from detectron2.engine import DefaultPredictor


class FrameObjectDetector(ABC):
    @abstractmethod
    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[list[str | None, float | None] | None]:
        """Detect objects on single video-frame"""


class Detectron2FrameObjectsDetector(FrameObjectDetector):
    """Facebook Detectron2 single frame/image objects detector"""

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


class YOLOv8FrameObjectsDetector(FrameObjectDetector):
    """Ultralytics YOLOv8 single frame/image objects detector"""

    def __init__(
            self, model: Any, threshold: float, device: str
    ) -> None:
        self.model = model
        self.threshold = threshold
        self.device = device

    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[tuple[str | None, float | None] | None]:

        raw_detection_outputs = self.model.predict(
            frame, conf=self.threshold, device=self.device
        )

        objects_names_dict = self.model.names

        detection_outputs = raw_detection_outputs[0].numpy()
        predicted_objects_ids = detection_outputs.boxes.cls.tolist()
        prediction_scores = detection_outputs.boxes.conf.tolist()

        return [
            (objects_names_dict[int(predicted_object_id)], round(score, 4))
            for predicted_object_id, score in zip(
                predicted_objects_ids, prediction_scores
            )
        ]
