from db import init_db
from services.db_session import SessionLocal

from models.category import Category


def main():
    init_db()
    db = SessionLocal()

    try:
        if not db.query(Category).filter_by(name="دارو").first():
            db.add(Category(name="دارو"))

        if not db.query(Category).filter_by(name="تجهیزات پزشکی").first():
            db.add(Category(name="تجهیزات پزشکی"))

        db.commit()

        print("Categories Seeded")

    finally:
        db.close()


if __name__ == "__main__":
    main()