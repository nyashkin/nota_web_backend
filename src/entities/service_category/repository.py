from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.service_category.exceptions.domain import (
    ServiceCategoryCreateException,
    ServiceCategoryNotFoundException,
    ServiceCategoryUknownException,
)
from src.entities.service_category.exceptions.http import (
    ServiceCategoryIdAndParentIdCannotBeEqualError,
)
from src.entities.service_category.models import ServiceCategoryOrm
from src.entities.service_category.schemas import (
    ServiceCategoryCreateShema,
    ServiceCategoryReadSchema,
    ServiceCategoryUpdateShema,
)


class ServiceCategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_category(
        self, create_category: ServiceCategoryCreateShema
    ) -> ServiceCategoryReadSchema:
        category_orm = ServiceCategoryOrm(**create_category.model_dump())
        self._session.add(category_orm)
        try:
            await self._session.flush()
            await self._session.refresh(category_orm)
            if category_orm.id == category_orm.parent_id:
                raise ServiceCategoryIdAndParentIdCannotBeEqualError
            await self._session.commit()
        except IntegrityError:
            raise ServiceCategoryCreateException
        except SQLAlchemyError as e:
            logger.error(e)
            raise ServiceCategoryUknownException
        return ServiceCategoryReadSchema.model_validate(category_orm)

    async def update_category(
        self, id: int, update_category: ServiceCategoryUpdateShema
    ) -> ServiceCategoryReadSchema:
        try:
            category_orm = await self._get_category_orm_by_id(id)
            for key, val in update_category.model_dump().items():
                category_orm.__setattr__(key, val)
            await self._session.flush()
            await self._session.refresh(category_orm)
            if category_orm.id == category_orm.parent_id:
                raise ServiceCategoryIdAndParentIdCannotBeEqualError
            await self._session.commit()
        except IntegrityError:
            raise ServiceCategoryCreateException
        except SQLAlchemyError as e:
            logger.error(e)
            raise ServiceCategoryUknownException
        return ServiceCategoryReadSchema.model_validate(category_orm)

    async def delete_category(self, id: int):
        stmt = delete(ServiceCategoryOrm).where(ServiceCategoryOrm.id == id)
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError as e:
            logger.error(e)
            raise ServiceCategoryUknownException

    async def get_category_by_id(self, id: int) -> ServiceCategoryReadSchema:
        category_orm: ServiceCategoryOrm | None = await self._get_category_orm_by_id(id)
        return ServiceCategoryReadSchema.model_validate(category_orm)

    async def _get_category_orm_by_id(self, id: int) -> ServiceCategoryOrm:
        query = select(ServiceCategoryOrm).where(ServiceCategoryOrm.id == id)
        category_orm: ServiceCategoryOrm | None = (
            await self._session.execute(query)
        ).scalar_one_or_none()
        if not category_orm:
            raise ServiceCategoryNotFoundException
        return category_orm

    async def get_all(self) -> list[ServiceCategoryReadSchema]:
        try:
            query = select(ServiceCategoryOrm)
            category_orms: list[ServiceCategoryOrm] = list(
                (await self._session.execute(query)).scalars().all()
            )
            category_reads = [
                ServiceCategoryReadSchema.model_validate(category_orm)
                for category_orm in category_orms
            ]
        except SQLAlchemyError as e:
            logger.error(e)
            raise ServiceCategoryUknownException
        return category_reads
