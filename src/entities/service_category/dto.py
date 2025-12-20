from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.dto import BaseDTO


class ServiceCategoryUpdateDTO(BaseDTO):
    name: str = Field(min_length=5, max_length=32)
    parent_id: PositiveInt | None


class ServiceCategoryCreateDTO(ServiceCategoryUpdateDTO):
    pass


class ServiceCategoryReadDTO(ServiceCategoryUpdateDTO):
    id: int
    created_at: datetime
    updated_at: datetime
