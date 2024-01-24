# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
#
# from user_app.users import current_active_user
# from results_app import crud, schemas
# from db.database import get_async_session
# from user_app.models import User
# from fastapi_users import FastAPIUsers
#
#
# results_router = APIRouter()
#
#
# @results_router.post("/detect_object/{video_url}", response_model=schemas.DetectionResult)
# async def create_detection_request(video_url: str = "http://afdsgdhgjfhkl.adsfg.asfdg.sfdgh/asfd", user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
#     task_id = "test_task_id"
#     detection_result = schemas.DetectionResultCreate(video_url=video_url, task_id=task_id)
#     return await crud.create_detection_result(db, detection_result, user.id)
#
# @results_router.get("/results/", response_model=List[schemas.DetectionResult])
# async def read_results(user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
#     return await crud.get_user_detection_results(db, user.id)
#
# @results_router.get("/results/{result_id}", response_model=schemas.DetectionResult)
# async def read_result(result_id: int, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
#     db_result = await crud.get_detection_result(db, result_id)
#     if db_result is None or db_result.user_id != user.id:
#         raise HTTPException(status_code=404, detail="Result not found")
#     return db_result

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from results_app import crud, schemas
from db.database import get_async_session
from user_app.models import User
from user_app.users import current_active_user
from fastapi_users import FastAPIUsers

results_router = APIRouter()

@results_router.post("/detect_object/{video_url}", response_model=schemas.DetectionResult)
async def create_detection_request(video_url: str, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    task_id = "test_task_id"
    detection_result = schemas.DetectionResultCreate(video_url=video_url, task_id=task_id)
    return await crud.create_detection_result(db, detection_result, user.id)

@results_router.get("/results/", response_model=List[schemas.DetectionResult])
async def read_results(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    return await crud.get_user_detection_results(db, user.id)

@results_router.get("/results/{result_id}", response_model=schemas.DetectionResult)
async def read_result(result_id: int, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    db_result = await crud.get_detection_result(db, result_id)
    if db_result is None or db_result.user_id != user.id:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result
