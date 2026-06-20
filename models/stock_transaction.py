from datetime import date

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    transaction_type: Mapped[str] = mapped_column(
        String(10)
    )

    quantity: Mapped[float] = mapped_column()

    batch_number: Mapped[str | None] = mapped_column(
        String(100)
    )

    expiry_date: Mapped[str | None] = mapped_column(
        String(20)
    )
    description: Mapped[str | None] = mapped_column(
        String(500)
    )