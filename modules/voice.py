import subprocess
import logging

logger = logging.getLogger(__name__)

def speak(text: str, rate: float = 1.0, pitch: float = 1.0):
    """
    Converts text to speech.
    rate: speed (0.5 slow — 2.0 fast)
    pitch: voice pitch (0.5 deep — 2.0 high)
    """
    try:
        print(f"\n[AI Guide]: {text}")
        subprocess.run(
            ["termux-tts-speak", "-r", str(rate), "-p", str(pitch), text],
            timeout=30
        )
    except subprocess.TimeoutExpired:
        logger.error("Speech timed out")
    except Exception as e:
        logger.error(f"Speech error: {e}")
        print(f"[Speech failed]: {e}")


def listen(timeout: int = 10) -> str | None:
    """
    Listens to user voice and returns text.
    Returns None if nothing was heard.
    """
    try:
        print("\n[Listening...]")
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        text = result.stdout.strip()
        if text:
            print(f"[You]: {text}")
            return text
        return None
    except subprocess.TimeoutExpired:
        logger.warning("Listening timed out")
        return None
    except Exception as e:
        logger.error(f"Listen error: {e}")
        return None
