from config import COMPLAINANT_FILE, COMPLAINT_FILE
from storage import load_data, save_data, next_id
from utils import read_text, valid_email, valid_phone, print_table


def add_complainant():
    complainants = load_data(COMPLAINANT_FILE)

    print("\n--- Register Complainant ---")
    name = read_text("Full name: ")
    email = read_text("Email: ").lower()
    phone = read_text("Phone number: ")

    if not valid_email(email):
        print("Enter a valid email address.")
        return

    if not valid_phone(phone):
        print("Phone number must contain 10 to 15 digits.")
        return

    if any(c["email"].lower() == email for c in complainants):
        print("This email address is already registered.")
        return

    if any(c["phone"] == phone for c in complainants):
        print("This phone number is already registered.")
        return

    complainant = {
        "id": next_id(complainants),
        "name": name,
        "email": email,
        "phone": phone
    }

    complainants.append(complainant)
    save_data(COMPLAINANT_FILE, complainants)

    print(f"Complainant registered. ID: {complainant['id']}")


def list_complainants():
    complainants = load_data(COMPLAINANT_FILE)

    print_table(
        ["ID", "Name", "Email", "Phone"],
        [
            [c["id"], c["name"], c["email"], c["phone"]]
            for c in complainants
        ]
    )


def get_complainant(complainant_id):
    return next(
        (
            c for c in load_data(COMPLAINANT_FILE)
            if c["id"] == complainant_id
        ),
        None
    )


def complainant_menu():
    while True:
        print("\n--- Complainant Management ---")
        print("1. Register complainant")
        print("2. View complainants")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_complainant()
        elif choice == "2":
            list_complainants()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
