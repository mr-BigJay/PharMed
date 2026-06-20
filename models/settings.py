from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    network_name: Mapped[str] = mapped_column(
        String(255)
    )

    version: Mapped[str] = mapped_column(
        String(20)
    )