from fastapi import UploadFile

from sqlalchemy.dialects.postgresql import UUID
from settings import CeleryConfig, celery_instance
from db.sync_database_session import get_sync_session
from video_analysis.results.enums import DetectionStatus
from video_analysis.results.crud import update_detection_result_with_celery
from video_analysis.video_split import split_video_into_frames
from video_analysis.video_processing import (
    clean_up_processed_files, upload_video_to_temp_folder
)


@celery_instance.task(bind=True)
def process_video_task(
        self, frames_path: str, video_path: str, video_folder_path: str
) -> tuple:
    try:
        frame_paths = split_video_into_frames(video_path, frames_path)
        clean_up_processed_files(video_folder_path)

        task_result = {"task_id": self.request.id, "frame_paths": frame_paths}
        return task_result

    except Exception as e:
        task_result = {"task_id": self.request.id, "error": [str(e)]}
        return task_result


@celery_instance.task
def update_detection_result_task(
        task_result: dict
) -> str:

    with get_sync_session() as db:
        error = task_result.get("error")
        task_id = task_result.get("task_id")

        if error:
            status = DetectionStatus.FAILURE
            result = [error]
        else:
            status = DetectionStatus.SUCCESS
            result = task_result.get("frame_paths")

        update_detection_result_with_celery(db, task_id, status, result)

    return f"DetectionResult with task_id: '{task_id}' updated successfully"