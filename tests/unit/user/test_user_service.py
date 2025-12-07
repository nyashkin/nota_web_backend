# tests/unit/entities/user/test_services.py
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.entities.user.dto import UserCreateDTO, UserReadDTO
from src.entities.user.enums import UserRoleEnum
from src.entities.user.schemas import UserUpdateSchema
from src.entities.user.services import UserService


# ==========================
# Fixtures
# ==========================
@pytest.fixture
def user_read_dto():
    now = datetime.now(UTC)
    return UserReadDTO(
        id=1,
        username="testuser",
        role=UserRoleEnum.CUSTOMER,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def create_user_read_dto():
    return UserCreateDTO(
        username="newuser",
        password="password123",
        role=UserRoleEnum.CUSTOMER,
    )


@pytest.fixture
def update_user_read_dto():
    return UserUpdateSchema(username="updateduser")


@pytest.fixture
def uow_mock(user_read_dto):
    uow = MagicMock()
    uow.users.create_user = AsyncMock(return_value=user_read_dto)
    uow.users.update_user = AsyncMock(return_value=user_read_dto)
    uow.users.get_user_by_id = AsyncMock(return_value=user_read_dto)
    uow.users.change_username = AsyncMock(return_value=user_read_dto)
    return uow


# ==========================
# UserService Tests
# ==========================
@pytest.mark.asyncio
class TestUserService:
    async def test_create_user(
        self,
        uow_mock,
        create_user_read_dto,
        user_read_dto,
    ):
        service = UserService(uow=uow_mock)
        result = await service.create_user(create_user_read_dto)

        uow_mock.users.create_user.assert_called_once_with(create_user_read_dto)
        assert result.id == user_read_dto.id
        assert result.username == user_read_dto.username
        assert result.role == user_read_dto.role

    async def test_update_user(
        self,
        uow_mock,
        update_user_read_dto,
        user_read_dto,
    ):
        service = UserService(uow=uow_mock)
        result = await service.update_user(user_id=1, update_user=update_user_read_dto)

        uow_mock.users.update_user.assert_called_once_with(
            1,
            update_user_read_dto,
        )
        assert result.id == user_read_dto.id
        assert result.username == user_read_dto.username

    async def test_get_user_by_id(
        self,
        uow_mock,
        user_read_dto,
    ):
        service = UserService(uow=uow_mock)
        result = await service.get_user_by_id(user_id=1)

        uow_mock.users.get_user_by_id.assert_called_once_with(1)
        assert result.id == user_read_dto.id
        assert result.username == user_read_dto.username

    async def test_change_username(
        self,
        uow_mock,
        user_read_dto,
    ):
        service = UserService(uow=uow_mock)
        result = await service.change_username(
            user_id=1,
            username="newname",
        )

        uow_mock.users.change_username.assert_called_once_with(
            1,
            "newname",
        )
        assert result.id == user_read_dto.id
        assert result.username == user_read_dto.username
