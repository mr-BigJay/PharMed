from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class StockRequest(Base):
    __tablename__ = "stock_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    center_id: Mapped[int | None] = mapped_column(
        ForeignKey("centers.id"),
        nullable=True
    )

    health_house_id: Mapped[int | None] = mapped_column(
        ForeignKey("health_houses.id"),
        nullable=True
    )

    request_date: Mapped[date] = mapped_column(
        Date,
        default=date.today
    )

    quantity: Mapped[float] = mapped_column()

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )

    description: Mapped[str | None] = mapped_column(
        String(500)
    )
