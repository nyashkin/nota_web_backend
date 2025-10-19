from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.core.database.mixins import TimestampMixin, IdMixin
from src.core.database.base_model import BaseOrm
from src.entities.user.enums import UserRole


class UserOrm(BaseOrm, IdMixin, TimestampMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[UserRole] = mapped_column(String(16), nullable=False)
