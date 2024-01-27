from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from results_app.enums import DetectionStatus
from user_app.models import Base, User


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(UUID(as_uuid=True))
    status = Column(Enum(DetectionStatus), default=DetectionStatus.PROCESSING)
    result = Column(JSON, default=list)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))

    user = relationship("User", back_populates="detection_results")
