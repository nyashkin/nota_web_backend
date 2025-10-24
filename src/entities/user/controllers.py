from typing import Annotated
from fastapi import APIRouter, Path
from starlette import status
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
from src.entities.user.schemas import UserSchemaCreate, UserReadSchema
from pydantic import PositiveInt

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_service: UserServiceDI, create_user: UserSchemaCreate
) -> UserReadSchema:
    try:
        user_read = await user_service.create_user(create_user)
        return user_read
    except UserAlredyExistsException as e:
        raise UserAlreadyExistsError(e)
    except UserUknownException as e:
        raise UserUknownError(e)


@router.get(path="/{user_id}", response_model=UserReadSchema)
async def get_user_by_id(
    user_service: UserServiceDI, user_id: Annotated[PositiveInt, Path()]
) -> UserReadSchema:
    try:
        user_read = await user_service.get_user_by_id(user_id)
        return user_read
    except UserNotFoundException as e:
        raise UserNotFoundError(e)


@router.put(path="/{user_id}", response_model=UserReadSchema)
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
