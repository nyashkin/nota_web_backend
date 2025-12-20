from typing import Annotated

from fastapi import Depends

from src.auth.dependencies import CurrentNotaryUser
from src.entities.notary_profiles.dto import NotaryProfileReadDTO
from src.entities.notary_profiles.exceptions.domain import (
    NotaryProfileNotFoundError,
)
from src.entities.notary_profiles.exceptions.http import (
    NotaryProfileNotFoundHTTPException,
)
from src.entities.notary_profiles.service import NotaryProfileService

NotaryProfileServiceDI = Annotated[NotaryProfileService, Depends()]


async def get_notary_profile(
    notary_profile_service: NotaryProfileServiceDI,
    current_notary_user: CurrentNotaryUser,
) -> NotaryProfileReadDTO:
    try:
        return await notary_profile_service.get_notary_profile_by_user_id(
            current_notary_user.id,
        )
    except NotaryProfileNotFoundError:
        raise NotaryProfileNotFoundHTTPException


NotaryProfileRequiredDI = Depends(get_notary_profile)
NotaryProfileDI = Annotated[NotaryProfileReadDTO, Depends(get_notary_profile)]
