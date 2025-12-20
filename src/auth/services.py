from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from loguru import logger

from src.auth.enums import TokenType
from src.auth.exceptions.domain import (
    InvalidJwtTokenError,
    JwtTokenExpiredError,
    PasswordOrUsernameInvalidError,
)
from src.auth.schemas import AuthTokenRead, TokenPayloadSchema, TokenRead
from src.auth.utils import check_password, hash_password
from src.core import config
from src.core.database.dependencies import UoWDI
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.dto import UserReadDTO
from src.entities.user.schemas import UserCreateDTO


class CryptoService:
    public_key: str = config.auth.public_key
    private_key: str = config.auth.private_key
    access_token_expire_hours = config.auth.access_token_expire_hours
    refresh_token_expire_days = config.auth.refresh_token_expire_days
    alg = config.auth.algorithm

    @classmethod
    def encode_refresh_token(cls, user: UserReadDTO) -> str:
        datetime_now = datetime.now(timezone.utc)
        now_unix = int(datetime_now.timestamp())

        refresh_datetime_exp = datetime_now + timedelta(
            days=cls.refresh_token_expire_days,
        )

        exp_refresh_unix: int = int(refresh_datetime_exp.timestamp())

        refresh_payload = TokenPayloadSchema(
            sub=str(user.id),
            jti=str(uuid4()),
            iat=now_unix,
            exp=exp_refresh_unix,
            nbf=now_unix,
            type=TokenType.REFRESH,
        )

        return jwt.encode(
            payload=refresh_payload.model_dump(),
            key=cls.private_key,
            algorithm=cls.alg,
        )

    @classmethod
    def encode_access_token(cls, user: UserReadDTO) -> str:
        datetime_now = datetime.now(timezone.utc)
        access_datetime_exp = datetime_now + timedelta(
            hours=cls.access_token_expire_hours,
        )

        now_unix: int = int(datetime_now.timestamp())
        exp_access_unix: int = int(access_datetime_exp.timestamp())

        access_payload = TokenPayloadSchema(
            sub=str(user.id),
            jti=str(uuid4()),
            iat=now_unix,
            exp=exp_access_unix,
            nbf=now_unix,
            type=TokenType.ACCESS,
        )

        return jwt.encode(
            payload=access_payload.model_dump(),
            key=cls.private_key,
            algorithm=cls.alg,
        )

    @classmethod
    def get_payload(cls, jwt_str: str) -> TokenPayloadSchema:
        try:
            payload = TokenPayloadSchema.model_validate(
                jwt.decode(
                    jwt=jwt_str,
                    key=cls.public_key,
                    algorithms=[
                        cls.alg,
                    ],
                ),
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise JwtTokenExpiredError
        except jwt.PyJWTError as e:
            logger.error(e)
            raise InvalidJwtTokenError


class AuthService:
    def __init__(
        self,
        uow: UoWDI,
        user_service: UserServiceDI,
    ) -> None:
        self._uow = uow
        self._user_service = user_service

    async def register_user(
        self,
        create_user: UserCreateDTO,
    ) -> UserReadDTO:
        create_user.password = hash_password(create_user.password)
        new_user = await self._user_service.create_user(create_user)
        return new_user

    async def login_user(
        self,
        username: str,
        password: str,
    ) -> TokenRead:
        password_hash_from_db = await self._uow.users.get_password_hash_by_username(
            username,
        )

        if check_password(password, password_hash_from_db):
            user = await self._uow.users.get_user_by_username(username)
            return TokenRead(
                access_token=CryptoService.encode_access_token(user),
                refresh_token=CryptoService.encode_refresh_token(user),
            )

        raise PasswordOrUsernameInvalidError

    async def refresh_token(
        self,
        refresh_token: str,
    ) -> AuthTokenRead:
        user_payload = CryptoService.get_payload(refresh_token)
        user = await self._uow.users.get_user_by_id(int(user_payload.sub))
        access_token = CryptoService.encode_access_token(user)
        return AuthTokenRead(access_token=access_token)
