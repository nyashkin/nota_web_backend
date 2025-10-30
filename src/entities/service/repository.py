from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.entities.service.exceptions.domain import (
    NotUniqueServiceTitleException,
    ServiceNotFoundException,
)
from src.entities.service.models import ServiceOrm
from src.entities.service.schemas import (
    ServiceCreateSchema,
    ServiceReadSchema,
    ServiceUpdateSchema,
)


class ServiceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_service(
        self, create_service: ServiceCreateSchema
    ) -> ServiceReadSchema:
        try:
            service_orm = ServiceOrm(**create_service.model_dump())
            self._session.add(service_orm)
            await self._session.flush()
            await self._session.refresh(service_orm, attribute_names=["category"])
            await self._session.commit()
        except IntegrityError:
            raise NotUniqueServiceTitleException(create_service.title)
        return ServiceReadSchema.model_validate(service_orm)

    async def get_service_by_id(self, id: int) -> ServiceReadSchema:
        service_orm = await self._get_service_orm_by_id(id)
        return ServiceReadSchema.model_validate(service_orm)

    async def get_all(self) -> list[ServiceReadSchema]:
        query = select(ServiceOrm)
        all_services_orms: list[ServiceOrm] = list(
            (await self._session.execute(query)).scalars().all()
        )

        all_services_read = [
            ServiceReadSchema.model_validate(service_orm)
            for service_orm in all_services_orms
        ]
        return all_services_read

    async def update_service(
        self, id: int, update_service: ServiceUpdateSchema
    ) -> ServiceReadSchema:
        try:
            service_orm = await self._get_service_orm_by_id(id)
            for attr, val in update_service.model_dump(exclude_none=True).items():
                setattr(service_orm, attr, val)
            await self._session.flush()
            await self._session.refresh(service_orm, attribute_names=["category"])
            await self._session.commit()
        except IntegrityError:
            raise NotUniqueServiceTitleException(update_service.title)
        return ServiceReadSchema.model_validate(service_orm)

    async def delete_service(self, id: int) -> None:
        await self._session.execute(delete(ServiceOrm).where(ServiceOrm.id == id))

    async def _get_service_orm_by_id(self, id: int) -> ServiceOrm:
        query = (
            select(ServiceOrm)
            .where(ServiceOrm.id == id)
            .options(selectinload(ServiceOrm.category))
        )
        service_orm: ServiceOrm | None = (
            await self._session.execute(query)
        ).scalar_one_or_none()
        if not service_orm:
            raise ServiceNotFoundException(id)
        return service_orm
