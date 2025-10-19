from fastapi import Depends
from typing import Annotated, AsyncGenerator

from src.core.database.session_factory import get_session_maker
from src.core.database.uow import UoW


async def get_uow() -> AsyncGenerator[UoW]:
    async with UoW(get_session_maker()) as uow:
        yield uow


UoWDI = Annotated[UoW, Depends(get_uow)]
