from fastapi import (
    APIRouter, Depends, HTTPException, File, UploadFile
)
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from video_analysis.tasks import (
    detect_objects_on_video_task
)
from db.async_database_session import get_async_session
from settings import settings
from video_analysis.detection_results import crud, schemas
from video_analysis.utils import (
    pass_file_extension_check, upload_file_to_temp_folder
)
from users.models import User
from users.users import current_active_user


results_router = APIRouter()


@results_router.post(
    "/detect_objects/", response_model=schemas.DetectionResult
)
async def upload_video_to_start_detecting_objects(
        video_file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):

    if not pass_file_extension_check(video_file):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid file type. Only next video extensions are allowed: "
                f"{settings.SUPPORTED_FILE_EXTENSIONS}"
            )
        )

    uploaded_video_path = await upload_file_to_temp_folder(video_file)

    detection_task = detect_objects_on_video_task.apply_async(
        args=[uploaded_video_path]
    )
    detection_result_in_processing = await crud.create_detection_result(
        db, task_id=detection_task.id, user_id=user.id
    )

    return detection_result_in_processing


@results_router.get(
    "/detection_results/", response_model=list[schemas.DetectionResult]
)
async def read_results(
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    db_detection_results_list = await crud.get_user_detection_results(
        db, user.id
    )

    return db_detection_results_list


@results_router.get(
    "/detection_results/{task_id}", response_model=schemas.DetectionResult
)
async def read_result_by_task_id(
        task_id: UUID,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    db_detection_result = await crud.get_detection_result_by_task_id(
        db, task_id, user.id
    )

    if db_detection_result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found or not accessible for current user"
        )

    return db_detection_result
