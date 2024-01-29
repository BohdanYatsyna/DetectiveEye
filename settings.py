import os

from celery import Celery
from pydantic_settings import BaseSettings
from pathlib import Path


# TODO: change variables with sensitive info and move to env
class Settings(BaseSettings):
    PROJECT_NAME: str = "DetectiveEye"

    DATABASE_URL: str | None = "postgresql+asyncpg://postgres:postgres@192.168.31.136/detect"
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    MEDIA_TEMP: Path = os.path.join(ROOT_DIR, "media", "temp")

    TOKEN_SECRET: str = "SECRET"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()


# For Celery, as tool for distributed tasks execution used in video_analysis
class CeleryConfig:
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    broker_connection_retry_on_startup = True


celery_instance = Celery("video_analysing")
celery_instance.config_from_object(CeleryConfig)
