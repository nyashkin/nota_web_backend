from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Int64, Str32, Str128, Str256
from src.entities.user.models import UserOrm


class NotaryProfileOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "notary_profiles"

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
    license_number: Mapped[Str128] = mapped_column(
        unique=True,
        nullable=False,
    )
    inn: Mapped[Str128] = mapped_column(
        unique=True,
        nullable=False,
    )
    description: Mapped[Str256] = mapped_column(
        unique=True,
        nullable=False,
    )

    # RELATIONS
    user: Mapped[UserOrm] = relationship(
        "UserOrm",
        single_parent=True,
        uselist=False,
    )
