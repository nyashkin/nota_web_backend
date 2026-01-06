from src.core.database.dependencies import UoWDI
from src.entities.notary_profiles.dto import (
    NotaryProfileCreateDTO,
    NotaryProfileReadDTO,
    NotaryProfileUpdateDTO,
)
from src.entities.notary_profiles.exceptions.domain import (
    NotaryProfileNotFoundError,
)


class NotaryProfileService:
    def __init__(
        self,
        uow: UoWDI,
    ):
        self._uow = uow

    async def get_notary_profile_by_user_id(
        self,
        user_id: int,
    ) -> NotaryProfileReadDTO:
        notary_profile = await self._uow.notary_profiles.get_notary_profile_by_user_id(
            user_id
        )
        return notary_profile

    async def create_notary_profile(
        self,
        user_id: int,
        notary_profile: NotaryProfileCreateDTO,
    ) -> NotaryProfileReadDTO:
        notary_profile = await self._uow.notary_profiles.create_notary_profile(
            user_id,
            notary_profile,
        )
        return notary_profile

    async def update_notary_profile_by_user_id(
        self,
        user_id: int,
        notary_profile_update_dto: NotaryProfileUpdateDTO,
    ) -> NotaryProfileReadDTO:
        notary_profile = (
            await self._uow.notary_profiles.update_notary_profile_by_user_id(
                user_id,
                notary_profile_update_dto,
            )
        )
        if not notary_profile:
            raise NotaryProfileNotFoundError

        return NotaryProfileReadDTO.model_validate(notary_profile)

    async def get_all_notary_profiles(self) -> list[NotaryProfileReadDTO]:
        notary_profiles = await self._uow.notary_profiles.get_all_notary_profiles()
        return notary_profiles
