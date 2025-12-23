from datetime import datetime
from decimal import Decimal

from pydantic import Field

from src.core.dto import BaseDTO


class ServiceUpdateDTO(BaseDTO):
    title: str = Field(min_length=8, max_length=128)
    description: str = Field(min_length=8, max_length=256)
    price: Decimal
    category_id: int


class ServiceCreateDTO(ServiceUpdateDTO):
    pass


class ServiceReadDTO(ServiceUpdateDTO):
    id: int
    created_at: datetime
    updated_at: datetime
    category_id: int
