import sys
import os
import json
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from build_prompt import build_system_prompt

client = OpenAI(
    api_key=config.API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def load_history():
    try:
        with open(config.HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(conversation):
    os.makedirs(os.path.dirname(config.HISTORY_PATH), exist_ok=True)
    with open(config.HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)


def chat(user_message, conversation, system_prompt):
    conversation.append({"role": "user", "content": user_message})

    # Only send the recent window so long histories don't blow up the request
    recent = conversation[-config.HISTORY_WINDOW:]
    messages = [{"role": "system", "content": system_prompt}] + recent

    response = client.chat.completions.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        messages=messages
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return reply


def run():
    if not config.API_KEY:
        print("No GROQ_API_KEY found. Put it in your .env file and try again.")
        return

    system_prompt = build_system_prompt()
    conversation = load_history()

    if conversation:
        print(f"Picking up where you left off ({len(conversation)} messages).")
    print("Type 'quit' to exit, 'reset' to start fresh.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            break

        if user_input.lower() == "reset":
            conversation = []
            save_history(conversation)
            print("Cleared. Fresh start.\n")
            continue

        try:
            reply = chat(user_input, conversation, system_prompt)
        except Exception as e:
            # Drop the unanswered user message so history stays coherent
            conversation.pop()
            print(f"Something went wrong talking to the API: {e}\n")
            continue

        print("\n" + reply + "\n")
        save_history(conversation)

    save_history(conversation)
    print("Take care.")


if __name__ == "__main__":
    run()
