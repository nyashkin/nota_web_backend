from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.notary_profiles.dto import (
    NotaryProfileCreateDTO,
    NotaryProfileReadDTO,
    NotaryProfileUpdateDTO,
)
from src.entities.notary_profiles.exceptions.domain import (
    NotaryProfileIsNotUniqueError,
    NotaryProfileNotFoundError,
)
from src.entities.notary_profiles.models import NotaryProfileOrm


class NotaryProfileRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def create_notary_profile(
        self,
        user_id: int,
        notary_profile_dto: NotaryProfileCreateDTO,
    ) -> NotaryProfileReadDTO:
        try:
            notary_profile_orm = NotaryProfileOrm(
                user_id=user_id,
                **notary_profile_dto.model_dump(exclude_unset=True),
            )
            self._session.add(notary_profile_orm)
            await self._session.flush()
            return NotaryProfileReadDTO.model_validate(notary_profile_orm)
        except IntegrityError:
            raise NotaryProfileIsNotUniqueError
        except Exception as e:
            logger.error(e)
            raise e

    async def get_notary_profile_by_user_id(
        self,
        user_id: int,
    ) -> NotaryProfileReadDTO:
        query = select(NotaryProfileOrm).where(NotaryProfileOrm.user_id == user_id)
        notary_profile = (await self._session.execute(query)).scalar_one_or_none()
        if not notary_profile:
            raise NotaryProfileNotFoundError
        return NotaryProfileReadDTO.model_validate(notary_profile)

    async def get_notary_profile_by_id(
        self,
        id: int,
    ) -> NotaryProfileOrm | None:
        query = select(NotaryProfileOrm).where(NotaryProfileOrm.id == id)
        notary_profile = (await self._session.execute(query)).scalar_one_or_none()
        if not notary_profile:
            raise NotaryProfileNotFoundError
        return notary_profile

    async def update_notary_profile_by_id(
        self,
        profile_id: int,
        update_dto: NotaryProfileUpdateDTO,
    ) -> NotaryProfileOrm | None:
        update_values = update_dto.model_dump(exclude_unset=True)
        stmt = (
            update(NotaryProfileOrm)
            .where(NotaryProfileOrm.id == profile_id)
            .values(**update_values)
            .returning(NotaryProfileOrm)
        )
        notary_profile = (await self._session.execute(stmt)).scalar_one_or_none()
        if not notary_profile:
            raise NotaryProfileNotFoundError
        return notary_profile

    async def update_notary_profile_by_user_id(
        self,
        user_id: int,
        update_dto: NotaryProfileUpdateDTO,
    ) -> NotaryProfileOrm | None:
        update_values = update_dto.model_dump(exclude_unset=True)
        stmt = (
            update(NotaryProfileOrm)
            .where(NotaryProfileOrm.user_id == user_id)
            .values(**update_values)
            .returning(NotaryProfileOrm)
        )
        notary_profile = (await self._session.execute(stmt)).scalar_one_or_none()
        if not notary_profile:
            raise NotaryProfileNotFoundError
        return notary_profile

    async def delete_notary_profile_by_user_id(
        self,
        user_id: int,
    ) -> None:
        stmt = delete(NotaryProfileOrm).where(NotaryProfileOrm.user_id == user_id)
        await self._session.execute(stmt)
