from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class IdMixin:
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )
