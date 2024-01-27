import shutil
import os

from fastapi import (
    APIRouter, Depends, HTTPException, File, UploadFile, BackgroundTasks
)
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from celery_worker.worker import process_video_task
from db.database import get_async_session
from results_app import crud, schemas
from service.utils import get_video_paths, get_file_extension
from service.video_processing import upload_video_to_temp_folder
from user_app.models import User
from user_app.users import current_active_user


results_router = APIRouter()


@results_router.post(
    "/detect_objects/", response_model=schemas.DetectionResult
)
async def upload_video_for_detecting_objects(
        video_file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):
    file_extension = get_file_extension(video_file)

    if file_extension != "mp4":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only '.mp4' video files are allowed."
        )

    frames_path, video_path, video_folder_path = get_video_paths()
    upload_video_to_temp_folder(video_file, video_path)

    task = process_video_task.delay(
        frames_path, video_path, video_folder_path
    )

    new_detection_result = await crud.create_detection_result(
        db, task_id=task.id, user_id=user.id
    )

    return new_detection_result


@results_router.get("/results/", response_model=list[schemas.DetectionResult])
async def read_results(
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    results_list = await crud.get_user_detection_results(db, user.id)

    return results_list


@results_router.get(
    "/results/{task_id}", response_model=schemas.DetectionResult
)
async def read_result(
        task_id: UUID,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    db_result = await crud.get_detection_result(db, task_id)

    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    elif db_result.user_id != user.id:
        raise HTTPException(
            status_code=400, detail="User can see only own results"
        )

    return db_result


@results_router.put(
    "/results/{task_id}", response_model=schemas.DetectionResult
)
async def update_result(
    task_id: UUID,
    detection_result_update: schemas.DetectionResultUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    existing_result = await crud.get_detection_result(db, task_id)
    if not existing_result or existing_result.user_id != user.id:
        raise HTTPException(
            status_code=404,
            detail="Result not found or not owned by the user"
        )

    updated_result = await crud.update_detection_result(
        db, task_id, detection_result_update
    )

    if not updated_result:
        raise HTTPException(status_code=404, detail="Result not found")

    return updated_result
