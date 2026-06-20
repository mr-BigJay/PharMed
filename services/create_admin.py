import bcrypt

import models.center
import models.health_house
from services.db_session import SessionLocal
from models.user import User

db = SessionLocal()

mobile = "09111111111"

exists = (
    db.query(User)
    .filter_by(mobile=mobile)
    .first()
)

if exists:
    print("Admin already exists")
    raise SystemExit

password = "603240@BigJayX"

password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

admin = User(
    first_name="BigJay",
    last_name="Admin",
    mobile=mobile,
    password_hash=password_hash,
    role="super_admin",
    is_manager=True,
    is_active=True
)

db.add(admin)
db.commit()

print("Super Admin Created Successfully")