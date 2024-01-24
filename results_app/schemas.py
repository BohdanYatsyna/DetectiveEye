from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class DetectionResultBase(BaseModel):
    video_url: HttpUrl


class DetectionResultCreate(DetectionResultBase):
    pass


class DetectionResultUpdate(BaseModel):
    status: Optional[str]
    result: Optional[list]


class DetectionResult(DetectionResultBase):
    id: int
    task_id: str
    status: str
    result: Optional[str]  # JSON stored as string, convert to actual JSON when reading

    class Config:
        orm_mode = True
