import bcrypt

from services.db_session import SessionLocal

from models.user import User


MAX_HEALTH_HOUSE_USERS = 3
MAX_CENTER_USERS = 5


def create_user(
    first_name,
    last_name,
    mobile,
    password,
    role,
    center_id,
    health_house_id=None,
    created_by=None,
    require_manager=False
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

        users_count = _count_unit_users(
            db,
            center_id,
            health_house_id
        )
        max_users = get_max_users_for_unit(
            health_house_id
        )
        is_manager = users_count == 0

        if require_manager and not is_manager:
            if not created_by or not created_by.is_manager:
                return (
                    False,
                    "پس از ثبت مدیر واحد، کاربران بعدی باید توسط مدیر همان واحد ایجاد شوند"
                )

            if not _same_unit(
                created_by,
                center_id,
                health_house_id
            ):
                return (
                    False,
                    "مدیر فقط می‌تواند برای واحد خودش کاربر ایجاد کند"
                )

        if users_count >= max_users:
            return (
                False,
                f"ظرفیت ثبت کاربر برای این واحد تکمیل شده است "
                f"({max_users} نفر)"
            )

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
            is_active=True,
            created_by=(
                created_by.id
                if created_by
                else None
            )
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


def create_unit_user(
    current_user,
    first_name,
    last_name,
    mobile,
    password
):
    if not current_user or not current_user.is_manager:
        return (
            False,
            "فقط مدیر واحد اجازه ایجاد کاربر جدید را دارد"
        )

    role = (
        "بهورز"
        if current_user.health_house_id
        else "پرستار"
    )

    return create_user(
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        password=password,
        role=role,
        center_id=current_user.center_id,
        health_house_id=current_user.health_house_id,
        created_by=current_user,
        require_manager=True
    )


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


def get_user_capacity(
    current_user
):
    db = SessionLocal()

    try:
        if not current_user:
            return {
                "registered": 0,
                "max_users": 0,
                "remaining": 0,
            }

        registered = _count_unit_users(
            db,
            current_user.center_id,
            current_user.health_house_id
        )
        max_users = get_max_users_for_unit(
            current_user.health_house_id
        )

        return {
            "registered": registered,
            "max_users": max_users,
            "remaining": max(
                max_users - registered,
                0
            ),
        }

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


def get_max_users_for_unit(
    health_house_id
):
    if health_house_id is not None:
        return MAX_HEALTH_HOUSE_USERS

    return MAX_CENTER_USERS


def _count_unit_users(
    db,
    center_id,
    health_house_id
):
    if health_house_id is not None:
        return (
            db.query(User)
            .filter(
                User.health_house_id == health_house_id
            )
            .count()
        )

    return (
        db.query(User)
        .filter(
            User.center_id == center_id,
            User.health_house_id.is_(None)
        )
        .count()
    )


def _same_unit(
    user,
    center_id,
    health_house_id
):
    if health_house_id is not None:
        return user.health_house_id == health_house_id

    return (
        user.center_id == center_id
        and user.health_house_id is None
    )
