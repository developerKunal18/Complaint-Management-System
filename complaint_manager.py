from config import (
    COMPLAINT_FILE,
    COMPLAINANT_FILE,
    STAFF_FILE,
    COMPLAINT_CATEGORIES,
    PRIORITIES
)
from storage import load_data, save_data, next_id
from complainant_manager import get_complainant
from staff_manager import get_staff
from utils import (
    read_text,
    read_positive_int,
    timestamp,
    print_table
)


def create_complaint():
    print("\n--- Submit Complaint ---")

    complainant_id = read_positive_int("Complainant ID: ")
    complainant = get_complainant(complainant_id)

    if not complainant:
        print("Complainant not found. Register the person first.")
        return

    title = read_text("Complaint title: ")
    description = read_text("Description: ")

    print("Categories:", ", ".join(COMPLAINT_CATEGORIES))
    category = read_text("Category: ").title()

    if category not in COMPLAINT_CATEGORIES:
        print("Invalid complaint category.")
        return

    print("Priorities:", ", ".join(PRIORITIES))
    priority = read_text("Priority: ").title()

    if priority not in PRIORITIES:
        print("Invalid priority.")
        return

    complaints = load_data(COMPLAINT_FILE)

    complaint = {
        "id": next_id(complaints),
        "complainant_id": complainant_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "assigned_to": None,
        "resolution_notes": "",
        "created_at": timestamp(),
        "updated_at": timestamp(),
        "resolved_at": None,
        "closed_at": None
    }

    complaints.append(complaint)
    save_data(COMPLAINT_FILE, complaints)

    print("Complaint submitted successfully.")
    print(f"Complaint ID: {complaint['id']}")
    print("Current status: Open")


def list_complaints(status_filter=None):
    complaints = load_data(COMPLAINT_FILE)
    complainants = {
        c["id"]: c["name"]
        for c in load_data(COMPLAINANT_FILE)
    }
    staff_members = {
        s["id"]: s["name"]
        for s in load_data(STAFF_FILE)
    }

    rows = []

    for complaint in complaints:
        if status_filter and complaint["status"] != status_filter:
            continue

        staff_id = complaint.get("assigned_to")

        rows.append([
            complaint["id"],
            complainants.get(complaint["complainant_id"], "Unknown"),
            complaint["title"],
            complaint["category"],
            complaint["priority"],
            complaint["status"],
            staff_members.get(staff_id, "Unassigned")
        ])

    print_table(
        [
            "ID", "Complainant", "Title", "Category",
            "Priority", "Status", "Assigned Staff"
        ],
        rows
    )


def assign_complaint():
    print("\n--- Assign Complaint ---")

    complaint_id = read_positive_int("Complaint ID: ")
    staff_id = read_positive_int("Staff ID: ")

    complaints = load_data(COMPLAINT_FILE)
    complaint = next(
        (c for c in complaints if c["id"] == complaint_id),
        None
    )

    if not complaint:
        print("Complaint not found.")
        return

    if complaint["status"] in ["Resolved", "Closed"]:
        print("Resolved or closed complaints cannot be reassigned.")
        return

    staff = get_staff(staff_id)

    if not staff:
        print("Active staff member not found.")
        return

    complaint["assigned_to"] = staff_id
    complaint["status"] = "Assigned"
    complaint["updated_at"] = timestamp()

    save_data(COMPLAINT_FILE, complaints)

    print(
        f"Complaint {complaint_id} assigned to "
        f"{staff['name']} successfully."
    )


def update_complaint_status():
    print("\n--- Update Complaint Status ---")

    complaint_id = read_positive_int("Complaint ID: ")
    complaints = load_data(COMPLAINT_FILE)

    complaint = next(
        (c for c in complaints if c["id"] == complaint_id),
        None
    )

    if not complaint:
        print("Complaint not found.")
        return

    current_status = complaint["status"]

    transitions = {
        "Open": ["Assigned"],
        "Assigned": ["In Progress", "Open"],
        "In Progress": ["Assigned", "Resolved"],
        "Resolved": ["Closed", "In Progress"],
        "Closed": []
    }

    allowed = transitions[current_status]

    if not allowed:
        print("This complaint is already closed.")
        return

    print(f"Current status: {current_status}")
    print("Allowed next statuses:", ", ".join(allowed))

    new_status = read_text("New status: ").title()

    if new_status not in allowed:
        print("Invalid status transition.")
        return

    if new_status == "In Progress" and not complaint.get("assigned_to"):
        print("Assign this complaint to a staff member first.")
        return

    if new_status == "Resolved":
        notes = read_text("Resolution notes: ")
        complaint["resolution_notes"] = notes
        complaint["resolved_at"] = timestamp()

    if new_status == "In Progress":
        complaint["resolved_at"] = None
        complaint["resolution_notes"] = ""

    if new_status == "Closed":
        if not complaint.get("resolution_notes"):
            print("Resolution notes are required before closing.")
            return

        complaint["closed_at"] = timestamp()

    if new_status == "Resolved":
        complaint["closed_at"] = None

    complaint["status"] = new_status
    complaint["updated_at"] = timestamp()

    save_data(COMPLAINT_FILE, complaints)

    print(f"Complaint status updated to {new_status}.")


def search_complaint():
    print("\n--- Search Complaint ---")

    complaint_id = read_positive_int("Complaint ID: ")
    complaints = load_data(COMPLAINT_FILE)

    complaint = next(
        (c for c in complaints if c["id"] == complaint_id),
        None
    )

    if not complaint:
        print("Complaint not found.")
        return

    complainant = get_complainant(complaint["complainant_id"])
    staff_id = complaint.get("assigned_to")
    staff = get_staff(staff_id) if staff_id else None

    print("\n========== COMPLAINT DETAILS ==========")
    print(f"ID: {complaint['id']}")
    print(f"Title: {complaint['title']}")
    print(f"Description: {complaint['description']}")
    print(f"Complainant: {complainant['name'] if complainant else 'Unknown'}")
    print(f"Category: {complaint['category']}")
    print(f"Priority: {complaint['priority']}")
    print(f"Status: {complaint['status']}")
    print(f"Assigned Staff: {staff['name'] if staff else 'Unassigned'}")
    print(f"Resolution: {complaint['resolution_notes'] or 'Not resolved'}")
    print(f"Created: {complaint['created_at']}")
    print(f"Last Updated: {complaint['updated_at']}")
    print("=======================================")


def complaint_menu():
    while True:
        print("\n--- Complaint Management ---")
        print("1. Submit complaint")
        print("2. View all complaints")
        print("3. View open complaints")
        print("4. Assign complaint")
        print("5. Update complaint status")
        print("6. Search complaint")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            create_complaint()
        elif choice == "2":
            list_complaints()
        elif choice == "3":
            list_complaints("Open")
        elif choice == "4":
            assign_complaint()
        elif choice == "5":
            update_complaint_status()
        elif choice == "6":
            search_complaint()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
