import aiofiles
import errno
import logging
import os
import uuid

from fastapi import UploadFile, HTTPException

from settings import settings


def get_file_extension(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1].lower()
    return file_extension


def pass_file_extension_check(file: UploadFile) -> bool:
    file_extension = get_file_extension(file)
    return file_extension in settings.SUPPORTED_FILE_EXTENSIONS


def create_temporary_file_path(file: UploadFile) -> str:
    file_extension = get_file_extension(file)
    temporary_file_name = str(uuid.uuid4())
    temporary_file_path = os.path.join(
        settings.TEMP_FOLDER,
        f"{temporary_file_name}.{file_extension}"
    )
    return temporary_file_path


async def upload_file(file: UploadFile) -> str:
    upload_path = create_temporary_file_path(file)

    try:
        async with aiofiles.open(upload_path, "wb") as temp_file:
            while True:
                contents = await file.read(1024 * 1024)
                if not contents:
                    break
                await temp_file.write(contents)

    except PermissionError:
        raise HTTPException(
            status_code=500,
            detail="File permission error occurred"
        )
    except OSError as error:
        logging.error(f"File upload error: {error}")
        if error.errno == errno.ENOSPC:
            raise HTTPException(
                status_code=507,
                detail="Server storage is full, please try again later"
            )

        raise HTTPException(
            status_code=500,
            detail="Unexpected error with uploading, please try again"
        )

    return upload_path


def delete_file(file_path: str) -> None:
    os.remove(file_path)
