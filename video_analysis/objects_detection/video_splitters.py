import cv2

from abc import ABC, abstractmethod


class VideoSplitter(ABC):
    @abstractmethod
    def split_video_into_frames(self, video_path: str) -> bytearray:
        """Split video into frames and yield frame-by-frame"""


class OpenCVVideoSplitter(VideoSplitter):
    def split_video_into_frames(self, video_path: str) -> bytearray:
        video_object = cv2.VideoCapture(video_path)
        if not video_object.isOpened():
            raise FileNotFoundError("Failed to open video file")

        try:
            while True:
                success, frame = video_object.read()
                if not success:
                    break
                yield frame

        finally:
            video_object.release()


OPENCV_VIDEO_SPLITTER = OpenCVVideoSplitter()
