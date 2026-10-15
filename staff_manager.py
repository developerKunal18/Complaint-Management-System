from config import STAFF_FILE, COMPLAINT_FILE
from storage import load_data, save_data, next_id
from utils import read_text, valid_email, print_table


def add_staff():
    staff_members = load_data(STAFF_FILE)

    print("\n--- Add Staff Member ---")
    name = read_text("Staff name: ")
    email = read_text("Staff email: ").lower()
    department = read_text("Department: ")

    if not valid_email(email):
        print("Enter a valid email address.")
        return

    if any(s["email"].lower() == email for s in staff_members):
        print("This staff email is already registered.")
        return

    member = {
        "id": next_id(staff_members),
        "name": name,
        "email": email,
        "department": department,
        "active": True
    }

    staff_members.append(member)
    save_data(STAFF_FILE, staff_members)

    print(f"Staff member added. Staff ID: {member['id']}")


def list_staff():
    staff_members = load_data(STAFF_FILE)

    print_table(
        ["ID", "Name", "Email", "Department", "Status"],
        [
            [
                s["id"],
                s["name"],
                s["email"],
                s["department"],
                "Active" if s["active"] else "Inactive"
            ]
            for s in staff_members
        ]
    )


def get_staff(staff_id):
    return next(
        (
            s for s in load_data(STAFF_FILE)
            if s["id"] == staff_id and s["active"]
        ),
        None
    )


def deactivate_staff():
    staff_id = int(input("Staff ID to deactivate: ").strip())
    staff_members = load_data(STAFF_FILE)

    member = next(
        (s for s in staff_members if s["id"] == staff_id),
        None
    )

    if not member:
        print("Staff member not found.")
        return

    if not member["active"]:
        print("Staff member is already inactive.")
        return

    complaints = load_data(COMPLAINT_FILE)

    has_open_work = any(
        c.get("assigned_to") == staff_id
        and c["status"] in ["Assigned", "In Progress"]
        for c in complaints
    )

    if has_open_work:
        print(
            "Reassign or resolve this staff member's active complaints "
            "before deactivation."
        )
        return

    member["active"] = False
    save_data(STAFF_FILE, staff_members)

    print("Staff member deactivated.")


def staff_menu():
    while True:
        print("\n--- Staff Management ---")
        print("1. Add staff member")
        print("2. View staff")
        print("3. Deactivate staff member")
        print("0. Back")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                add_staff()
            elif choice == "2":
                list_staff()
            elif choice == "3":
                deactivate_staff()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Enter a valid numeric staff ID.")
