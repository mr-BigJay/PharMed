from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class HealthHouse(Base):
    __tablename__ = "health_houses"

    id: Mapped[int] = mapped_column(primary_key=True)

    center_id: Mapped[int] = mapped_column(
        ForeignKey("centers.id")
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(200)
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )