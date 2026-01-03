from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Int64


class BookingOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "bookings"

    service_id: Mapped[Int64] = mapped_column(
        ForeignKey("services.id"),
        nullable=False,
    )

    notary_profile_id: Mapped[Int64] = mapped_column(
        ForeignKey("notary_profiles.id"),
        nullable=False,
    )

    customer_profile_id: Mapped[Int64] = mapped_column(
        ForeignKey("customer_profiles.id"),
        nullable=False,
    )

    commission_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )
    commission_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    service = relationship(
        "ServiceOrm",
        lazy="joined",
        uselist=False,
    )

    notary_profile = relationship(
        "NotaryProfileOrm",
        lazy="joined",
        uselist=False,
    )

    customer_profile = relationship(
        "CustomerProfileOrm",
        lazy="joined",
        uselist=False,
    )
