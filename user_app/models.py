from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    detection_results = relationship("DetectionResult", back_populates="user")
