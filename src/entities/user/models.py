from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin
from src.core.database.types import Str32, Str256
from src.entities.user.enums import UserRoleEnum


class UserOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[Str32] = mapped_column(
        unique=True,
        nullable=False,
    )
    password: Mapped[Str256] = mapped_column(nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(
        String(16),
        nullable=False,
    )

    customer_profile = relationship(
        "CustomerProfileOrm",
        uselist=False,
        back_populates="user",
    )
