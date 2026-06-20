from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    item_code: Mapped[str | None] = mapped_column(
        String(50)
    )

    item_name: Mapped[str] = mapped_column(
        String(255)
    )

    item_form: Mapped[str | None] = mapped_column(
        String(100)
    )

    unit: Mapped[str | None] = mapped_column(
        String(50)
    )

    minimum_stock: Mapped[int] = mapped_column(
        default=0
    )