import os

from celery import Celery
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "DetectiveEye"

    DATABASE_URL: str = os.getenv("ENV_DATABASE_URL")
    ROOT_DIR: Path = Path(__file__).resolve().parent
    TEMP_VIDEO_FOLDER: Path = os.path.join(ROOT_DIR, "temp_storage")

    TOKEN_SECRET: str = os.getenv("ENV_TOKEN_SECRET")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()


# For Celery, as tool for distributed tasks execution used in video_analysis
class CeleryConfig:
    broker_url = os.getenv("ENV_BROKER_URL")
    result_backend = os.getenv("ENV_RESULT_BACKEND")
    broker_connection_retry_on_startup = True


celery_instance = Celery("video_analysing")
celery_instance.config_from_object(CeleryConfig)
