import pandas as pd

from db import init_db
from services.db_session import SessionLocal
from models.center import Center
from models.health_house import HealthHouse


def next_health_house_code(db, start_number):
    number = start_number

    while True:
        code = f"H{number:03}"
        exists = (
            db.query(HealthHouse)
            .filter_by(code=code)
            .first()
        )

        if not exists:
            return code, number + 1

        number += 1


def main():
    init_db()
    db = SessionLocal()

    try:
        df = pd.read_excel(
            "data/health_houses.xlsx",
            header=None
        )

        added = 0
        next_number = db.query(HealthHouse).count() + 1

        for _, row in df.iterrows():

            if pd.isna(row[0]) or pd.isna(row[1]):
                continue

            center_name = str(row[0]).strip()
            house_name = str(row[1]).strip()

            if not center_name or not house_name:
                continue

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

            house_code, next_number = next_health_house_code(
                db,
                next_number
            )

            health_house = HealthHouse(
                center_id=center.id,
                code=house_code,
                name=house_name,
                is_active=True
            )

            db.add(health_house)
            added += 1

        db.commit()

        print(f"{added} health houses imported successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()