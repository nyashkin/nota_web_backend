from src.core.database import UoWDI
from src.entities.user.schemas import UserCreateSchema, UserReadSchema


class UserService:
    def __init__(self, uow: UoWDI) -> None:
        self._uow = uow

    async def create_user(self, create_user: UserCreateSchema) -> UserReadSchema:
        return await self._uow.users.create_user(create_user)

    async def get_user_by_id(self, user_id: int) -> UserReadSchema:
        return await self._uow.users.get_user_by_id(user_id)

    async def change_username(self, user_id: int, username: str) -> UserReadSchema:
        user = await self._uow.users.change_username(user_id, username)
        return user
