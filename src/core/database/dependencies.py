from fastapi import Depends
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.core.database.session_factory import get_session_maker
from src.core.database.uow import UoW

SessionMakerDI = Annotated[async_sessionmaker[AsyncSession], Depends(get_session_maker)]


async def get_uow(session_maker: SessionMakerDI) -> AsyncGenerator[UoW]:
    async with UoW(session_maker) as uow:
        yield uow


UoWDI = Annotated[UoW, Depends(get_uow)]
