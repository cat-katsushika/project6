import cv2

from django.core.files.base import ContentFile


def generate_thumbnail(video_path):
    # Capture the video
    vidcap = cv2.VideoCapture(video_path)

    # Read the first frame
    success, image = vidcap.read()

    if not success:
        raise ValueError("Could not read frame from video")

    # Convert the image to a PNG
    is_success, buffer = cv2.imencode(".png", image)

    if not is_success:
        raise ValueError("Could not encode image to PNG")

    return ContentFile(buffer.tobytes(), name="thumbnail.png")
