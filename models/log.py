from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    action: Mapped[str] = mapped_column(
        String(255)
    )

    details: Mapped[str | None] = mapped_column(
        String(1000)
    )