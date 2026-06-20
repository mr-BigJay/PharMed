import pandas as pd

from services.db_session import SessionLocal
from models.center import Center

db = SessionLocal()

df = pd.read_excel(
    "data/centers.xlsx",
    header=None
)

added = 0

for _, row in df.iterrows():

    center_name = str(row[0]).strip()

    if not center_name:
        continue

    exists = (
        db.query(Center)
        .filter_by(name=center_name)
        .first()
    )

    if exists:
        continue

    center = Center(
        code=f"C{added+1:03}",
        name=center_name,
        is_active=True
    )

    db.add(center)
    added += 1

db.commit()

print(f"{added} centers imported successfully.")