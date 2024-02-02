import cv2
import logging

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog


class Detector:
    def __init__(self):
        self.configurations = get_cfg()

        # Specifying exact Detectron2 model settings file
        self.configurations.merge_from_file(model_zoo.get_config_file(
            "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
        ))
        self.configurations.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
        )

        # Set threshold for this model.
        # Object will be taken into account if prediction accuracy is >= 70 %
        self.configurations.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7

        # Choosing CPU or GPU mode
        self.configurations.MODEL.DEVICE = "cpu"

        self.predictor = DefaultPredictor(self.configurations)

        # Load metadata for returning objects names in detection results
        self.model_metadata = MetadataCatalog.get("coco_2017_train")
        self.objects_names = self.model_metadata.get("thing_classes")

    def detect_objects(self, video_path: str) -> list:
        logging.info(f"Starting to process video: {video_path}")

        video_object = cv2.VideoCapture(video_path)
        if not video_object.isOpened():
            logging.error(f"Failed to open video file: {video_path}")
            return []

        frames_count = 0
        detection_results = []

        while True:
            success, frame = video_object.read()
            if not success:
                break  # Break the loop when there are no frames left

            frames_count += 1

            # Convert frame from BGR to RGB
            frame_rgb = frame[:, :, ::-1]

            # Perform object detection on single frame
            frame_detection_outputs = self.predictor(frame_rgb)

            predicted_objects_names = frame_detection_outputs[
                "instances"
            ].pred_classes.tolist()
            prediction_accuracy = frame_detection_outputs[
                "instances"
            ].scores.tolist()
            single_image_results = [
                (
                    self.objects_names[name],
                    round(prediction_accuracy[index], 4)
                )
                for index, name in enumerate(predicted_objects_names)
            ]

            detection_results.append(single_image_results)

        video_object.release()
        cv2.destroyAllWindows()

        logging.info(
            f"Finished detecting objects."
            f" Total frames processed: {frames_count}"
        )

        return detection_results
