from src.core.database.dependencies import UoWDI
from src.entities.service.dto import ServiceCreateDTO, ServiceReadDTO, ServiceUpdateDTO
from src.entities.service.exceptions.domain import (
    ServiceCategoryForServiceNotFoundError,
)


class ServiceService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_service(
        self,
        service_create: ServiceCreateDTO,
    ) -> ServiceReadDTO:
        service_category = await self._uow.service_categories.get_category_by_id(
            service_create.category_id,
        )
        if not service_category:
            raise ServiceCategoryForServiceNotFoundError(service_create.category_id)
        return await self._uow.services.create_service(service_create)

    async def get_service_by_id(
        self,
        service_id: int,
    ) -> ServiceReadDTO:
        return await self._uow.services.get_service_by_id(service_id)

    async def get_services_by_category_id(
        self,
        category_id: int,
    ) -> list[ServiceReadDTO]:
        return await self._uow.services.get_services_by_category_id(category_id)

    async def get_all_service(self) -> list[ServiceReadDTO]:
        return await self._uow.services.get_all()

    async def update_service(
        self,
        service_id: int,
        service_update: ServiceUpdateDTO,
    ) -> ServiceReadDTO:
        return await self._uow.services.update_service(
            service_id,
            service_update,
        )

    async def delete_service(
        self,
        service_id: int,
    ) -> None:
        return await self._uow.services.delete_service(service_id)
