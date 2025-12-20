from src.core.database.dependencies import UoWDI
from src.entities.service.dto import ServiceReadDTO
from src.entities.service_category.dto import (
    ServiceCategoryCreateDTO,
    ServiceCategoryReadDTO,
    ServiceCategoryUpdateDTO,
)
from src.entities.service_category.exceptions.domain import (
    ParentServiceCategoryNotFoundError,
    ServiceCategoryNotFoundError,
)


class ServiceCategoryService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_category(
        self,
        create_category: ServiceCategoryCreateDTO,
    ) -> ServiceCategoryReadDTO:
        if parent_id := create_category.parent_id:
            parent_category = await self._uow.service_categories.get_category_by_id(
                parent_id,
            )
            if not parent_category:
                raise ParentServiceCategoryNotFoundError
        return await self._uow.service_categories.create_category(create_category)

    async def update_category(
        self,
        category_id: int,
        update_category: ServiceCategoryUpdateDTO,
    ) -> ServiceCategoryReadDTO:
        return await self._uow.service_categories.update_category(
            category_id,
            update_category,
        )

    async def get_by_id(
        self,
        category_id: int,
    ) -> ServiceCategoryReadDTO | None:
        return await self._uow.service_categories.get_category_by_id(category_id)

    async def get_all(self) -> list[ServiceCategoryReadDTO]:
        return await self._uow.service_categories.get_all()

    async def get_services_by_category_id(
        self,
        category_id: int,
    ) -> list[ServiceReadDTO]:
        category = await self._uow.service_categories.get_category_by_id(category_id)
        if not category:
            raise ServiceCategoryNotFoundError
        return await self._uow.services.get_services_by_category_id(category_id)

    async def delete_category(self, category_id: int) -> None:
        category_to_delete = await self._uow.service_categories.get_category_by_id(
            category_id,
        )
        if not category_to_delete:
            raise ServiceCategoryNotFoundError
        await self._uow.service_categories.delete_category(category_to_delete.id)
