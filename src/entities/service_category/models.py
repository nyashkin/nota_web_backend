from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin


class ServiceCategoryOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "service_categories"
    name: Mapped[str] = mapped_column(String(32), unique=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("service_categories.id", ondelete="CASCADE"),
        nullable=True,
    )


ServiceCategoryOrm.parent = relationship(
    "ServiceCategoryOrm",
    remote_side=[ServiceCategoryOrm.id],
    backref="subcategories",
    passive_deletes=True,
)
