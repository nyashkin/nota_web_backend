from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO
from src.entities.user.exceptions.domain import (
    UsernameAlredyExistsError,
    UserNotFoundError,
)
from src.entities.user.models import UserOrm


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_user(self, user_create: UserCreateDTO) -> UserReadDTO:
        user = UserOrm(**user_create.model_dump())
        self._session.add(user)
        try:
            await self._session.commit()
            await self._session.refresh(user)
        except IntegrityError:
            raise UsernameAlredyExistsError(user_create.username)
        return UserReadDTO.model_validate(user)

    async def get_user_by_id(self, id: int) -> UserReadDTO:
        user: UserOrm = await self._get_user_model_by_id(id)
        return UserReadDTO.model_validate(user)

    async def get_password_hash_by_username(self, username: str) -> str:
        user_orm = await self._get_user_model_by_username(username)
        return user_orm.password

    async def get_user_by_username(self, username: str) -> UserReadDTO:
        user_orm = await self._get_user_model_by_username(username)
        return UserReadDTO.model_validate(user_orm)

    async def change_username(self, id: int, username: str) -> UserReadDTO:
        user = await self._get_user_model_by_id(id)
        user.username = username
        try:
            await self._session.flush()
            await self._session.refresh(user)
            await self._session.commit()
            return UserReadDTO.model_validate(user)
        except IntegrityError:
            raise UsernameAlredyExistsError(username)

    async def update_user(
        self,
        id: int,
        update_user: UserUpdateDTO,
    ) -> UserReadDTO:
        stmt = update(UserOrm).where(UserOrm.id == id).values(update_user.model_dump())
        await self._session.execute(stmt)
        user_orm = await self._get_user_model_by_id(id)
        return UserReadDTO.model_validate(user_orm)

    async def _get_user_model_by_id(self, id: int) -> UserOrm:
        query = select(UserOrm).where(UserOrm.id == id)
        user_orm: UserOrm | None = (
            await self._session.execute(query)
        ).scalar_one_or_none()
        if not user_orm:
            raise UserNotFoundError(id)
        return user_orm

    async def _get_user_model_by_username(self, username: str) -> UserOrm:
        query = select(UserOrm).where(UserOrm.username == username)
        user_orm: UserOrm | None = (
            await self._session.execute(query)
        ).scalar_one_or_none()
        if not user_orm:
            raise UserNotFoundError
        return user_orm
