from abc import ABC, abstractmethod

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

from settings import settings


class FrameObjectDetector(ABC):
    @abstractmethod
    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[tuple[str | None, float | None] | None]:
        """Detect objects on single frame"""


class Detectron2FrameObjectsDetector(FrameObjectDetector):
    def __init__(
            self,
            model_config: str = settings.DETECTRON2_MODEL_CONFIG,
            threshold: float = settings.DETECTRON2_SCORE_THRESH_TEST,
            device: str = settings.DETECTRON2_DEVICE
    ) -> None:
        # Load default Detectron2 configurations
        self.configurations = get_cfg()

        # Specifying exact Detectron2 model settings file
        self.configurations.merge_from_file(model_zoo.get_config_file(
            model_config
        ))
        self.configurations.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            model_config
        )

        # Set threshold for the model to show results
        # with prediction score above it
        self.configurations.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold

        # Choosing CPU or GPU mode
        self.configurations.MODEL.DEVICE = device

        # Set up predictor according to configs above
        self.predictor = DefaultPredictor(self.configurations)

        # Load metadata for returning objects names in detection results
        self.model_metadata = MetadataCatalog.get("coco_2017_train")
        self.objects_names = self.model_metadata.get("thing_classes")

    def detect_objects_on_frame(
            self, frame: bytearray
    ) -> list[tuple[str | None, float | None] | None]:
        # Convert frame to RGB
        frame_rgb = frame[:, :, ::-1]

        outputs = self.predictor(frame_rgb)
        predicted_classes = outputs["instances"].pred_classes.tolist()
        prediction_scores = outputs["instances"].scores.tolist()

        return [
            (self.objects_names[name], round(score, 4))
            for name, score in zip(predicted_classes, prediction_scores)
        ]


DETECTRON2_FRAMES_DETECTOR = Detectron2FrameObjectsDetector()
