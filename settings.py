from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DetectiveEye"

    DATABASE_URL: str | None = "postgresql+asyncpg://postgres:postgres@192.168.31.136/detect"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()