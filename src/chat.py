import sys
import os
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from build_prompt import build_system_prompt

client = OpenAI(
    api_key=config.API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def chat(user_message, conversation, system_prompt):
    conversation.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": system_prompt}] + conversation

    response = client.chat.completions.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        messages=messages
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return reply


def run():
    system_prompt = build_system_prompt()
    conversation = []
    print("Bot ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break
        reply = chat(user_input, conversation, system_prompt)
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    run()