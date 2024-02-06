from .single_frame_detectors_factory import (
    DETECTRON2_FRAME_DETECTOR, YOLOv8_FRAME_DETECTOR
)
from .video_splitters import VideoSplitter, OPENCV_VIDEO_SPLITTER
from .single_frame_detectors import (
    FrameObjectDetector
)


class VideoObjectDetector:
    """Handles objects detection on video"""

    def __init__(
            self,
            object_detector: FrameObjectDetector,
            video_splitter: VideoSplitter
    ):
        self.object_detector = object_detector
        self.video_splitter = video_splitter

    def detect_all_objects_on_video(
            self, video_path: str
    ) -> list[list[tuple[str | None, float | None] | None] | None]:
        detection_results = []
        frames_count = 0

        for frame in self.video_splitter.split_video_into_frames(video_path):
            frames_count += 1
            detection_result = self.object_detector.detect_objects_on_frame(
                frame
            )
            detection_results.append(detection_result)

        return detection_results


DEFAULT_DETECTRON2_OBJECTS_DETECTOR = VideoObjectDetector(
    DETECTRON2_FRAME_DETECTOR, OPENCV_VIDEO_SPLITTER
)
DEFAULT_YOLOv8_OBJECTS_DETECTOR = VideoObjectDetector(
    YOLOv8_FRAME_DETECTOR, OPENCV_VIDEO_SPLITTER
)
