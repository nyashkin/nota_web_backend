from src.core.schemas import BaseAppSchema
from src.entities.customer_profiles.dto import (
    CustomerProfileCreateDTO,
    CustomerProfileReadDTO,
    CustomerProfileUpdateDTO,
)


class CustomerProfileCreateSchema(
    CustomerProfileCreateDTO,
    BaseAppSchema,
):
    pass


class CustomerProfileReadSchema(
    CustomerProfileReadDTO,
    BaseAppSchema,
):
    pass


class CustomerProfileUpdateSchema(
    CustomerProfileUpdateDTO,
    BaseAppSchema,
):
    pass
