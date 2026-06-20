# PharMed

PharMed is a pharmacy and medical supplies inventory management desktop app
built with PySide6, SQLAlchemy, and SQLite.

## Current features

- Mobile/password login and user registration for centers and health houses
- Dashboard navigation for inventory, equipment, requests, users, and reports
- Item registration with category, form, unit, and minimum stock
- Per-unit opening stock and stock in/out transactions
- Stock validation that blocks outgoing transactions above available quantity
- Medical equipment inventory view
- Stock request registration and manager approval/rejection workflow
- Basic inventory reports and low-stock report
- Unit manager user list with activation/deactivation controls

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
