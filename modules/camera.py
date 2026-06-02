import subprocess
import base64
import os
import logging

logger = logging.getLogger(__name__)

PHOTO_PATH = "/sdcard/blind_guide_photo.jpg"

def capture_photo(camera_id: int = 0) -> str | None:
    """
    Takes a photo and returns it as base64 string.
    camera_id: 0 = back camera, 1 = front camera
    """
    try:
        # Take the photo
        result = subprocess.run(
            ["termux-camera-photo", "-c", str(camera_id), PHOTO_PATH],
            capture_output=True,
            timeout=10
        )

        # Check photo was saved
        if not os.path.exists(PHOTO_PATH):
            logger.error("Photo file not created")
            return None

        # Convert to base64 for Claude API
        with open(PHOTO_PATH, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        print("[Camera]: Photo captured successfully")
        return encoded

    except subprocess.TimeoutExpired:
        logger.error("Camera timed out")
        return None
    except Exception as e:
        logger.error(f"Camera error: {e}")
        return None
