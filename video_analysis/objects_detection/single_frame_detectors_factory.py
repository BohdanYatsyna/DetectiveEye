from abc import ABC, abstractmethod

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog
from ultralytics import YOLO

from settings import settings
from .single_frame_detectors import (
    FrameObjectDetector,
    Detectron2FrameObjectsDetector,
    YOLOv8FrameObjectsDetector
)


class FrameObjectDetectorFactory(ABC):
    @abstractmethod
    def create_single_frame_detector(
            self, *args, **kwargs
    ) -> FrameObjectDetector:
        """Creates Frame Object Detector instance"""


class Detectron2DetectorFactory(FrameObjectDetectorFactory):
    """Creates instance of Detectron2FrameObjectsDetector"""

    def create_single_frame_detector(
            self, model_config: str, threshold: float, device: str
    ) -> Detectron2FrameObjectsDetector:
        """
        Next parameters are required for creating
        Detectron2FrameObjectsDetector

        :param model_config: Detectron2 model config file str like:
        'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'
        :param threshold: float value for predictions below it not to be shown
        :param device: str 'cpu' or 'gpu' for different hardware support
        'gpu' mode is possible only with CUDA support
        """

        # Load default Detectron2 configurations
        configurations = get_cfg()

        # Specifying exact Detectron2 model settings file
        configurations.merge_from_file(model_zoo.get_config_file(
            model_config
        ))
        configurations.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            model_config
        )

        # Set threshold for the model to show results
        # with prediction score above it
        configurations.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold

        # Choosing CPU or GPU mode
        configurations.MODEL.DEVICE = device
        predictor = DefaultPredictor(configurations)

        # Load metadata for returning objects names in detection results
        model_metadata = MetadataCatalog.get("coco_2017_train")
        objects_names = model_metadata.get("thing_classes")

        return Detectron2FrameObjectsDetector(predictor, objects_names)


class YOLOv8DetectorFactory(FrameObjectDetectorFactory):
    """Creates instance of VOLOv8FrameObjectsDetector"""

    def create_single_frame_detector(
            self, model_name: str, threshold: float, device: str
    ) -> YOLOv8FrameObjectsDetector:
        """
        Next parameters are required for creating YOLOv8FrameObjectsDetector

        :param model_name: YOLOv8 model config file str like:
        'yolov8n.pt'
        :param threshold: float value for predictions below it not to be shown
        :param device: str 'cpu' or 'gpu' for different hardware support
        'gpu' mode is possible only with CUDA support
        """

        model = YOLO(model_name)
        threshold = threshold
        device = device

        return YOLOv8FrameObjectsDetector(model, threshold, device)


YOLOv8_FACTORY = YOLOv8DetectorFactory()
YOLOv8_FRAME_DETECTOR = YOLOv8_FACTORY.create_single_frame_detector(
    model_name=settings.YOLOv8_MODEL,
    threshold=settings.YOLOv8_SCORE_THRESH_TEST,
    device=settings.YOLOv8_DEVICE
)

DETECRON2_FACTORY = Detectron2DetectorFactory()
DETECTRON2_FRAME_DETECTOR = DETECRON2_FACTORY.create_single_frame_detector(
    model_config=settings.DETECTRON2_MODEL_CONFIG,
    threshold=settings.DETECTRON2_SCORE_THRESH_TEST,
    device=settings.DETECTRON2_DEVICE
)
