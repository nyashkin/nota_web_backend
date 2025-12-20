from datetime import datetime

from pydantic import PositiveInt

from src.core.dto import BaseDTO
from src.entities.user.enums import UserRoleEnum


class UserUpdateDTO(BaseDTO):
    username: str


class UserReadDTO(UserUpdateDTO):
    id: PositiveInt
    role: UserRoleEnum
    created_at: datetime
    updated_at: datetime


class UserCreateDTO(UserUpdateDTO):
    role: UserRoleEnum
    password: str


class UserFullDTO(UserCreateDTO):
    id: int
