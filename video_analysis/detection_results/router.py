from celery import chain
from fastapi import (
    APIRouter, Depends, HTTPException, File, UploadFile
)
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from video_analysis.tasks import (
    detect_objects_on_video_task, update_detection_result_task
)
from db.async_database_session import get_async_session
from video_analysis.detection_results import crud, schemas
from video_analysis.utils import upload_video_to_temp_folder
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

    if video_file.filename.split(".")[-1].lower() != "mp4":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only '.mp4' video files are allowed."
        )

    uploaded_video_path = await upload_video_to_temp_folder(video_file)

    task_chain = chain(
        detect_objects_on_video_task.s(uploaded_video_path),
        update_detection_result_task.s()
    )
    result = task_chain.apply_async()

    new_detection_result = await crud.create_detection_result(
        db, task_id=result.parent.id, user_id=user.id
    )

    return new_detection_result


@results_router.get(
    "/detection_results/", response_model=list[schemas.DetectionResult]
)
async def read_results(
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    results_list = await crud.get_user_detection_results(db, user.id)

    return results_list


@results_router.get(
    "/detection_results/{task_id}", response_model=schemas.DetectionResult
)
async def read_result_by_task_id(
        task_id: UUID,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    db_result = await crud.get_detection_result_by_task_id(db, task_id)

    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    elif db_result.user_id != user.id:
        raise HTTPException(
            status_code=400, detail="User can see only own results"
        )

    return db_result
