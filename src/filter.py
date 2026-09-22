import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Words that suggest YOU were venting or having a hard time
VENT_KEYWORDS = [
    # setbacks
    "rejected", "reject", "didn't get", "didnt get", "no offer",
    "turned down", "denied", "failed", "no response", "ghosted",
    # feelings
    "sucks", "gutted", "devastated", "disappointed", "upset",
    "stressed", "anxious", "anxiety", "depressed", "burnt out",
    "burned out", "overwhelmed", "exhausted", "lonely", "hurt",
    "angry", "frustrated", "scared", "worried", "crying", "cried",
    # phrasings
    "i can't", "i cant", "i hate", "i'm done", "im done",
    "worst", "terrible", "awful", "miserable", "hopeless",
    "don't know what to do", "dont know what to do",
]


def is_vent_message(text, your_name):
    """Rough heuristic: your message containing venting language."""
    return any(kw in text.lower() for kw in VENT_KEYWORDS)


def extract_support_pairs(messages, your_name, their_name, window=3):
    """
    Find your venting messages, then grab their next several replies
    as a 'support exchange' example.
    """
    pairs = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        if msg["sender"] == your_name and is_vent_message(msg["text"], your_name):
            # Collect your vent message
            vent_text = msg["text"]

            # Look ahead for their reply/replies
            replies = []
            j = i + 1
            while j < len(messages) and len(replies) < window:
                if messages[j]["sender"] == their_name:
                    replies.append(messages[j]["text"])
                elif messages[j]["sender"] == your_name:
                    break  # you started talking again, stop collecting
                j += 1

            if replies:
                pairs.append({
                    "vent": vent_text,
                    "response": " ".join(replies)
                })
            i = j
        else:
            i += 1

    return pairs


def save_candidate_pairs(pairs, output_path="data/processed/candidate_pairs.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    print(f"Found {len(pairs)} candidate exchanges -> {output_path}")
    print("Review this file by hand and copy your favorites into style_examples.json")


if __name__ == "__main__":
    with open("data/processed/messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    # Update these to match the actual sender_name strings in your export
    YOUR_NAME = "Your Name"
    THEIR_NAME = "Their Name"

    pairs = extract_support_pairs(messages, YOUR_NAME, THEIR_NAME)
    save_candidate_pairs(pairs)