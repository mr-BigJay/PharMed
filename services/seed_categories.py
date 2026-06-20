from services.db_session import SessionLocal

from models.category import Category

db = SessionLocal()

if not db.query(Category).filter_by(name="دارو").first():
    db.add(Category(name="دارو"))

if not db.query(Category).filter_by(name="تجهیزات پزشکی").first():
    db.add(Category(name="تجهیزات پزشکی"))

db.commit()

print("Categories Seeded")