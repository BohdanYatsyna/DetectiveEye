import aiofiles
import os
import shutil

from fastapi import UploadFile


async def upload_video_to_temp_folder(video_file: UploadFile, video_path: str):
    os.makedirs(os.path.dirname(video_path), exist_ok=True)

    try:
        async with aiofiles.open(video_path, "wb") as temp_file:
            while True:
                contents = await video_file.read(1024*1024)
                if not contents:
                    break
                await temp_file.write(contents)
    except Exception as e:
        return {"message": f"There was an error uploading the file: {e}"}
    finally:
        await video_file.close()


def clean_up_processed_files(video_folder_path: str):
    try:
        shutil.rmtree(video_folder_path)
        print(f"Successfully cleaned up '{video_folder_path}'")
    except Exception as e:
        print(
            f"Error during cleanup of '{video_folder_path}': "
            f"Error message '{e}'"
        )
