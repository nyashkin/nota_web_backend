# tests/unit/auth/test_services.py
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest

from src.auth.enums import TokenType
from src.auth.exceptions.domain import (
    InvalidJwtTokenException,
    JwtTokenExpiredException,
    PasswordOrUsernameInvalidException,
)
from src.auth.schemas import AuthTokenRead, TokenRead
from src.auth.services import AuthService, CryptoService
from src.entities.user.dto import UserCreateDTO, UserReadDTO
from src.entities.user.enums import UserRoleEnum


# ==========================
# Fixtures
# ==========================
@pytest.fixture
def user_read_dto() -> UserReadDTO:
    now_unix: int = int(datetime.now(timezone.utc).timestamp())
    return UserReadDTO(
        id=1,
        username="testuser",
        role=UserRoleEnum.CUSTOMER,
        created_at=now_unix,
        updated_at=now_unix,
    )


@pytest.fixture
def create_user_read_dto() -> UserCreateDTO:
    return UserCreateDTO(
        username="newuser",
        password="password123",
        role=UserRoleEnum.CUSTOMER,
    )


@pytest.fixture
def uow_mock():
    uow = MagicMock()
    uow.users.get_password_hash_by_username = AsyncMock(return_value="hashed_password")
    uow.users.get_user_by_username = AsyncMock()
    uow.users.get_user_by_id = AsyncMock()
    return uow


@pytest.fixture
def user_service_mock(user_read_dto):
    service = MagicMock()
    service.create_user = AsyncMock(return_value=user_read_dto)
    return service


# ==========================
# CryptoService Tests
# ==========================
class TestCryptoService:
    def test_encode_decode_access_token(self, user_read_dto):
        token = CryptoService.encode_access_token(user_read_dto)
        assert token is not None

        payload = CryptoService.get_payload(token)
        assert payload.sub == str(user_read_dto.id)
        assert payload.type == TokenType.ACCESS

    def test_encode_decode_refresh_token(self, user_read_dto):
        token = CryptoService.encode_refresh_token(user_read_dto)
        assert token is not None

        payload = CryptoService.get_payload(token)
        assert payload.sub == str(user_read_dto.id)
        assert payload.type == TokenType.REFRESH

    def test_get_payload_invalid_token(self):
        with pytest.raises(InvalidJwtTokenException):
            CryptoService.get_payload("invalid.token.string")

    def test_get_payload_expired_token(self, user_read_dto):
        expired_payload = {
            "sub": str(user_read_dto.id),
            "jti": "123",
            "iat": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()),
            "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),
            "nbf": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()),
            "type": TokenType.ACCESS,
        }
        token = jwt.encode(
            expired_payload, CryptoService.private_key, algorithm=CryptoService.alg,
        )
        with pytest.raises(JwtTokenExpiredException):
            CryptoService.get_payload(token)


# ==========================
# AuthService Tests
# ==========================
@pytest.mark.asyncio
class TestAuthService:
    async def test_register_user(
        self, uow_mock, user_service_mock, create_user_read_dto, user_read_dto,
    ):
        service = AuthService(uow=uow_mock, user_service=user_service_mock)
        result = await service.register_user(create_user_read_dto)

        user_service_mock.create_user.assert_called_once()
        assert result == user_read_dto

    async def test_login_user_success(
        self, uow_mock, user_service_mock, user_read_dto, monkeypatch,
    ):
        service = AuthService(uow=uow_mock, user_service=user_service_mock)

        monkeypatch.setattr(
            "src.auth.services.check_password", lambda pw, hash_pw: True,
        )
        uow_mock.users.get_user_by_username.return_value = user_read_dto

        result = await service.login_user("testuser", "password")
        assert isinstance(result, TokenRead)
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"

    async def test_login_user_invalid_password(
        self, uow_mock, user_service_mock, monkeypatch,
    ):
        service = AuthService(uow=uow_mock, user_service=user_service_mock)

        monkeypatch.setattr(
            "src.auth.services.check_password", lambda pw, hash_pw: False,
        )

        with pytest.raises(PasswordOrUsernameInvalidException):
            await service.login_user("testuser", "wrongpassword")

    async def test_refresh_token_success(self, uow_mock, user_read_dto):
        service = AuthService(uow=uow_mock, user_service=MagicMock())

        refresh_token = CryptoService.encode_refresh_token(user_read_dto)
        uow_mock.users.get_user_by_id.return_value = user_read_dto

        result = await service.refresh_token(refresh_token)
        assert isinstance(result, AuthTokenRead)
        assert result.access_token is not None
        assert result.token_type == "bearer"

    async def test_refresh_token_invalid(self):
        service = AuthService(uow=MagicMock(), user_service=MagicMock())

        with pytest.raises(InvalidJwtTokenException):
            await service.refresh_token("invalid.token.string")
