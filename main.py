from config import (
    COMPLAINANT_FILE,
    COMPLAINT_FILE,
    STAFF_FILE,
    COMMENT_FILE
)
from storage import ensure_file

from complainant_manager import complainant_menu
from complaint_manager import complaint_menu
from staff_manager import staff_menu
from comment_manager import comment_menu
from report_manager import report_menu


def initialize():
    for file_path in [
        COMPLAINANT_FILE,
        COMPLAINT_FILE,
        STAFF_FILE,
        COMMENT_FILE
    ]:
        ensure_file(file_path)


def main():
    initialize()

    while True:
        print("\n======================================")
        print("      COMPLAINT MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Complainant management")
        print("2. Complaint management")
        print("3. Staff management")
        print("4. Complaint updates and comments")
        print("5. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                complainant_menu()
            elif choice == "2":
                complaint_menu()
            elif choice == "3":
                staff_menu()
            elif choice == "4":
                comment_menu()
            elif choice == "5":
                report_menu()
            elif choice == "0":
                print("Thank you for using Complaint Management System.")
                break
            else:
                print("Invalid choice. Select an option from the menu.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Operation failed: {error}")
            print("Check the entered values and JSON data files.")


if __name__ == "__main__":
    main()
