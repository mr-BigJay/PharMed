import re
import bcrypt
from services.db_session import SessionLocal
from models.user import User

MOBILE_PATTERN = r"^09\d{9}$"
PERSIAN_PATTERN = r"^[آ-ی\s]+$"


def validate_mobile(mobile: str) -> bool:
    return bool(
        re.match(
            MOBILE_PATTERN,
            mobile
        )
    )


def validate_persian(text: str) -> bool:
    return bool(
        re.match(
            PERSIAN_PATTERN,
            text
        )
    )


def login_user(
    mobile: str,
    password: str
):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter_by(
                mobile=mobile,
                is_active=True
            )
            .first()
        )

        if not user:
            return None

        valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )

        if not valid:
            return None

        db.expunge(
            user
        )

        return user

    finally:
        db.close()