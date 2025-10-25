from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import PositiveInt

from src.auth.dependencies import AdminRequiredDI, AuthRequiredDI, CurrentUserDI
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.exceptions.domain import (
    UserAlredyExistsException,
    UserNotFoundException,
    UserUknownException,
)
from src.entities.user.exceptions.http import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserUknownError,
)
from src.entities.user.schemas import UserReadSchema

user_router = APIRouter(prefix="/users", tags=["👥 Users"])


@user_router.get("/me")
def get_me(user: CurrentUserDI) -> UserReadSchema:
    return user


@user_router.get(
    path="/{user_id}", response_model=UserReadSchema, dependencies=[AuthRequiredDI]
)
async def get_user_by_id(
    user_service: UserServiceDI, user_id: Annotated[PositiveInt, Path()]
) -> UserReadSchema:
    try:
        user_read = await user_service.get_user_by_id(user_id)
        return user_read
    except UserNotFoundException as e:
        raise UserNotFoundError(e)
    except UserUknownException:
        raise UserUknownError


@user_router.put(
    path="/{user_id}", response_model=UserReadSchema, dependencies=[AdminRequiredDI]
)
async def update_username(
    user_service: UserServiceDI, user_id: Annotated[int, Path()], new_username: str
) -> UserReadSchema:
    try:
        user_read = await user_service.change_username(user_id, new_username)
        return user_read
    except UserAlredyExistsException as e:
        raise UserAlreadyExistsError(e)
    except UserUknownException as e:
        raise UserUknownError(e)
