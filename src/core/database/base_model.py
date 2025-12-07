from sqlalchemy import BigInteger, Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase

from src.core.database.types import (
    Int16,
    Int32,
    Int64,
    Str16,
    Str32,
    Str64,
    Str128,
    Str256,
)


class BaseOrm(DeclarativeBase):
    type_annotation_map = {
        Int16: SmallInteger,
        Int32: Integer,
        Int64: BigInteger,
        Str16: String(16),
        Str32: String(32),
        Str64: String(64),
        Str128: String(128),
        Str256: String(256),
    }
