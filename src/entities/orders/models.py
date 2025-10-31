from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin


class OrderOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "orders"
    customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    notary_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    service_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("services.id"))

    customer = relationship(
        "UserOrm",
        back_populates="orders_as_customer",
        foreign_keys=[customer_id],
        uselist=False,
    )
    notary = relationship(
        "UserOrm",
        back_populates="orders_as_notary",
        foreign_keys=[notary_id],
        uselist=False,
    )
    service = relationship(
        "ServiceOrm",
        foreign_keys=[service_id],
        uselist=False,
    )
