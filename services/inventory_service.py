from datetime import date

from sqlalchemy import func

from services.db_session import SessionLocal

from models.category import Category
from models.item import Item
from models.opening_stock import OpeningStock
from models.stock_transaction import StockTransaction


TRANSACTION_IN = "in"
TRANSACTION_OUT = "out"

TRANSACTION_LABELS = {
    TRANSACTION_IN: "ورود",
    TRANSACTION_OUT: "خروج",
}


def get_categories():
    db = SessionLocal()

    try:
        return (
            db.query(Category)
            .order_by(Category.name)
            .all()
        )

    finally:
        db.close()


def add_item(
    category_id,
    item_name,
    item_form,
    unit,
    minimum_stock
):
    db = SessionLocal()

    try:
        item_name = item_name.strip()
        item_form = item_form.strip()
        unit = unit.strip() or "عدد"

        if not item_name:
            return (
                False,
                "نام کالا را وارد کنید"
            )

        if minimum_stock < 0:
            return (
                False,
                "حداقل موجودی نمی‌تواند منفی باشد"
            )

        exists = (
            db.query(Item)
            .filter(
                Item.category_id == category_id,
                Item.item_name == item_name,
                Item.item_form == item_form
            )
            .first()
        )

        if exists:
            return (
                False,
                "این کالا قبلاً ثبت شده است"
            )

        item = Item(
            category_id=category_id,
            item_name=item_name,
            item_form=item_form,
            unit=unit,
            minimum_stock=minimum_stock
        )

        db.add(item)
        db.commit()

        return (
            True,
            "کالا با موفقیت ثبت شد"
        )

    except Exception as exc:
        db.rollback()
        return (
            False,
            f"خطا در ثبت کالا: {exc}"
        )

    finally:
        db.close()


def list_inventory(
    user,
    search_text=""
):
    db = SessionLocal()

    try:
        query = (
            db.query(
                Item,
                Category.name.label("category_name")
            )
            .join(
                Category,
                Item.category_id == Category.id
            )
        )

        search_text = search_text.strip()
        if search_text:
            query = query.filter(
                Item.item_name.like(
                    f"%{search_text}%"
                )
            )

        rows = []
        for item, category_name in query.order_by(Item.item_name).all():
            opening_quantity = _sum_opening_stock(
                db,
                user,
                item.id
            )
            incoming_quantity = _sum_transactions(
                db,
                user,
                item.id,
                TRANSACTION_IN
            )
            outgoing_quantity = _sum_transactions(
                db,
                user,
                item.id,
                TRANSACTION_OUT
            )
            current_stock = (
                opening_quantity
                + incoming_quantity
                - outgoing_quantity
            )
            minimum_stock = item.minimum_stock or 0

            rows.append({
                "item_id": item.id,
                "item_name": item.item_name,
                "item_form": item.item_form or "",
                "category_name": category_name,
                "unit": item.unit or "",
                "minimum_stock": minimum_stock,
                "opening_quantity": opening_quantity,
                "incoming_quantity": incoming_quantity,
                "outgoing_quantity": outgoing_quantity,
                "current_stock": current_stock,
                "status": (
                    "کسری"
                    if current_stock < minimum_stock
                    else "موجود"
                ),
            })

        return rows

    finally:
        db.close()


def set_opening_stock(
    user,
    item_id,
    quantity
):
    db = SessionLocal()

    try:
        if quantity < 0:
            return (
                False,
                "موجودی اولیه نمی‌تواند منفی باشد"
            )

        if not _can_manage_inventory(
            user
        ):
            return (
                False,
                "واحد کاربر برای ثبت موجودی مشخص نیست"
            )

        center_id, health_house_id = _scope_values(
            user
        )
        opening_stock = (
            db.query(OpeningStock)
            .filter(
                OpeningStock.item_id == item_id,
                *_scope_identity_filters(
                    OpeningStock,
                    center_id,
                    health_house_id
                )
            )
            .first()
        )

        if opening_stock:
            opening_stock.quantity = quantity
        else:
            opening_stock = OpeningStock(
                item_id=item_id,
                center_id=center_id,
                health_house_id=health_house_id,
                quantity=quantity
            )
            db.add(opening_stock)

        db.commit()

        return (
            True,
            "موجودی اولیه ثبت شد"
        )

    except Exception as exc:
        db.rollback()
        return (
            False,
            f"خطا در ثبت موجودی اولیه: {exc}"
        )

    finally:
        db.close()


def create_transaction(
    user,
    item_id,
    transaction_type,
    quantity,
    batch_number="",
    expiry_date="",
    description=""
):
    db = SessionLocal()

    try:
        if transaction_type not in TRANSACTION_LABELS:
            return (
                False,
                "نوع تراکنش معتبر نیست"
            )

        if quantity <= 0:
            return (
                False,
                "تعداد باید بیشتر از صفر باشد"
            )

        if not _can_manage_inventory(
            user
        ):
            return (
                False,
                "واحد کاربر برای ثبت تراکنش مشخص نیست"
            )

        if transaction_type == TRANSACTION_OUT:
            current_stock = get_current_stock(
                user,
                item_id
            )
            if quantity > current_stock:
                return (
                    False,
                    "موجودی برای ثبت خروج کافی نیست"
                )

        center_id, health_house_id = _scope_values(
            user
        )

        transaction = StockTransaction(
            item_id=item_id,
            user_id=user.id,
            center_id=center_id,
            health_house_id=health_house_id,
            transaction_date=date.today(),
            transaction_type=transaction_type,
            quantity=quantity,
            batch_number=batch_number.strip(),
            expiry_date=expiry_date.strip(),
            description=description.strip()
        )

        db.add(transaction)
        db.commit()

        return (
            True,
            "تراکنش با موفقیت ثبت شد"
        )

    except Exception as exc:
        db.rollback()
        return (
            False,
            f"خطا در ثبت تراکنش: {exc}"
        )

    finally:
        db.close()


def get_current_stock(
    user,
    item_id
):
    db = SessionLocal()

    try:
        return (
            _sum_opening_stock(
                db,
                user,
                item_id
            )
            + _sum_transactions(
                db,
                user,
                item_id,
                TRANSACTION_IN
            )
            - _sum_transactions(
                db,
                user,
                item_id,
                TRANSACTION_OUT
            )
        )

    finally:
        db.close()


def list_recent_transactions(
    user,
    limit=50
):
    db = SessionLocal()

    try:
        query = (
            db.query(
                StockTransaction,
                Item.item_name,
                Item.item_form
            )
            .join(
                Item,
                StockTransaction.item_id == Item.id
            )
        )
        query = _apply_scope_filter(
            query,
            StockTransaction,
            user
        )

        rows = []
        for transaction, item_name, item_form in (
            query
            .order_by(StockTransaction.id.desc())
            .limit(limit)
            .all()
        ):
            rows.append({
                "id": transaction.id,
                "date": transaction.transaction_date,
                "item_name": item_name,
                "item_form": item_form or "",
                "transaction_type": transaction.transaction_type,
                "transaction_label": TRANSACTION_LABELS.get(
                    transaction.transaction_type,
                    transaction.transaction_type
                ),
                "quantity": transaction.quantity,
                "batch_number": transaction.batch_number or "",
                "expiry_date": transaction.expiry_date or "",
                "description": transaction.description or "",
            })

        return rows

    finally:
        db.close()


def get_report_data(
    user
):
    rows = list_inventory(
        user
    )
    low_stock_rows = [
        row
        for row in rows
        if row["current_stock"] < row["minimum_stock"]
    ]

    total_items = len(
        rows
    )
    total_stock = sum(
        row["current_stock"]
        for row in rows
    )

    return {
        "total_items": total_items,
        "total_stock": total_stock,
        "low_stock_count": len(low_stock_rows),
        "low_stock_rows": low_stock_rows,
    }


def _sum_opening_stock(
    db,
    user,
    item_id
):
    query = db.query(
        func.coalesce(
            func.sum(OpeningStock.quantity),
            0.0
        )
    ).filter(
        OpeningStock.item_id == item_id
    )
    query = _apply_scope_filter(
        query,
        OpeningStock,
        user
    )

    return float(
        query.scalar() or 0
    )


def _sum_transactions(
    db,
    user,
    item_id,
    transaction_type
):
    query = db.query(
        func.coalesce(
            func.sum(StockTransaction.quantity),
            0.0
        )
    ).filter(
        StockTransaction.item_id == item_id,
        StockTransaction.transaction_type == transaction_type
    )
    query = _apply_scope_filter(
        query,
        StockTransaction,
        user
    )

    return float(
        query.scalar() or 0
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


def _scope_identity_filters(
    model,
    center_id,
    health_house_id
):
    return [
        (
            model.center_id == center_id
            if center_id is not None
            else model.center_id.is_(None)
        ),
        (
            model.health_house_id == health_house_id
            if health_house_id is not None
            else model.health_house_id.is_(None)
        ),
    ]


def _can_manage_inventory(
    user
):
    return bool(
        user
        and (
            user.center_id
            or user.health_house_id
        )
    )
