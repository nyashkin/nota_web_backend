from src.core.schemas import BaseAppSchema
from src.entities.service.dto import ServiceCreateDTO, ServiceReadDTO, ServiceUpdateDTO


class ServiceUpdateSchema(
    ServiceUpdateDTO,
    BaseAppSchema,
):
    pass


class ServiceCreateSchema(
    ServiceCreateDTO,
    BaseAppSchema,
):
    pass


class ServiceReadSchema(
    ServiceReadDTO,
    BaseAppSchema,
):
    pass
