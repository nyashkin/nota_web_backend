from fastapi import APIRouter

from src.auth.dependencies import CurrentUserDI, NotaryRoleRequiredDI
from src.entities.notary_profiles.dependencies import (
    NotaryProfileRequiredDI,
    NotaryProfileServiceDI,
)
from src.entities.notary_profiles.exception_api_route import (
    NotaryProfileExceptionApiRoute,
)
from src.entities.notary_profiles.schemas import (
    NotaryProfileCreateSchema,
    NotaryProfileReadSchema,
    NotaryProfileUpdateSchema,
)

notary_profiles_router = APIRouter(
    prefix="/notaries",
    tags=["Notary profiles"],
    route_class=NotaryProfileExceptionApiRoute,
)


@notary_profiles_router.get(
    "/me",
    dependencies=[NotaryProfileRequiredDI],
    response_model=NotaryProfileReadSchema,
)
async def get_me_notary_profile(
    notary_profile_service: NotaryProfileServiceDI,
    current_user: CurrentUserDI,
) -> NotaryProfileReadSchema:
    notary_profile_dto = await notary_profile_service.get_notary_profile_by_user_id(
        current_user.id
    )
    return NotaryProfileReadSchema.model_validate(notary_profile_dto)


@notary_profiles_router.post(
    "/me",
    dependencies=[NotaryRoleRequiredDI],
    response_model=NotaryProfileReadSchema,
)
async def create_me_notary_profile(
    notary_profile_service: NotaryProfileServiceDI,
    current_user: CurrentUserDI,
    notary_profile_create: NotaryProfileCreateSchema,
) -> NotaryProfileReadSchema:
    notary_profile_dto = await notary_profile_service.create_notary_profile(
        user_id=current_user.id,
        notary_profile=notary_profile_create,
    )
    return NotaryProfileReadSchema.model_validate(notary_profile_dto)


@notary_profiles_router.put(
    "/me",
    dependencies=[NotaryProfileRequiredDI],
    response_model=NotaryProfileReadSchema,
)
async def update_me_notary_profile(
    notary_profile_service: NotaryProfileServiceDI,
    current_user: CurrentUserDI,
    notary_profile_update_schema: NotaryProfileUpdateSchema,
) -> NotaryProfileReadSchema:
    notary_profile_dto = await notary_profile_service.update_notary_profile_by_user_id(
        current_user.id,
        notary_profile_update_schema,
    )
    return NotaryProfileReadSchema.model_validate(notary_profile_dto)
