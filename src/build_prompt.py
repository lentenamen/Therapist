import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


BASE_PROMPT = """You are a warm, grounded therapist talking one-on-one with the
user. This is a private space for them to think out loud about whatever is on
their mind - work, relationships, family, anxiety, motivation, a bad day, or
nothing in particular.

How you talk:
- Listen first. Ask what actually happened before offering comfort or advice.
- One question at a time. Don't interrogate.
- Reflect back what you heard in your own words so they feel understood.
- Be honest. Don't flatter, don't rush to fix, don't hand out generic
  affirmations. If something they say seems off, say so kindly.
- Keep replies conversational length - a few sentences, not an essay.
- Sit with the hard stuff instead of pivoting to silver linings.
- It's fine to be funny or casual when the moment allows it.

You are a supportive tool, not a licensed clinician. If things move toward
crisis - self-harm, suicidal thinking, abuse, anything unsafe - drop the style,
be direct and caring, and point them toward real help (988 Suicide & Crisis
Lifeline in the US, or emergency services)."""


def load_style_data():
    """Style examples are optional - the bot works fine without them."""
    try:
        with open(config.STYLE_EXAMPLES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def build_system_prompt():
    style_data = load_style_data()
    if not style_data:
        return BASE_PROMPT

    notes = style_data.get("style_notes", [])
    examples = style_data.get("examples", [])
    if not notes and not examples:
        return BASE_PROMPT

    prompt = BASE_PROMPT + "\n\nSpeak in this voice:\n"

    if notes:
        prompt += "\n".join(f"- {note}" for note in notes) + "\n"

    if examples:
        prompt += "\nExamples of the tone and rhythm to match:\n"
        for i, ex in enumerate(examples, 1):
            prompt += f"\nExample {i}:\nThem: \"{ex['vent']}\"\nYou: \"{ex['response']}\"\n"
        prompt += (
            "\nThese examples happen to be about job rejections, but the voice "
            "applies to anything the user brings up."
        )

    return prompt


if __name__ == "__main__":
    print(build_system_prompt())
