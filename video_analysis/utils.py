import aiofiles
import logging
import os
import shutil
import uuid

from fastapi import UploadFile

from settings import settings


async def upload_video_to_temp_folder(video_file: UploadFile) -> str:
    new_name = f"{str(uuid.uuid4())}.mp4"
    video_file_full_path = os.path.join(settings.TEMP_VIDEO_FOLDER, new_name)

    async with aiofiles.open(video_file_full_path, "wb") as temp_file:
        while True:
            contents = await video_file.read(1024*1024)
            if not contents:
                break
            await temp_file.write(contents)

    return video_file_full_path


def delete_processed_video(video_file_path: str) -> None:
    if not os.path.isfile(video_file_path):
        logging.error(
            f"Unsuccessful attempt to delete video file: '{video_file_path}'"
        )

    os.remove(video_file_path)
    logging.info(f"Successfully cleaned up '{video_file_path}'")

