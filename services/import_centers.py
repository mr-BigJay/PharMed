import pandas as pd

from db import init_db
from services.db_session import SessionLocal
from models.center import Center


def next_center_code(db, start_number):
    number = start_number

    while True:
        code = f"C{number:03}"
        exists = (
            db.query(Center)
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
            "data/centers.xlsx",
            header=None
        )

        added = 0
        next_number = db.query(Center).count() + 1

        for _, row in df.iterrows():

            if pd.isna(row[0]):
                continue

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

            center_code, next_number = next_center_code(
                db,
                next_number
            )

            center = Center(
                code=center_code,
                name=center_name,
                is_active=True
            )

            db.add(center)
            added += 1

        db.commit()

        print(f"{added} centers imported successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()