import sys
sys.path.append("src")

from rejection_log import add_entry, summary
from chat import run as run_chat


def menu():
    print("\n1. Chat / vent")
    print("2. Log a rejection")
    print("3. View rejection history")
    print("4. Quit")
    return input("> ")


if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == "1":
            run_chat()
        elif choice == "2":
            company = input("Company: ")
            role = input("Role: ")
            note = input("Note (optional): ")
            add_entry(company, role, note)
        elif choice == "3":
            summary()
        elif choice == "4":
            break