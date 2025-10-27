from src.core.database import UoWDI
from src.entities.service_category.schemas import (
    ServiceCategoryCreateShema,
    ServiceCategoryReadSchema,
    ServiceCategoryUpdateShema,
)


class ServiceCategoryService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_category(
        self,
        create_category: ServiceCategoryCreateShema,
    ) -> ServiceCategoryReadSchema:
        return await self._uow.service_categories.create_category(create_category)

    async def update_category(
        self, category_id: int, update_category: ServiceCategoryUpdateShema
    ) -> ServiceCategoryReadSchema:
        return await self._uow.service_categories.update_category(
            category_id, update_category
        )

    async def get_by_id(
        self,
        category_id: int,
    ) -> ServiceCategoryReadSchema:
        return await self._uow.service_categories.get_category_by_id(category_id)

    async def get_all(self) -> list[ServiceCategoryReadSchema]:
        return await self._uow.service_categories.get_all()

    async def delete_category(self, category_id: int) -> None:
        await self._uow.service_categories.delete_category(category_id)
