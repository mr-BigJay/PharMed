from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Center(Base):
    __tablename__ = "centers"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(String(50), unique=True)

    name: Mapped[str] = mapped_column(String(200))

    is_active: Mapped[bool] = mapped_column(default=True)