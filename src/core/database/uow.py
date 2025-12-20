from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.entities.customer_profiles.repository import CustomerProfileRepository
from src.entities.notary_profiles.repository import NotaryProfileRepository
from src.entities.service.repository import ServiceRepository
from src.entities.service_category.repository import ServiceCategoryRepository
from src.entities.user.repository import UserRepository


class UoW:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()

        self.users = UserRepository(self._session)
        self.customer_profiles = CustomerProfileRepository(self._session)
        self.notary_profiles = NotaryProfileRepository(self._session)
        self.service_categories = ServiceCategoryRepository(self._session)
        self.services = ServiceRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
        finally:
            await self._session.close()
