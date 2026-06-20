import getpass
import os
import sys

import bcrypt

from db import init_db
from services.db_session import SessionLocal
from models.user import User


def read_admin_password():
    password = os.getenv(
        "PHARMED_ADMIN_PASSWORD"
    )

    if password:
        return password

    if sys.stdin.isatty():
        return getpass.getpass(
            "Super admin password: "
        )

    raise SystemExit(
        "Set PHARMED_ADMIN_PASSWORD before running this script."
    )


def main():
    init_db()
    db = SessionLocal()

    try:
        mobile = os.getenv(
            "PHARMED_ADMIN_MOBILE",
            "09111111111"
        )

        exists = (
            db.query(User)
            .filter_by(mobile=mobile)
            .first()
        )

        if exists:
            print("Admin already exists")
            raise SystemExit

        password = read_admin_password()

        if len(password) < 6:
            raise SystemExit(
                "Admin password must be at least 6 characters."
            )

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        admin = User(
            first_name=os.getenv(
                "PHARMED_ADMIN_FIRST_NAME",
                "Super"
            ),
            last_name=os.getenv(
                "PHARMED_ADMIN_LAST_NAME",
                "Admin"
            ),
            mobile=mobile,
            password_hash=password_hash,
            role="super_admin",
            is_manager=True,
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("Super Admin Created Successfully")

    finally:
        db.close()


if __name__ == "__main__":
    main()