# from sqlalchemy.orm import Session
#
# from results_app.models import DetectionResult
# from results_app.schemas import DetectionResultCreate, DetectionResultUpdate
#
#
# def create_detection_result(db: Session, detection_result: DetectionResultCreate, user_id: int):
#     db_detection_result = DetectionResult(**detection_result.dict(), user_id=user_id)
#     db.add(db_detection_result)
#     db.commit()
#     db.refresh(db_detection_result)
#     return db_detection_result
#
#
# def update_detection_result(db: Session, result_id: int, detection_result: DetectionResultUpdate):
#     db_detection_result = db.query(DetectionResult).filter(DetectionResult.id == result_id).first()
#
#     if db_detection_result:
#         for var, value in vars(detection_result).items():
#             setattr(db_detection_result, var, value) if value else None
#         db.commit()
#         db.refresh(db_detection_result)
#         return db_detection_result
#
#     return None
#
# def get_user_detection_results(db: Session, user_id: str):
#     return db.query(DetectionResult).filter(DetectionResult.user_id == user_id).all()
#
#
# def get_detection_result(db: Session, result_id: int):
#     return db.query(DetectionResult).filter(DetectionResult.id == result_id).first()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from results_app.models import DetectionResult
from results_app.schemas import DetectionResultCreate, DetectionResultUpdate


async def create_detection_result(db: AsyncSession, detection_result: DetectionResultCreate, user_id: int):
    db_detection_result = DetectionResult(**detection_result.dict(), user_id=user_id)
    db.add(db_detection_result)
    await db.commit()
    await db.refresh(db_detection_result)
    return db_detection_result


async def update_detection_result(db: AsyncSession, result_id: int, detection_result: DetectionResultUpdate):
    result = await db.execute(select(DetectionResult).where(DetectionResult.id == result_id))
    db_detection_result = result.scalar_one_or_none()

    if db_detection_result:
        for var, value in vars(detection_result).items():
            if value:
                setattr(db_detection_result, var, value)
        await db.commit()
        await db.refresh(db_detection_result)
        return db_detection_result

    return None


async def get_user_detection_results(db: AsyncSession, user_id: str):
    result = await db.execute(select(DetectionResult).where(DetectionResult.user_id == user_id))
    return result.scalars().all()


async def get_detection_result(db: AsyncSession, result_id: int):
    result = await db.execute(select(DetectionResult).where(DetectionResult.id == result_id))
    return result.scalar_one_or_none()