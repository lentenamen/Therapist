import sys

# Windows consoles default to cp1252 and choke on em dashes, emoji, etc.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.append("src")

from chat import run


if __name__ == "__main__":
    run()
