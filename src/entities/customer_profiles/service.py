from src.core.database.dependencies import UoWDI
from src.entities.customer_profiles.dto import (
    CustomerProfileCreateDTO,
    CustomerProfileReadDTO,
    CustomerProfileUpdateDTO,
)
from src.entities.customer_profiles.exceptions.domain import (
    CustomerProfileNotFoundError,
)


class CustomerProfileService:
    def __init__(
        self,
        uow: UoWDI,
    ):
        self._uow = uow

    async def get_customer_profile_by_user_id(
        self,
        user_id: int,
    ) -> CustomerProfileReadDTO:
        customer_profile = (
            await self._uow.customer_profiles.get_customer_profile_by_user_id(user_id)
        )
        return customer_profile

    async def create_customer_profile(
        self,
        user_id: int,
        customer_profile: CustomerProfileCreateDTO,
    ) -> CustomerProfileReadDTO:
        customer_profile = await self._uow.customer_profiles.create_customer_profile(
            user_id,
            customer_profile,
        )
        return customer_profile

    async def update_customer_profile_by_user_id(
        self,
        user_id: int,
        customer_profile_update_dto: CustomerProfileUpdateDTO,
    ) -> CustomerProfileReadDTO:
        customer_profile = (
            await self._uow.customer_profiles.update_customer_profile_by_user_id(
                user_id,
                customer_profile_update_dto,
            )
        )
        if not customer_profile:
            raise CustomerProfileNotFoundError

        return CustomerProfileReadDTO.model_validate(customer_profile)
