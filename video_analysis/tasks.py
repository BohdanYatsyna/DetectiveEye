from typing import Any

from celery import Task

from db.sync_database_session import get_sync_session
from settings import celery_instance
from video_analysis.detection_results.enums import (
    DetectionStatus, ObjectsDetectorChoice
)
from video_analysis.objects_detection.video_detectors import (
    DEFAULT_DETECTRON2_OBJECTS_DETECTOR,
    DEFAULT_YOLOv8_OBJECTS_DETECTOR,
    VideoObjectDetector
)
from video_analysis.utils import delete_file
from video_analysis.detection_results.crud import update_detection_result


@celery_instance.task()
def delete_video_after_detecting_task(video_file_path: str) -> None:
    delete_file(video_file_path)


class ObjectsDetectionTask(Task):
    def after_return(
            self,
            status: str,
            return_value: list,
            task_id: str,
            args: Any,
            kwargs: Any,
            einfo: Any,
    ) -> None:
        file_path = args[0]
        delete_video_after_detecting_task.apply_async(args=[file_path])

    def on_success(
            self, return_value: list, task_id: str, args: Any, kwargs: Any
    ) -> None:
        with get_sync_session() as db:
            update_detection_result(
                db, task_id, DetectionStatus.SUCCESS, return_value
            )

    @staticmethod
    def get_error_message(exception: Exception) -> list[str]:
        if isinstance(exception, FileNotFoundError):
            error_message = [
                f"{str(exception)}. Try to upload video again"
            ]
        elif isinstance(exception, TimeoutError):
            error_message = [
                "Objects detecting take too long time, "
                "try to upload shorter video"
            ]
        else:
            error_message = [
                "Unexpected objects detecting error, "
                "please try to upload video again"
            ]

        return error_message

    def on_failure(
            self,
            exception: Exception,
            task_id: str,
            args: Any,
            kwargs: Any,
            einfo: Any,
    ) -> None:
        error_message = self.get_error_message(exception)

        with (get_sync_session() as db):
            update_detection_result(
                db, task_id, DetectionStatus.FAILURE, error_message
            )

    @staticmethod
    def get_object_detector(detector_choice: str) -> VideoObjectDetector:
        if detector_choice == ObjectsDetectorChoice.DEFAULT_DETECTRON2.value:
            detector = DEFAULT_DETECTRON2_OBJECTS_DETECTOR
        elif detector_choice == ObjectsDetectorChoice.DEFAULT_YOLOv8.value:
            detector = DEFAULT_YOLOv8_OBJECTS_DETECTOR

        return detector


@celery_instance.task(
    bind=True, base=ObjectsDetectionTask
)
def object_detection_on_video_task(
        self, video_file_path: str, detector_choice: str
) -> list:
    detector = self.get_object_detector(detector_choice)
    detection_results = detector.detect_all_objects_on_video(video_file_path)

    return detection_results
