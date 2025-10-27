from src.core.database import UoWDI
from src.entities.service.schemas import (
    ServiceCreateSchema,
    ServiceReadSchema,
    ServiceUpdateSchema,
)


class ServiceService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_service(
        self,
        service_create: ServiceCreateSchema,
    ) -> ServiceReadSchema:
        return await self._uow.services.create_service(service_create)

    async def get_service_by_id(self, service_id: int) -> ServiceReadSchema:
        return await self._uow.services.get_service_by_id(service_id)

    async def get_all_service(self) -> list[ServiceReadSchema]:
        return await self._uow.services.get_all()

    async def update_service(
        self, service_id: int, service_update: ServiceUpdateSchema
    ) -> ServiceReadSchema:
        return await self._uow.services.update_service(
            service_id,
            service_update,
        )

    async def delete_service(self, service_id: int) -> None:
        return await self._uow.services.delete_service(service_id)
