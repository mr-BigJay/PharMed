# PharMed

PharMed is a pharmacy and medical supplies inventory management desktop app
built with PySide6, SQLAlchemy, and SQLite.

## Setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Bootstrap reference data in this order:

```bash
python3 services/seed_categories.py
python3 services/import_centers.py
python3 services/import_health_houses.py
python3 services/import_items.py
```

Create the first super admin without storing the password in source code:

```bash
PHARMED_ADMIN_PASSWORD="change-me" python3 services/create_admin.py
```

Run the app:

```bash
python3 main.py
```