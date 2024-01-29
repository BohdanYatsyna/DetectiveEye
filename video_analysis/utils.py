import os
import uuid

from settings import settings
from fastapi import UploadFile


def get_file_extension(file: UploadFile) -> str:
    return file.filename.split(".")[-1].lower()


def get_uuid_name() -> str:
    return str(uuid.uuid4())


def get_video_paths() -> tuple:
    video_folder_name = get_uuid_name()

    video_folder_path = os.path.join(
        settings.MEDIA_TEMP, f"{video_folder_name}"
    )
    video_path = os.path.join(video_folder_path, f"{video_folder_name}.mp4")
    frames_path = os.path.join(video_folder_path, "frames")

    return frames_path, video_path, video_folder_path
