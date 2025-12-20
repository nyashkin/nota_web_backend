from src.core.schemas import BaseAppSchema
from src.entities.user.dto import UserCreateDTO, UserFullDTO, UserReadDTO, UserUpdateDTO


class UserUpdateSchema(
    UserUpdateDTO,
    BaseAppSchema,
):
    pass


class UserReadSchema(
    UserReadDTO,
    BaseAppSchema,
):
    pass


class UserCreateSchema(
    UserCreateDTO,
    BaseAppSchema,
):
    pass


class UserFullSchema(
    UserFullDTO,
    BaseAppSchema,
):
    pass
