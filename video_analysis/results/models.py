from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from video_analysis.results.enums import DetectionStatus
from users.models import Base, User


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    status: Mapped[DetectionStatus] = mapped_column(
        Enum(DetectionStatus), default=DetectionStatus.PROCESSING
    )
    result: Mapped[list] = mapped_column(JSON, default=list)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship("User", back_populates="detection_results")
