from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import PositiveInt

from src.auth.dependencies import AdminRequiredDI, AuthRequiredDI, CurrentUserDI
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.schemas import UserReadSchema, UserUpdateSchema

user_router = APIRouter(prefix="/users", tags=["👥 Users"])


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
    return await user_service.update_user(user.id, update_user)


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
    return await user_service.change_username(current_user.id, new_username)


@user_router.get(
    path="/{user_id}",
    dependencies=[AuthRequiredDI],
    response_model=UserReadSchema,
)
async def get_user_by_id(
    user_service: UserServiceDI, user_id: Annotated[PositiveInt, Path()]
) -> UserReadSchema:
    return await user_service.get_user_by_id(user_id)


@user_router.put(
    path="/{user_id}",
    dependencies=[AdminRequiredDI],
    response_model=UserReadSchema,
)
async def update_username_by_id(
    user_service: UserServiceDI, user_id: Annotated[int, Path()], new_username: str
) -> UserReadSchema:
    return await user_service.change_username(user_id, new_username)
