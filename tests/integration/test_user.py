import uuid

import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from src.schemas.users import UserCreateResponseTest, UserResponse


async def test_register(async_client: AsyncClient):
    user_data = {
        "email": "testuser@example.com",
        "first_name": "some",
        "last_name": "user",
        "password": "Testuser1!",
    }
    response = await async_client.post(
        "/api/v1/users/register",
        json=user_data,
    )
    response_json = response.json()
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        user_response = UserResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")

    assert user_response.email == user_data["email"], "Email does not match"
    assert (
        user_response.first_name == user_data["first_name"]
    ), "First name does not match"
    assert (
        user_response.last_name == user_data["last_name"]
    ), "Last name does not match"
    assert (
        isinstance(user_response.id, uuid.UUID)
        and len(str(user_response.id)) > 0
    ), "Invalid user ID"
    assert (
        user_response.is_superuser is False
    ), "User should not be a superuser by default"


async def test_change_user_role(
    async_client: AsyncClient,
    create_superuser: UserCreateResponseTest,
    create_reader: UserCreateResponseTest,
):
    user_id = str(create_reader.id)
    new_role = "admin"
    headers = {"Authorization": f"Bearer {create_superuser.access_token}"}
    response = await async_client.patch(
        f"/api/v1/users/{user_id}/change-role?new_role={new_role}",
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        user_response = UserResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert user_response.email == create_reader.email, "Email does not match"
    assert user_response.role == new_role, "Role does not match"


async def test_get_users(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_three_readers: UserCreateResponseTest,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.get("/api/v1/users", headers=headers)
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    user_ids = []
    for user in response_json:
        try:
            UserResponse(**user)
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
        user_ids.append(user["id"])
    assert isinstance(
        response_json, list
    ), f"Expected a list, but got {type(response_json).__name__}"
    assert (
        len(response_json) == 4
    ), f"Expected 4 users, but got {len(response_json)}"
    assert len(user_ids) == len(set(user_ids)), "Duplicate user IDs found"


async def test_get_current_user(
    async_client: AsyncClient, create_reader: UserCreateResponseTest
):
    headers = {"Authorization": f"Bearer {create_reader.access_token}"}
    response = await async_client.get("/api/v1/users/me", headers=headers)
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        user_response = UserResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert user_response.id == create_reader.id, "User ID does not match"
    assert user_response.email == create_reader.email, "Email does not match"


async def test_update_current_user(
    async_client: AsyncClient, create_reader: UserCreateResponseTest
):
    headers = {"Authorization": f"Bearer {create_reader.access_token}"}
    json = {
        "first_name": "new_first_name",
        "last_name": "new_last_name",
    }
    response = await async_client.patch(
        "/api/v1/users/me", headers=headers, json=json
    )
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        user_response = UserResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert user_response.id == create_reader.id, "User ID does not match"
    assert user_response.first_name == json["first_name"]
    assert user_response.last_name == json["last_name"]


async def test_register_with_invalid_data(async_client: AsyncClient):
    user_data = {
        "email": "invalid_email",
        "first_name": "some",
        "last_name": "user",
        "password": "inv_pas",
    }
    response = await async_client.post(
        "/api/v1/users/register",
        json=user_data,
    )
    response_json = response.json()
    assert (
        response.status_code == 422
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    error_details = response_json["detail"]
    assert isinstance(
        error_details, list
    ), f"Expected 'detail' to be a list, but got {type(error_details).__name__}"

    email_errors = [
        err for err in error_details if "email" in err.get("loc", [])
    ]
    assert len(email_errors) > 0, "Expected validation error for 'email' field"

    password_errors = [
        err for err in error_details if "password" in err.get("loc", [])
    ]
    assert (
        len(password_errors) > 0
    ), "Expected validation error for 'password' field"


async def test_change_user_role_not_superuser(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_reader: UserCreateResponseTest,
):
    user_id = str(create_reader.id)
    new_role = "admin"
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.patch(
        f"/api/v1/users/{user_id}/change-role?new_role={new_role}",
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 403
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    assert (
        "Permission denied" in response_json["detail"]
    ), f"Expected 'Permission denied'. but got {response_json["detail"]}"


async def test_get_users_not_admin(
    async_client: AsyncClient,
    create_reader: UserCreateResponseTest,
    create_three_readers: UserCreateResponseTest,
):
    headers = {"Authorization": f"Bearer {create_reader.access_token}"}
    response = await async_client.get("/api/v1/users", headers=headers)
    response_json = response.json()
    assert (
        response.status_code == 403
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    assert (
        "Permission denied" in response_json["detail"]
    ), f"Expected 'Permission denied'. but got {response_json["detail"]}"


async def test_get_current_user_not_auth(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users/me")
    response_json = response.json()
    assert (
        response.status_code == 403
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    assert (
        "Not authenticated" in response_json["detail"]
    ), f"Expected 'Permission denied'. but got {response_json["detail"]}"


async def test_update_current_user_not_auth(async_client: AsyncClient):
    json = {
        "first_name": "new_first_name",
        "last_name": "new_last_name",
    }
    response = await async_client.patch("/api/v1/users/me", json=json)
    response_json = response.json()
    assert (
        response.status_code == 403
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    assert (
        "Not authenticated" in response_json["detail"]
    ), f"Expected 'Permission denied'. but got {response_json["detail"]}"
