import json
import os
import sys
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def load_log():
    if not os.path.exists(config.REJECTION_LOG_PATH):
        return []
    with open(config.REJECTION_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_log(log):
    os.makedirs(os.path.dirname(config.REJECTION_LOG_PATH), exist_ok=True)
    with open(config.REJECTION_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def add_entry(company, role, note=""):
    log = load_log()
    log.append({
        "company": company,
        "role": role,
        "note": note,
        "date": str(date.today())
    })
    save_log(log)
    print(f"Logged: {company} - {role} ({len(log)} total rejections tracked)")


def summary():
    log = load_log()
    print(f"\nTotal rejections logged: {len(log)}")
    for entry in log:
        print(f"  {entry['date']} - {entry['company']} ({entry['role']})")


if __name__ == "__main__":
    summary()