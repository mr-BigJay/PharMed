# PharMed

PharMed is a pharmacy and medical supplies inventory management desktop app
built with PySide6, SQLAlchemy, and SQLite.

## Current features

- Mobile/password login and user registration for centers and health houses
- Dashboard navigation for inventory, equipment, requests, users, and reports
- Fully right-to-left inventory admin shell with a right sidebar and top bar
- Item registration with category, form, unit, and minimum stock
- Per-unit opening stock and stock in/out transactions
- Stock validation that blocks outgoing transactions above available quantity
- Medical equipment inventory view
- Stock request registration and manager approval/rejection workflow
- Basic inventory reports and low-stock report
- Unit manager user list with activation/deactivation controls
- Automatic first-run bootstrap for categories, centers, health houses,
  drugs, and medical equipment from the bundled `data/*.xlsx` files
- First registered user for each unit becomes that unit manager
- Health houses support 3 users total; treatment centers support 5 users total

PharMed is designed for a public health network supply flow, so it does not
model purchase orders, prices, or external suppliers.

## Setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Reference data is imported automatically on app startup from:

- `data/centers.xlsx`
- `data/health_houses.xlsx`
- `data/inventory_items.xlsx`

The bootstrap is idempotent, so restarting the app does not create duplicate
centers, health houses, drugs, or medical equipment.

Create the first super admin without storing the password in source code:

```bash
PHARMED_ADMIN_PASSWORD="change-me" python3 services/create_admin.py
```

Run the app:

```bash
python3 main.py
```

When building an installer with PyInstaller, bundle both resource folders:

```bash
pyinstaller --add-data "assets:assets" --add-data "data:data" main.py
```
