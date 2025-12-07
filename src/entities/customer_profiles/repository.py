from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.customer_profiles.dto import (
    CustomerProfileCreateDTO,
    CustomerProfileReadDTO,
    CustomerProfileUpdateDTO,
)
from src.entities.customer_profiles.exceptions.domain import (
    CustomerProfileIsNotUniqueException,
    CustomerProfileNotFoundException,
)
from src.entities.customer_profiles.models import CustomerProfileOrm


class CustomerProfileRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def create_customer_profile(
        self,
        user_id: int,
        customer_profile_dto: CustomerProfileCreateDTO,
    ) -> CustomerProfileReadDTO:
        try:
            customer_profile_orm = CustomerProfileOrm(
                user_id=user_id,
                **customer_profile_dto.model_dump(exclude_unset=True),
            )
            self._session.add(customer_profile_orm)
            await self._session.flush()
            return CustomerProfileReadDTO.model_validate(customer_profile_orm)
        except IntegrityError:
            raise CustomerProfileIsNotUniqueException
        except Exception as e:
            logger.error(e)
            raise e

    async def get_customer_profile_by_user_id(
        self,
        user_id: int,
    ) -> CustomerProfileReadDTO:
        query = select(CustomerProfileOrm).where(CustomerProfileOrm.user_id == user_id)
        customer_profile = (await self._session.execute(query)).scalar_one_or_none()
        if not customer_profile:
            raise CustomerProfileNotFoundException
        return CustomerProfileReadDTO.model_validate(customer_profile)

    async def get_customer_profile_by_id(
        self,
        id: int,
    ) -> CustomerProfileOrm | None:
        query = select(CustomerProfileOrm).where(CustomerProfileOrm.id == id)
        customer_profile = (await self._session.execute(query)).scalar_one_or_none()
        if not customer_profile:
            raise CustomerProfileNotFoundException
        return customer_profile

    async def update_customer_profile_by_id(
        self,
        profile_id: int,
        update_dto: CustomerProfileUpdateDTO,
    ) -> CustomerProfileOrm | None:
        update_values = update_dto.model_dump(exclude_unset=True)
        stmt = (
            update(CustomerProfileOrm)
            .where(CustomerProfileOrm.id == profile_id)
            .values(**update_values)
            .returning(CustomerProfileOrm)
        )
        customer_profile = (await self._session.execute(stmt)).scalar_one_or_none()
        if not customer_profile:
            raise CustomerProfileNotFoundException
        return customer_profile

    async def update_customer_profile_by_user_id(
        self,
        user_id: int,
        update_dto: CustomerProfileUpdateDTO,
    ) -> CustomerProfileOrm | None:
        update_values = update_dto.model_dump(exclude_unset=True)
        stmt = (
            update(CustomerProfileOrm)
            .where(CustomerProfileOrm.user_id == user_id)
            .values(**update_values)
            .returning(CustomerProfileOrm)
        )
        customer_profile = (await self._session.execute(stmt)).scalar_one_or_none()
        if not customer_profile:
            raise CustomerProfileNotFoundException
        return customer_profile

    async def delete_customer_profile_by_user_id(
        self,
        user_id: int,
    ) -> None:
        stmt = delete(CustomerProfileOrm).where(CustomerProfileOrm.user_id == user_id)
        await self._session.execute(stmt)
