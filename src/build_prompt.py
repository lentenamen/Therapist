import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def build_system_prompt():
    with open(config.STYLE_EXAMPLES_PATH, "r", encoding="utf-8") as f:
        style_data = json.load(f)

    style_notes = "\n".join(f"- {note}" for note in style_data["style_notes"])

    examples_text = ""
    for i, ex in enumerate(style_data["examples"], 1):
        examples_text += f"\nExample {i}:\nFriend: \"{ex['vent']}\"\nThem: \"{ex['response']}\"\n"

    prompt = f"""You are modeled after the conversational style of someone the user 
talks to who is warm and supportive during hard moments, specifically around 
job/internship rejections.

Style notes:
{style_notes}

Here are real examples of how they respond:
{examples_text}

Match this tone and rhythm. Be genuinely comforting but in their voice, not a 
generic supportive-bot voice. You are a supportive tool, not a therapist or 
counselor — if things seem to go beyond rejection-stress into something heavier, 
gently suggest talking to a real person too."""

    return prompt


if __name__ == "__main__":
    print(build_system_prompt())