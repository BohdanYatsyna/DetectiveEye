from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from video_analysis.results.enums import DetectionStatus
from video_analysis.results import models, schemas


async def create_detection_result(
        db: AsyncSession,
        task_id: UUID,
        user_id: UUID,
):
    db_detection_result = models.DetectionResult(
        task_id=task_id,
        user_id=user_id,
    )
    db.add(db_detection_result)

    await db.commit()
    await db.refresh(db_detection_result)

    return db_detection_result


async def get_detection_result_by_task_id(db: AsyncSession, task_id: UUID):
    result = await db.execute(select(models.DetectionResult).where(
        models.DetectionResult.task_id == task_id
    ))

    return result.scalar_one_or_none()


async def get_user_detection_results(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(models.DetectionResult).where(
        models.DetectionResult.user_id == user_id
    ))

    return result.scalars().all()

def update_detection_result_with_celery(
        db, task_id: UUID, status: DetectionStatus, result: list
):
    db_detection_result = db.query(models.DetectionResult).filter(
        models.DetectionResult.task_id == task_id
    ).first()

    try:
        if db_detection_result:
            db_detection_result.status = status
            db_detection_result.result = result
            db.commit()
            db.refresh(db_detection_result)
            return db_detection_result
    except Exception as e:
        print(e)