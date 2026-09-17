import json
import os
import glob
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def fix_encoding(text):
    """Instagram exports mangle emoji/special chars - this fixes it."""
    if not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


def find_thread_folder(keyword):
    """Find the inbox folder matching the target person."""
    pattern = os.path.join(config.INSTAGRAM_INBOX_PATH, f"*{keyword}*")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No thread found matching '{keyword}' in {config.INSTAGRAM_INBOX_PATH}")
    return matches[0]


def load_thread_messages(folder_path):
    """Instagram splits long threads into message_1.json, message_2.json, etc."""
    message_files = sorted(glob.glob(os.path.join(folder_path, "message_*.json")))
    if not message_files:
        raise FileNotFoundError(f"No message_*.json files found in {folder_path}")

    all_messages = []
    for file_path in message_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for msg in data.get("messages", []):
            all_messages.append({
                "sender": fix_encoding(msg.get("sender_name", "")),
                "text": fix_encoding(msg.get("content", "")),
                "timestamp_ms": msg.get("timestamp_ms", 0)
            })

    # Instagram exports messages newest-first; flip to chronological order
    all_messages.sort(key=lambda m: m["timestamp_ms"])
    return all_messages


def extract_and_save(output_path="data/processed/messages.json"):
    folder = find_thread_folder(config.TARGET_THREAD_KEYWORD)
    messages = load_thread_messages(folder)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(messages)} messages to {output_path}")
    return messages


if __name__ == "__main__":
    extract_and_save()