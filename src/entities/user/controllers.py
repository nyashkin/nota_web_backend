from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import PositiveInt

from src.auth.dependencies import AdminRoleRequiredDI, AuthRequiredDI, CurrentUserDI
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.dto import UserUpdateDTO
from src.entities.user.exception_handler import UserExceptionHandlerRoute
from src.entities.user.schemas import UserReadSchema, UserUpdateSchema

user_router = APIRouter(
    prefix="/users", tags=["👥 Users"], route_class=UserExceptionHandlerRoute,
)


@user_router.get(
    "/me",
    tags=["👤 me"],
    response_model=UserReadSchema,
)
def get_self(user: CurrentUserDI) -> UserReadSchema:
    return user


@user_router.patch(
    "/me",
    tags=["👤 me"],
    response_model=UserReadSchema,
)
async def update_self(
    user_service: UserServiceDI,
    user: CurrentUserDI,
    update_user: UserUpdateSchema,
) -> UserReadSchema:
    user_update_dto = UserUpdateDTO.model_validate(update_user)
    user_dto = await user_service.update_user(
        user.id,
        user_update_dto,
    )
    return UserReadSchema.model_validate(user_dto)


@user_router.put(
    path="/me",
    tags=["👤 me"],
    response_model=UserReadSchema,
)
async def update_self_username(
    user_service: UserServiceDI,
    current_user: CurrentUserDI,
    new_username: str,
) -> UserReadSchema:
    user_dto = await user_service.change_username(current_user.id, new_username)
    return UserReadSchema.model_validate(user_dto)


@user_router.get(
    path="/{user_id}",
    dependencies=[AuthRequiredDI],
    response_model=UserReadSchema,
)
async def get_user_by_id(
    user_service: UserServiceDI, user_id: Annotated[PositiveInt, Path()],
) -> UserReadSchema:
    user_dto = await user_service.get_user_by_id(user_id)
    return UserReadSchema.model_validate(user_dto)


@user_router.put(
    path="/{user_id}",
    dependencies=[AdminRoleRequiredDI],
    response_model=UserReadSchema,
)
async def update_username_by_id(
    user_service: UserServiceDI, user_id: Annotated[int, Path()], new_username: str,
) -> UserReadSchema:
    user_dto = await user_service.change_username(user_id, new_username)
    return UserReadSchema.model_validate(user_dto)
