from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Int64, Str32


class ServiceCategoryOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "service_categories"

    name: Mapped[Str32] = mapped_column(unique=True)
    parent_id: Mapped[Int64 | None] = mapped_column(
        ForeignKey(
            "service_categories.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    parent: Mapped[Optional[ServiceCategoryOrm]] = relationship(
        "ServiceCategoryOrm",
        back_populates="children",
        remote_side="ServiceCategoryOrm.id",
    )

    children: Mapped[list[ServiceCategoryOrm]] = relationship(
        "ServiceCategoryOrm",
        back_populates="parent",
        uselist=True,
        single_parent=True,
    )

    services = relationship(
        "ServiceOrm",
        back_populates="category",
        uselist=True,
    )
