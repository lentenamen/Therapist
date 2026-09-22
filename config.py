import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"
MAX_TOKENS = 800

# Path to your unzipped Instagram export
INSTAGRAM_INBOX_PATH = "data/raw/your_instagram_activity/messages/inbox"

# The folder name (or partial match) for the person's thread
# e.g. if the folder is "username_1234567890", put "username" here
TARGET_THREAD_KEYWORD = "username_here"

STYLE_EXAMPLES_PATH = "data/style_examples.json"
HISTORY_PATH = "data/history.json"

# How many past messages to carry into each request
HISTORY_WINDOW = 40
