import logging

from fastapi import UploadFile

from db.sync_database_session import get_sync_session
from settings import CeleryConfig, celery_instance
from video_analysis.objects_detection.detector import Detector
from video_analysis.results.enums import DetectionStatus
from video_analysis.results.crud import update_detection_result
from video_analysis.utils import delete_processed_video



@celery_instance.task(bind=True)
def detect_objects_on_video_task(self, video_file_path: str) -> dict:
    detector = Detector()
    detection_results = detector.detect_objects(video_file_path)

    task_results = {
        "task_id": self.request.id,
        "detection_results": detection_results,
    }

    delete_processed_video(video_file_path)

    return task_results


@celery_instance.task
def update_detection_result_task(
        task_results: dict
) -> None:

    with get_sync_session() as db:
        detection_results = task_results.get("detection_results")
        task_id = task_results.get("task_id")
        status = DetectionStatus.SUCCESS

        if not detection_results:
            status = DetectionStatus.FAILURE

        update_detection_result(db, task_id, status, detection_results)

        logging.info(
            f"Successfully updated DetectionResult with task_id: '{task_id}'"
        )
