from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    detection_results: Mapped[list["DetectionResult"]] = relationship("DetectionResult", back_populates="user")















    # detection_results = relationship("DetectionResult", back_populates="user")