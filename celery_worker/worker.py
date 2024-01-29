from celery import Celery
from fastapi import UploadFile

from sqlalchemy.dialects.postgresql import UUID
from celery_worker.celery_config import CeleryConfig
from db.celery_session import get_sync_session
from results_app.enums import DetectionStatus
from results_app.crud import update_detection_result_with_celery
from service.video_split import split_video_into_frames
from service.video_processing import (
    clean_up_processed_files, upload_video_to_temp_folder
)


app = Celery("celery_worker")
app.config_from_object(CeleryConfig)


@app.task(bind=True)
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


@app.task
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