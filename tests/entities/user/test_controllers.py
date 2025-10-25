import pytest
from fastapi.testclient import TestClient

from src.entities.user.enums import UserRole
from src.entities.user.schemas import UserCreateSchema, UserReadSchema


@pytest.fixture(scope="class")
def shared_data():
    return {}


class TestUserControllers:
    def test_create_user(self, client: TestClient, shared_data: dict):
        create_user_schema = UserCreateSchema(
            username="user",
            password="secret_password",
            role=UserRole.USER,
        )
        response = client.post("/users/", json=create_user_schema.model_dump())
        shared_data["created_user_json"] = response.text
        assert response.status_code == 201

    def test_get_user_by_id(self, client: TestClient, shared_data: dict):
        created_user_json: str = shared_data["created_user_json"]
        created_user_schema = UserReadSchema.model_validate_json(created_user_json)

        response = client.get(f"/users/{created_user_schema.id}")

        getted_user_json = response.text
        getted_user_schema = UserReadSchema.model_validate_json(getted_user_json)

        assert created_user_schema == getted_user_schema

        shared_data["getted_user_schema"] = getted_user_schema

    def test_update_username(self, client: TestClient, shared_data: dict):
        getted_user_schema: UserReadSchema = shared_data["getted_user_schema"]
        new_name_prefix = "changed_"

        params: dict[str, int | str] = {
            "user_id": getted_user_schema.id,
            "new_username": new_name_prefix + getted_user_schema.username,
        }
        response_with_updated_username_from_change_endpoint = client.put(
            f"/users/{getted_user_schema.id}", params=params
        )

        response_with_updated_username = client.get(f"/users/{getted_user_schema.id}")

        user_with_updated_username = UserReadSchema.model_validate_json(
            response_with_updated_username.text
        )

        assert (
            new_name_prefix + getted_user_schema.username
            == user_with_updated_username.username
        )

        assert (
            response_with_updated_username_from_change_endpoint.text
            == response_with_updated_username.text
        )
