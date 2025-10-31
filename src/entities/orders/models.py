from src.core.database.base_model import BaseOrm
from src.core.database.mixins import IdMixin, TimestampMixin


class Order(BaseOrm, IdMixin, TimestampMixin):
    pass
