from datetime import datetime
from decimal import Decimal

from pydantic import Field

from src.core.schemas import BaseAppSchema
from src.entities.service_category.schemas import ServiceCategoryReadSchema


class ServiceUpdateSchema(BaseAppSchema):
    title: str = Field(min_length=8, max_length=128)
    description: str = Field(min_length=8, max_length=256)
    price: Decimal
    category_id: int
    category: ServiceCategoryReadSchema | None


class ServiceCreateSchema(ServiceUpdateSchema):
    pass


class ServiceReadSchema(ServiceUpdateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
