import os

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "DetectiveEye"

    DATABASE_URL: str | None = "postgresql+asyncpg://postgres:postgres@192.168.31.136/detect"
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    MEDIA_TEMP: Path = os.path.join(ROOT_DIR, "media", "temp")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
