from datetime import date

from services.db_session import SessionLocal

from models.item import Item
from models.stock_request import StockRequest
from models.user import User


STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"

STATUS_LABELS = {
    STATUS_PENDING: "در انتظار بررسی",
    STATUS_APPROVED: "تأیید شده",
    STATUS_REJECTED: "رد شده",
}


def create_request(
    user,
    item_id,
    quantity,
    description=""
):
    db = SessionLocal()

    try:
        if not user:
            return (
                False,
                "برای ثبت درخواست ابتدا وارد شوید"
            )

        if not (
            user.center_id
            or user.health_house_id
        ):
            return (
                False,
                "واحد کاربر برای ثبت درخواست مشخص نیست"
            )

        if quantity <= 0:
            return (
                False,
                "تعداد باید بیشتر از صفر باشد"
            )

        center_id, health_house_id = _scope_values(
            user
        )

        request = StockRequest(
            item_id=item_id,
            user_id=user.id,
            center_id=center_id,
            health_house_id=health_house_id,
            request_date=date.today(),
            quantity=quantity,
            status=STATUS_PENDING,
            description=description.strip()
        )

        db.add(request)
        db.commit()

        return (
            True,
            "درخواست با موفقیت ثبت شد"
        )

    except Exception as exc:
        db.rollback()
        return (
            False,
            f"خطا در ثبت درخواست: {exc}"
        )

    finally:
        db.close()


def list_requests(
    user
):
    db = SessionLocal()

    try:
        query = (
            db.query(
                StockRequest,
                Item.item_name,
                Item.item_form,
                User.first_name,
                User.last_name,
            )
            .join(
                Item,
                StockRequest.item_id == Item.id
            )
            .join(
                User,
                StockRequest.user_id == User.id
            )
        )

        if user and user.is_manager:
            query = _apply_scope_filter(
                query,
                StockRequest,
                user
            )
        elif user:
            query = query.filter(
                StockRequest.user_id == user.id
            )
        else:
            return []

        rows = []
        for request, item_name, item_form, first_name, last_name in (
            query
            .order_by(StockRequest.id.desc())
            .all()
        ):
            rows.append({
                "id": request.id,
                "request_date": request.request_date,
                "item_name": item_name,
                "item_form": item_form or "",
                "requester": f"{first_name} {last_name}",
                "quantity": request.quantity,
                "status": request.status,
                "status_label": STATUS_LABELS.get(
                    request.status,
                    request.status
                ),
                "description": request.description or "",
            })

        return rows

    finally:
        db.close()


def update_request_status(
    current_user,
    request_id,
    status
):
    db = SessionLocal()

    try:
        if status not in STATUS_LABELS:
            return (
                False,
                "وضعیت درخواست معتبر نیست"
            )

        if not current_user or not current_user.is_manager:
            return (
                False,
                "فقط مدیر واحد اجازه تغییر وضعیت درخواست را دارد"
            )

        query = db.query(StockRequest).filter(
            StockRequest.id == request_id
        )
        query = _apply_scope_filter(
            query,
            StockRequest,
            current_user
        )

        request = query.first()
        if not request:
            return (
                False,
                "درخواست مورد نظر پیدا نشد"
            )

        request.status = status
        db.commit()

        return (
            True,
            "وضعیت درخواست به‌روزرسانی شد"
        )

    except Exception as exc:
        db.rollback()
        return (
            False,
            f"خطا در تغییر وضعیت درخواست: {exc}"
        )

    finally:
        db.close()


def _scope_values(
    user
):
    if user and user.health_house_id:
        return (
            user.center_id,
            user.health_house_id
        )

    if user and user.center_id:
        return (
            user.center_id,
            None
        )

    return (
        None,
        None
    )


def _apply_scope_filter(
    query,
    model,
    user
):
    if user and user.health_house_id:
        return query.filter(
            model.health_house_id == user.health_house_id
        )

    if user and user.center_id:
        return query.filter(
            model.center_id == user.center_id,
            model.health_house_id.is_(None)
        )

    return query
