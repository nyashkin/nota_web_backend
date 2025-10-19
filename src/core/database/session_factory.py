from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.core import config

_engine = create_async_engine(url=str(config.db.dsn))

_session_maker = async_sessionmaker(_engine, autoflush=True, expire_on_commit=False)


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return _session_maker
