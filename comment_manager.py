from config import COMMENT_FILE, COMPLAINT_FILE
from storage import load_data, save_data, next_id
from utils import read_text, read_positive_int, timestamp, print_table


def add_comment():
    print("\n--- Add Complaint Update ---")

    complaint_id = read_positive_int("Complaint ID: ")
    complaints = load_data(COMPLAINT_FILE)

    complaint = next(
        (c for c in complaints if c["id"] == complaint_id),
        None
    )

    if not complaint:
        print("Complaint not found.")
        return

    if complaint["status"] == "Closed":
        print("Closed complaints cannot be updated.")
        return

    author = read_text("Author name: ")
    message = read_text("Comment or update: ")

    comments = load_data(COMMENT_FILE)

    comment = {
        "id": next_id(comments),
        "complaint_id": complaint_id,
        "author": author,
        "message": message,
        "created_at": timestamp()
    }

    comments.append(comment)
    save_data(COMMENT_FILE, comments)

    print(f"Update added successfully. Update ID: {comment['id']}")


def view_comments():
    complaint_id = read_positive_int("Complaint ID: ")
    complaints = load_data(COMPLAINT_FILE)

    if not any(c["id"] == complaint_id for c in complaints):
        print("Complaint not found.")
        return

    comments = [
        c for c in load_data(COMMENT_FILE)
        if c["complaint_id"] == complaint_id
    ]

    comments.sort(key=lambda c: c["created_at"])

    print_table(
        ["Update ID", "Author", "Message", "Created At"],
        [
            [c["id"], c["author"], c["message"], c["created_at"]]
            for c in comments
        ]
    )


def comment_menu():
    while True:
        print("\n--- Complaint Updates ---")
        print("1. Add update")
        print("2. View updates for a complaint")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_comment()
        elif choice == "2":
            view_comments()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
