from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

COMPLAINANT_FILE = DATA_DIR / "complainants.json"
COMPLAINT_FILE = DATA_DIR / "complaints.json"
STAFF_FILE = DATA_DIR / "staff.json"
COMMENT_FILE = DATA_DIR / "comments.json"

COMPLAINT_CATEGORIES = [
    "Technical",
    "Billing",
    "Service",
    "Product",
    "Infrastructure",
    "Other"
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]

STATUSES = [
    "Open",
    "Assigned",
    "In Progress",
    "Resolved",
    "Closed"
]
