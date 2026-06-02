import sys
import os
import time
import logging

# Setup logging
logging.basicConfig(
    filename=os.path.expanduser("~/blind_guide/logs/session.log"),
    level=logging.ERROR,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

sys.path.insert(0, os.path.expanduser("~/blind_guide"))

from modules.voice import speak, listen
from modules.camera import capture_photo
from modules.brain import chat, reset_conversation
from modules.memory import save_memory, get_memory_context

# Words that trigger camera
VISUAL_TRIGGERS = [
    "see", "look", "what", "where", "around", "here", "there",
    "ahead", "front", "left", "right", "behind", "safe", "road",
    "street", "room", "obstacle", "door", "stairs", "step", "car",
    "person", "outside", "inside", "going", "heading", "near",
    "describe", "help", "guide", "read", "sign", "anything"
]

# Words that exit the app
EXIT_WORDS = ["bye", "goodbye", "stop", "exit", "quit", "shutdown"]


def needs_camera(text: str) -> bool:
    return any(word in text.lower() for word in VISUAL_TRIGGERS)


def is_exit(text: str) -> bool:
    return any(word in text.lower() for word in EXIT_WORDS)


def main():
    speak(
        "Hello! I am your personal AI guide. "
        "I am here with you. "
        "Just talk to me naturally. "
        "Tell me where you are going, "
        "what you need, "
        "or ask me what is around you. "
        "I am always listening."
    )

    silence_count = 0

    while True:
        try:
            # Listen for user
            user_input = listen()

            if not user_input:
                silence_count += 1
                if silence_count >= 4:
                    speak("I am still here. Just talk to me whenever you are ready.")
                    silence_count = 0
                continue

            silence_count = 0

            # Check exit
            if is_exit(user_input):
                speak("Goodbye! Stay safe. I am always here when you need me.")
                break

            # Check reset
            if "reset" in user_input.lower() or "forget" in user_input.lower():
                reset_conversation()
                speak("Done. I have cleared our conversation. Fresh start!")
                continue

            # Decide if camera needed
            image_b64 = None
            if needs_camera(user_input):
                speak("One moment, let me look around for you.")
                image_b64 = capture_photo()
                if image_b64 is None:
                    speak("Camera did not respond. Let me answer based on what I know.")

            # Get AI response — inject memory context
            memory_context = get_memory_context()
            full_message = user_input
            if memory_context:
                full_message = user_input + "\n\n" + memory_context

            response = chat(full_message, image_b64)

            # Speak response
            speak(response)

            # Save to memory if camera was used
            if image_b64:
                save_memory(response, user_input)

        except KeyboardInterrupt:
            speak("Shutting down. Take care of yourself.")
            break
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            speak("I hit a small problem. Let us keep going.")
            time.sleep(1)


if __name__ == "__main__":
    main()
