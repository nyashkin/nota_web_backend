from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Int64, Str128, Str256


class ServiceOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "services"
    title: Mapped[Str128] = mapped_column(unique=True)
    description: Mapped[Str256] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
    )
    category_id: Mapped[Int64] = mapped_column(
        ForeignKey("service_categories.id"),
        nullable=False,
    )

    category = relationship(
        "ServiceCategoryOrm",
        back_populates="services",
    )
