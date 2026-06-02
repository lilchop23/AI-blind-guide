import requests
import time
import logging

logger = logging.getLogger(__name__)

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """You are a warm, calm and intelligent AI guide for a blind person.
- Describe surroundings clearly — objects, people, hazards, signs, distances
- Guide navigation step by step when heading somewhere
- Warn IMMEDIATELY about any danger — steps, traffic, obstacles
- Keep responses SHORT — 2 to 3 sentences maximum
- Never say I can see an image — speak as if you are physically there
- Use direction words: left, right, ahead, behind, arm's length, 2 steps away
- Be warm, reassuring and friendly at all times
- If you see text in the image, read it out
"""

conversation_history = []
MAX_HISTORY = 10


def chat(user_message: str, image_b64: str | None = None, retry: int = 0) -> str:
    parts = []
    if image_b64:
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": image_b64
            }
        })
    parts.append({"text": user_message})

    conversation_history.append({"role": "user", "parts": parts})
    trimmed = conversation_history[-MAX_HISTORY:]

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": trimmed,
        "generationConfig": {
            "maxOutputTokens": 300,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=25
        )
        data = response.json()

        if "error" in data:
            code = data["error"].get("code", 0)
            if code == 429 and retry < 3:
                print("[Brain]: Rate limited, waiting 20 seconds...")
                time.sleep(20)
                conversation_history.pop()
                return chat(user_message, image_b64, retry + 1)
            logger.error(f"Gemini error: {data}")
            return "I had trouble thinking. Please try again."

        reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        conversation_history.append({"role": "model", "parts": [{"text": reply}]})
        return reply

    except requests.Timeout:
        return "That took too long. Please try again."
    except Exception as e:
        logger.error(f"Brain error: {e}")
        return "Something went wrong. Please speak again."


def reset_conversation():
    conversation_history.clear()
    print("[Brain]: Conversation reset")
