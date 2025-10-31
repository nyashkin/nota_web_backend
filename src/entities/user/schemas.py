from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.schemas import BaseAppSchema
from src.entities.user.enums import UserRoleEnum


class UserUpdateSchema(BaseAppSchema):
    username: str
    phone_number: str = Field(min_length=5, max_length=20)
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)


class UserReadSchema(UserUpdateSchema):
    id: PositiveInt
    role: UserRoleEnum
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(UserUpdateSchema):
    role: UserRoleEnum
    password: str


class UserFullSchema(UserCreateSchema):
    id: int
