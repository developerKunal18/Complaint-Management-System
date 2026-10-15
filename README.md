
# Complaint Management System

## Overview

A Python command-line application for recording complaints, assigning staff members, tracking complaint progress, adding updates, and generating management reports.

## Features

- Complainant registration
- Complaint submission with category and priority
- Unique complaint IDs
- Staff registration and assignment
- Complaint status tracking
- Resolution notes and closure
- Complaint comments and updates
- Complaint search by ID
- Category-wise complaint reports
- Staff workload reports
- JSON-based persistent storage

## Technologies

- Python 3.10+
- JSON
- Python standard library

## Installation

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open the terminal in the project folder.
4. Run the application:

   ```bash
   python main.py
   ```

No external packages are required.

## Project Structure

```text
day357_complaint_management/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── complainant_manager.py
├── complaint_manager.py
├── staff_manager.py
├── comment_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── complainants.json
    ├── complaints.json
    ├── staff.json
    └── comments.json
```

## How to Use

1. Register a complainant.
2. Register a staff member.
3. Submit a complaint using the complainant ID.
4. Assign the complaint to an active staff member.
5. Move the complaint to In Progress.
6. Add updates or comments.
7. Resolve the complaint and enter resolution notes.
8. Close the resolved complaint.
9. Review the dashboard and staff workload reports.

## Complaint Status Flow

Open → Assigned → In Progress → Resolved → Closed

A resolved complaint can be reopened for further work by moving it back to In Progress.

## Testing Checklist

- Register a complainant with a valid email and phone number.
- Submit a complaint with a valid category and priority.
- Assign the complaint to an active staff member.
- Test an invalid status transition.
- Add and view complaint comments.
- Resolve the complaint with resolution notes.
- Close the resolved complaint.
- Generate the dashboard and staff workload report.

## Data Storage

The application stores records in JSON files inside the `data` directory. Back up these files regularly.

## Limitations

- Local, single-user learning application.
- No authentication or role-based permissions.
- JSON storage is not suitable for concurrent multi-user access.
- Email and SMS notifications are not integrated.
- Complaint updates do not currently include file attachments.

## Future Improvements

- Build a graphical interface using Tkinter.
- Add complaint search by category and priority.
- Add CSV export.
- Add email notifications.
- Add login and staff permissions.
- Migrate storage to SQLite or MySQL.
- Add automated tests using `unittest`.
