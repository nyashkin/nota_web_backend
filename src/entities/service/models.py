from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.entities.service_category.models import ServiceCategoryOrm


class ServiceOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "services"
    title: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("service_categories.id"),
        nullable=False,
    )

    category: Mapped[ServiceCategoryOrm] = relationship(
        "ServiceCategoryOrm", backref="services"
    )
