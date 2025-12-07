from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core import config

_engine = create_async_engine(url=str(config.db.dsn))

_session_maker = async_sessionmaker(
    _engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return _session_maker
