from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin


class CustomerProfileOrm(BaseOrm, TimestampMixin, IdMixin):
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
