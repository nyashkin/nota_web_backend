from src.core.schemas import BaseAppSchema
from src.entities.service_category.dto import (
    ServiceCategoryCreateDTO,
    ServiceCategoryReadDTO,
    ServiceCategoryUpdateDTO,
)


class ServiceCategoryUpdateSchema(
    ServiceCategoryUpdateDTO,
    BaseAppSchema,
):
    pass


class ServiceCategoryCreateSchema(
    ServiceCategoryCreateDTO,
    BaseAppSchema,
):
    pass


class ServiceCategoryReadSchema(
    ServiceCategoryReadDTO,
    BaseAppSchema,
):
    pass
