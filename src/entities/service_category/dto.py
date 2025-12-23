from __future__ import annotations

from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.dto import BaseDTO
from src.entities.service.schemas import ServiceReadSchema


class ServiceCategoryUpdateDTO(BaseDTO):
    name: str = Field(min_length=5, max_length=32)
    parent_id: PositiveInt | None


class ServiceCategoryCreateDTO(ServiceCategoryUpdateDTO):
    pass


class ServiceCategoryReadDTO(ServiceCategoryUpdateDTO):
    id: int
    created_at: datetime
    updated_at: datetime
    services: list[ServiceReadSchema] | None = None
