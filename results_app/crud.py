from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from results_app.enums import DetectionStatus
from results_app import models, schemas


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


async def get_detection_result(db: AsyncSession, task_id: UUID):
    result = await db.execute(select(models.DetectionResult).where(
        models.DetectionResult.task_id == task_id
    ))

    return result.scalar_one_or_none()


async def update_detection_result(
    db: AsyncSession,
    task_id: UUID,
    detection_result_update: schemas.DetectionResultUpdate
):
    result = await db.execute(select(models.DetectionResult).where(
        models.DetectionResult.task_id == task_id
    ))

    db_detection_result = result.scalar_one_or_none()

    if db_detection_result:
        db_detection_result.status = detection_result_update.status
        db_detection_result.result = detection_result_update.result

        await db.commit()
        await db.refresh(db_detection_result)

        return db_detection_result

    return None


async def get_user_detection_results(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(models.DetectionResult).where(
        models.DetectionResult.user_id == user_id
    ))

    return result.scalars().all()
