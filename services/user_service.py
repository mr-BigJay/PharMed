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


def list_unit_users(
    current_user
):
    db = SessionLocal()

    try:
        query = db.query(User)
        query = _apply_user_scope(
            query,
            current_user
        )

        rows = []
        for user in query.order_by(User.last_name, User.first_name).all():
            rows.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "mobile": user.mobile,
                "role": user.role,
                "is_manager": user.is_manager,
                "is_active": user.is_active,
                "center_id": user.center_id,
                "health_house_id": user.health_house_id,
            })

        return rows

    finally:
        db.close()


def set_user_active(
    current_user,
    user_id,
    is_active
):
    db = SessionLocal()

    try:
        if not current_user or not current_user.is_manager:
            return (
                False,
                "فقط مدیر واحد اجازه مدیریت کاربران را دارد"
            )

        if current_user.id == user_id and not is_active:
            return (
                False,
                "امکان غیرفعال کردن حساب خودتان وجود ندارد"
            )

        query = db.query(User).filter(
            User.id == user_id
        )
        query = _apply_user_scope(
            query,
            current_user
        )

        user = query.first()

        if not user:
            return (
                False,
                "کاربر مورد نظر پیدا نشد"
            )

        user.is_active = is_active
        db.commit()

        return (
            True,
            "وضعیت کاربر به‌روزرسانی شد"
        )

    except Exception as e:
        db.rollback()
        return (
            False,
            f"خطا در به‌روزرسانی کاربر: {str(e)}"
        )

    finally:
        db.close()


def _apply_user_scope(
    query,
    current_user
):
    if current_user and current_user.health_house_id:
        return query.filter(
            User.health_house_id == current_user.health_house_id
        )

    if current_user and current_user.center_id:
        return query.filter(
            User.center_id == current_user.center_id,
            User.health_house_id.is_(None)
        )

    return query
