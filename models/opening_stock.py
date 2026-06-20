from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class OpeningStock(Base):
    __tablename__ = "opening_stock"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id")
    )

    center_id: Mapped[int | None] = mapped_column(
        ForeignKey("centers.id"),
        nullable=True
    )

    health_house_id: Mapped[int | None] = mapped_column(
        ForeignKey("health_houses.id"),
        nullable=True
    )

    quantity: Mapped[float] = mapped_column()
