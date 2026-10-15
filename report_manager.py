from config import (
    COMPLAINT_FILE,
    COMPLAINANT_FILE,
    STAFF_FILE
)
from storage import load_data
from utils import print_table


def dashboard():
    complaints = load_data(COMPLAINT_FILE)
    complainants = load_data(COMPLAINANT_FILE)
    staff_members = load_data(STAFF_FILE)

    print("\n========== COMPLAINT DASHBOARD ==========")
    print(f"Total complainants: {len(complainants)}")
    print(f"Total staff members: {len(staff_members)}")
    print(f"Total complaints: {len(complaints)}")

    for status in [
        "Open", "Assigned", "In Progress", "Resolved", "Closed"
    ]:
        count = sum(c["status"] == status for c in complaints)
        print(f"{status} complaints: {count}")

    print("=========================================")


def category_report():
    complaints = load_data(COMPLAINT_FILE)

    if not complaints:
        print("No complaints available.")
        return

    categories = {}

    for complaint in complaints:
        category = complaint["category"]
        categories[category] = categories.get(category, 0) + 1

    print_table(
        ["Category", "Complaint Count"],
        [[category, count] for category, count in sorted(categories.items())]
    )


def staff_workload_report():
    complaints = load_data(COMPLAINT_FILE)
    staff_members = load_data(STAFF_FILE)

    rows = []

    for staff in staff_members:
        assigned = [
            c for c in complaints
            if c.get("assigned_to") == staff["id"]
        ]

        active = [
            c for c in assigned
            if c["status"] in ["Assigned", "In Progress"]
        ]

        resolved = [
            c for c in assigned
            if c["status"] in ["Resolved", "Closed"]
        ]

        rows.append([
            staff["id"],
            staff["name"],
            "Active" if staff["active"] else "Inactive",
            len(assigned),
            len(active),
            len(resolved)
        ])

    print_table(
        [
            "Staff ID", "Name", "Status",
            "Total Assigned", "Active", "Resolved/Closed"
        ],
        rows
    )


def report_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Complaint dashboard")
        print("2. Category report")
        print("3. Staff workload report")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            category_report()
        elif choice == "3":
            staff_workload_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
