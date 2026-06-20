import bcrypt

from services.db_session import SessionLocal

from models.user import User


MAX_USERS_PER_UNIT = 3


def create_user(
    first_name,
    last_name,
    mobile,
    password,
    role,
    center_id,
    health_house_id=None
):

    db = SessionLocal()

    try:

        exists = (
            db.query(User)
            .filter(
                User.mobile == mobile
            )
            .first()
        )

        if exists:
            return (
                False,
                "این شماره موبایل قبلاً ثبت شده است"
            )

        # اگر کاربر مربوط به خانه بهداشت باشد
        if health_house_id is not None:

            users_count = (
                db.query(User)
                .filter(
                    User.health_house_id ==
                    health_house_id
                )
                .count()
            )

        # اگر کاربر مربوط به مرکز درمانی باشد
        else:

            users_count = (
                db.query(User)
                .filter(
                    User.center_id ==
                    center_id,
                    User.health_house_id.is_(None)
                )
                .count()
            )

        if users_count >= MAX_USERS_PER_UNIT:
            return (
                False,
                f"ظرفیت ثبت کاربر برای این واحد تکمیل شده است "
                f"({MAX_USERS_PER_UNIT} نفر)"
            )

        is_manager = users_count == 0

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            password_hash=password_hash,
            role=role,
            center_id=center_id,
            health_house_id=health_house_id,
            is_manager=is_manager,
            is_active=True
        )

        db.add(user)

        db.commit()

        if is_manager:

            return (
                True,
                "کاربر با موفقیت ثبت شد و به عنوان مدیر واحد شناخته شد"
            )

        return (
            True,
            "کاربر با موفقیت ثبت شد"
        )

    except Exception as e:

        db.rollback()

        return (
            False,
            f"خطا در ثبت کاربر: {str(e)}"
        )

    finally:

        db.close()