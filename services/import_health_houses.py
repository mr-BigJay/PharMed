import pandas as pd

from services.db_session import SessionLocal
from models.center import Center
from models.health_house import HealthHouse

db = SessionLocal()

df = pd.read_excel(
    "data/health_houses.xlsx",
    header=None
)

added = 0

for _, row in df.iterrows():

    center_name = str(row[0]).strip()
    house_name = str(row[1]).strip()

    center = (
        db.query(Center)
        .filter_by(name=center_name)
        .first()
    )

    if not center:
        print(f"Center not found: {center_name}")
        continue

    exists = (
        db.query(HealthHouse)
        .filter_by(
            center_id=center.id,
            name=house_name
        )
        .first()
    )

    if exists:
        continue

    health_house = HealthHouse(
        center_id=center.id,
        code=f"H{added+1:03}",
        name=house_name,
        is_active=True
    )

    db.add(health_house)
    added += 1

db.commit()

print(f"{added} health houses imported successfully.")