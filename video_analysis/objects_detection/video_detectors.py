from .video_splitters import VideoSplitter, OPENCV_VIDEO_SPLITTER
from .single_frame_detectors import (
    DETECTRON2_FRAMES_DETECTOR, FrameObjectDetector
)


class VideoObjectDetector:
    def __init__(
            self,
            object_detector: FrameObjectDetector,
            video_splitter: VideoSplitter
    ):
        self.object_detector = object_detector
        self.video_splitter = video_splitter

    def detect_all_objects_on_video(self, video_path: str) -> list:
        detection_results = []
        frames_count = 0

        for frame in self.video_splitter.split_video_into_frames(video_path):
            frames_count += 1
            detection_result = self.object_detector.detect_objects_on_frame(
                frame
            )
            detection_results.append(detection_result)

        return detection_results


DEFAULT_VIDEO_OBJECTS_DETECTOR = VideoObjectDetector(
    DETECTRON2_FRAMES_DETECTOR, OPENCV_VIDEO_SPLITTER
)
