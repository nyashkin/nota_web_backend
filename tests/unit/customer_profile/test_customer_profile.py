# tests/unit/customer_profile/test_service.py
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.entities.customer_profiles.dto import (
    CustomerProfileCreateDTO,
    CustomerProfileReadDTO,
    CustomerProfileUpdateDTO,
)
from src.entities.customer_profiles.exceptions.domain import (
    CustomerProfileNotFoundException,
)
from src.entities.customer_profiles.service import CustomerProfileService


# ==========================
# Fixtures
# ==========================
@pytest.fixture()
def uow_mock():
    uow = MagicMock()
    uow.customer_profiles = AsyncMock()
    return uow


@pytest.fixture()
def service(uow_mock):
    return CustomerProfileService(uow=uow_mock)


@pytest.fixture()
def customer_profile_read_dto():
    now = datetime.now(UTC)
    return CustomerProfileReadDTO(
        id=1,
        user_id=10,
        first_name="John",
        last_name="Doe",
        phone_number="+123456",
        updated_at=now,
        created_at=now,
    )


# ==========================
# CustomerProfileService Tests
# ==========================
@pytest.mark.asyncio
class TestCustomerProfileService:
    # --------------------------
    # GET
    # --------------------------
    async def test_get_customer_profile_by_user_id(
        self,
        service,
        uow_mock,
        customer_profile_read_dto,
    ):
        uow_mock.customer_profiles.get_customer_profile_by_user_id.return_value = (
            customer_profile_read_dto
        )

        result = await service.get_customer_profile_by_user_id(10)

        uow_mock.customer_profiles.get_customer_profile_by_user_id.assert_awaited_once_with(
            10,
        )
        assert result == customer_profile_read_dto

    async def test_get_customer_profile_by_user_id_not_found(self, service, uow_mock):
        uow_mock.customer_profiles.get_customer_profile_by_user_id.side_effect = (
            CustomerProfileNotFoundException
        )

        with pytest.raises(CustomerProfileNotFoundException):
            await service.get_customer_profile_by_user_id(10)

    # --------------------------
    # CREATE
    # --------------------------
    async def test_create_customer_profile(
        self,
        service,
        uow_mock,
        customer_profile_read_dto,
    ):
        create_dto = CustomerProfileCreateDTO(
            first_name="John",
            last_name="Doe",
            phone_number="+123456",
        )
        uow_mock.customer_profiles.create_customer_profile.return_value = (
            customer_profile_read_dto
        )

        result = await service.create_customer_profile(10, create_dto)

        uow_mock.customer_profiles.create_customer_profile.assert_awaited_once_with(
            10,
            create_dto,
        )
        assert result == customer_profile_read_dto

    # --------------------------
    # UPDATE
    # --------------------------
    async def test_update_customer_profile_by_user_id(
        self,
        service,
        uow_mock,
        customer_profile_read_dto,
    ):
        update_dto = CustomerProfileUpdateDTO(first_name="Updated")
        uow_mock.customer_profiles.update_customer_profile_by_user_id.return_value = (
            customer_profile_read_dto
        )

        result = await service.update_customer_profile_by_user_id(10, update_dto)

        uow_mock.customer_profiles.update_customer_profile_by_user_id.assert_awaited_once_with(
            10,
            update_dto,
        )
        assert isinstance(result, CustomerProfileReadDTO)
        assert result.first_name == customer_profile_read_dto.first_name

    async def test_update_customer_profile_not_found(self, service, uow_mock):
        update_dto = CustomerProfileUpdateDTO(first_name="Updated")
        uow_mock.customer_profiles.update_customer_profile_by_user_id.return_value = (
            None
        )

        with pytest.raises(CustomerProfileNotFoundException):
            await service.update_customer_profile_by_user_id(10, update_dto)
