import cv2
import os


def split_video_into_frames(video_path, output_folder):
    vid_obj = cv2.VideoCapture(video_path)
    count = 0
    success = True
    frame_paths = []

    os.makedirs(output_folder, exist_ok=True)

    while success:
        success, image = vid_obj.read()
        if success:
            frame_path = os.path.join(output_folder, f"frame{count}.jpg")
            cv2.imwrite(frame_path, image)
            frame_paths.append(frame_path)
            count += 1

    vid_obj.release()
    cv2.destroyAllWindows()

    print(
        f"Video has been split into frames successfully. "
        f"Frames quantity: {count}"
    )

    return frame_paths
