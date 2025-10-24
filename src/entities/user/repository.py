from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.entities.user.exceptions.domain import (
    UserAlredyExistsException,
    UserNotFoundException,
    UserUknownException,
)
from src.entities.user.schemas import UserSchemaCreate, UserReadSchema
from src.entities.user.models import UserOrm
from sqlalchemy.exc import IntegrityError


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_user(self, user_create: UserSchemaCreate) -> UserReadSchema:
        user = UserOrm(**user_create.model_dump())
        self._session.add(user)
        try:
            await self._session.commit()
            await self._session.refresh(user)
        except IntegrityError:
            raise UserAlredyExistsException(user_create.username)
        except Exception as e:
            raise UserUknownException(e)
        return UserReadSchema.model_validate(user)

    async def _get_user_model_by_id(self, id: int) -> UserOrm:
        query = select(UserOrm).where(UserOrm.id == id)
        try:
            user_orm: UserOrm | None = (
                await self._session.execute(query)
            ).scalar_one_or_none()
            if not user_orm:
                raise UserNotFoundException(id)
        except Exception as e:
            raise UserUknownException(e)
        return user_orm

    async def get_user_by_id(self, id: int) -> UserReadSchema:
        user: UserOrm = await self._get_user_model_by_id(id)
        return UserReadSchema.model_validate(user)

    async def change_username(self, id: int, username: str) -> UserReadSchema:
        user = await self._get_user_model_by_id(id)
        user.username = username
        try:
            await self._session.flush()
            await self._session.refresh(user)
            await self._session.commit()
        except IntegrityError:
            raise UserAlredyExistsException(username)
        except Exception as e:
            raise UserUknownException(e)
        return UserReadSchema.model_validate(user)
