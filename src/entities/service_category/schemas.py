from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.schemas import BaseAppSchema


class ServiceCategoryUpdateShema(BaseAppSchema):
    name: str = Field(min_length=5, max_length=32)
    parent_id: PositiveInt | None


class ServiceCategoryCreateShema(ServiceCategoryUpdateShema):
    pass


class ServiceCategoryReadSchema(ServiceCategoryCreateShema):
    id: int
    created_at: datetime
    updated_at: datetime
