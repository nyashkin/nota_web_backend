from src.core.database.dependencies import UoWDI
from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO


class UserService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_user(
        self,
        create_user: UserCreateDTO,
    ) -> UserReadDTO:
        user_read_dto = await self._uow.users.create_user(create_user)
        return user_read_dto

    async def update_user(
        self,
        user_id: int,
        update_user: UserUpdateDTO,
    ) -> UserReadDTO:
        user_read_dto = await self._uow.users.update_user(
            user_id,
            update_user,
        )
        return user_read_dto

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserReadDTO:
        user_read_dto = await self._uow.users.get_user_by_id(user_id)
        return user_read_dto

    async def change_username(
        self,
        user_id: int,
        username: str,
    ) -> UserReadDTO:
        user_read_dto = await self._uow.users.change_username(
            user_id,
            username,
        )
        return user_read_dto
