import os
import logging

from celery import Celery
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path


load_dotenv()


# FastAPI settings
class Settings(BaseSettings):
    PROJECT_NAME: str = "DetectiveEye"
    DATABASE_URL: str = os.getenv("ENV_DATABASE_URL")
    ROOT_DIR: Path = Path(__file__).resolve().parent

    # Temporary storage for saving video and other files
    TEMP_FOLDER: Path = os.path.join(ROOT_DIR, "temp_storage")

    # File extension supported for objects detection
    SUPPORTED_FILE_EXTENSIONS: list[str] = ["mp4"]
    TOKEN_SECRET: str = os.getenv("ENV_TOKEN_SECRET")

    # Specifying exact Detectron2 model settings file
    DETECTRON2_MODEL_CONFIG: str = os.getenv(
        "ENV_DETECTRON2_MODEL_CONFIG",
        "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
    )
    # Set threshold for the model to show results with above prediction score
    DETECTRON2_SCORE_THRESH_TEST: float = float(os.getenv(
        "ENV_DETECTRON2_SCORE_THRESH_TEST", "0.7"
    ))
    # Choosing CPU or GPU mode
    DETECTRON2_DEVICE: str = os.getenv(
        "ENV_DETECTRON2_DEVICE", "cpu"
    )

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


# Logs configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

