from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100)
    )

    last_name: Mapped[str] = mapped_column(
        String(100)
    )

    mobile: Mapped[str] = mapped_column(
        String(11),
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[str] = mapped_column(
        String(20)
    )

    center_id: Mapped[int | None] = mapped_column(
        ForeignKey("centers.id"),
        nullable=True
    )

    health_house_id: Mapped[int | None] = mapped_column(
        ForeignKey("health_houses.id"),
        nullable=True
    )

    is_manager: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    creator = relationship(
        "User",
        remote_side=[id],
        foreign_keys=[created_by]
    )

    @property
    def full_name(self):

        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )