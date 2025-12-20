from src.core.schemas import BaseAppSchema
from src.entities.notary_profiles.dto import (
    NotaryProfileCreateDTO,
    NotaryProfileReadDTO,
    NotaryProfileUpdateDTO,
)


class NotaryProfileCreateSchema(
    NotaryProfileCreateDTO,
    BaseAppSchema,
):
    pass


class NotaryProfileReadSchema(
    NotaryProfileReadDTO,
    BaseAppSchema,
):
    pass


class NotaryProfileUpdateSchema(
    NotaryProfileUpdateDTO,
    BaseAppSchema,
):
    pass
