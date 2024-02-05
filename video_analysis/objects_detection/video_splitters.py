import cv2

from abc import ABC, abstractmethod


class VideoSplitter(ABC):
    @abstractmethod
    def split_video_into_frames(self, video_path: str) -> bytearray:
        pass


class OpenCVVideoSplitter(VideoSplitter):
    def split_video_into_frames(self, video_path: str) -> bytearray:
        video_object = cv2.VideoCapture(video_path)
        if not video_object.isOpened():
            cv2.destroyAllWindows()
            raise FileNotFoundError("Failed to open video file")

        try:
            while True:
                success, frame = video_object.read()
                if not success:
                    break
                yield frame

        finally:
            video_object.release()
            cv2.destroyAllWindows()


OPENCV_VIDEO_SPLITTER = OpenCVVideoSplitter()
