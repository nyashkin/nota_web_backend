from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Int64, Str32


class CustomerProfileOrm(BaseOrm, TimestampMixin, IdMixin):
    __tablename__ = "customer_profiles"

    user_id: Mapped[Int64] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    phone_number: Mapped[Str32] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )
    first_name: Mapped[Str32] = mapped_column(
        nullable=False,
    )
    last_name: Mapped[Str32] = mapped_column(
        nullable=False,
    )

    user = relationship(
        "UserOrm",
        single_parent=True,
        uselist=False,
        back_populates="customer_profile",
    )
