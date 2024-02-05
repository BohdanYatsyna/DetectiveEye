from typing import Any

from celery import Task

from db.sync_database_session import get_sync_session
from settings import celery_instance
from video_analysis.detection_results.enums import DetectionStatus
from video_analysis.objects_detection.video_detectors import (
    DEFAULT_VIDEO_OBJECTS_DETECTOR
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


@celery_instance.task(
    bind=True, base=ObjectsDetectionTask
)
def detect_objects_on_video_task(self, video_file_path: str) -> list:
    detection_results = (
        DEFAULT_VIDEO_OBJECTS_DETECTOR.detect_all_objects_on_video(
            video_file_path
        )
    )

    return detection_results
