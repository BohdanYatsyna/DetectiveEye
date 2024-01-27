from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from results_app.enums import DetectionStatus


class DetectionResultBase(BaseModel):
    task_id: UUID
    status: DetectionStatus
    result: Optional[list] = []


class DetectionResultCreate(DetectionResultBase):
    pass


class DetectionResultUpdate(DetectionResultBase):
    status: DetectionStatus
    result: Optional[list] = None


class DetectionResult(DetectionResultBase):
    id: int
    user_id: UUID

    class Config:
        from_attributes = True
