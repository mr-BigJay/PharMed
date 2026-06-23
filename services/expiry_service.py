from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from models.item import Item
from models.stock_transaction import StockTransaction
from services.inventory_service import _apply_scope_filter

NEAR_EXPIRY_DAYS = 30


def _parse_expiry_date(value: str | None) -> date | None:
    if not value:
        return None

    cleaned = value.strip()

    try:
        return date.fromisoformat(cleaned)
    except ValueError:
        pass

    for fmt in ("%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue

    return None


def get_expiring_medicines(
    db: Session,
    user=None
) -> list[dict]:
    today = date.today()
    near_expiry_limit = today + timedelta(days=NEAR_EXPIRY_DAYS)

    query = (
        db.query(StockTransaction, Item)
        .join(Item, Item.id == StockTransaction.item_id)
        .filter(
            StockTransaction.expiry_date.isnot(None),
            StockTransaction.transaction_type == "in",
        )
    )
    query = _apply_scope_filter(
        query,
        StockTransaction,
        user
    )
    rows = query.all()

    seen = set()
    results = []

    for transaction, item in rows:
        expiry = _parse_expiry_date(transaction.expiry_date)
        if not expiry:
            continue

        key = (
            item.id,
            transaction.batch_number,
            expiry.isoformat()
        )
        if key in seen:
            continue
        seen.add(key)

        if expiry <= near_expiry_limit:
            if expiry < today:
                status_label = "منقضی شده"
            else:
                status_label = "نزدیک به انقضا"

            results.append(
                {
                    "item_name": item.item_name,
                    "batch_number": transaction.batch_number or "-",
                    "expiry_date": expiry.strftime("%Y/%m/%d"),
                    "status_label": status_label,
                }
            )

    results.sort(
        key=lambda row: row["expiry_date"]
    )

    return results


def get_expiry_alert_count(
    db: Session,
    user=None
) -> int:
    return len(
        get_expiring_medicines(
            db,
            user
        )
    )
