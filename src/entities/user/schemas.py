from pydantic import PositiveInt
from src.core.schemas import BaseAppSchema
from src.entities.user.enums import UserRole
from datetime import datetime


class UserBaseSchema(BaseAppSchema):
    username: str
    role: UserRole


class UserReadSchema(UserBaseSchema):
    id: PositiveInt
    created_at: datetime
    updated_at: datetime


class UserSchemaCreate(UserBaseSchema):
    password: str
