import json
import os
from datetime import datetime

MEMORY_FILE = os.path.expanduser("~/blind_guide/data/memory.json")


def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_memory(description: str, user_said: str):
    memory = load_memory()
    key = datetime.now().strftime("%Y-%m-%d %H:%M")
    memory[key] = {
        "description": description[:200],
        "user_said": user_said[:100],
        "time": key
    }
    if len(memory) > 30:
        oldest = sorted(memory.keys())[0]
        del memory[oldest]
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"[Memory]: Saved — {key}")


def get_memory_context() -> str:
    memory = load_memory()
    if not memory:
        return ""
    recent = list(memory.values())[-8:]
    lines = [f"  [{m['time']}] {m['description']}" for m in recent]
    return "\n[PLACES I HAVE BEEN]:\n" + "\n".join(lines)


def clear_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)
    print("[Memory]: Cleared")
