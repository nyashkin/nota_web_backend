from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.service.exceptions.domain import UknownServiceException
from src.entities.service.models import ServiceOrm
from src.entities.service.schemas import ServiceCreateSchema, ServiceReadSchema


class ServiceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_service(
        self, create_service: ServiceCreateSchema
    ) -> ServiceReadSchema:
        service_orm = ServiceOrm(**create_service.model_dump())
        self._session.add(service_orm)
        await self._session.flush()
        await self._session.refresh(service_orm)
        await self._session.commit()
        return ServiceReadSchema.model_validate(service_orm)

    async def get_all(self) -> list[ServiceReadSchema]:
        query = select(ServiceOrm)
        try:
            all_services_orms: list[ServiceOrm] = list(
                (await self._session.execute(query)).scalars().all()
            )
        except SQLAlchemyError as e:
            logger.error(e)
            raise UknownServiceException

        all_services_read = [
            ServiceReadSchema.model_validate(service_orm)
            for service_orm in all_services_orms
        ]
        return all_services_read
