from datetime import date, datetime

import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from src.schemas.author import AuthorResponse
from src.schemas.users import UserCreateResponseTest


async def test_create_author(
    async_client: AsyncClient, create_admin: UserCreateResponseTest
):
    author_data = {
        "name": "Alexander Pushkin",
        "birth_date": "2000-12-24",
        "biography": "Biography",
    }
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.post(
        f"/api/v1/authors/create",
        json=author_data,
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        author_response = AuthorResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert isinstance(author_response.id, int), "Invalid user ID"
    assert author_response.id > 0, "Invalid user ID"
    assert author_response.name == author_data["name"]
    assert (
        author_response.birth_date
        == datetime.strptime(author_data["birth_date"], "%Y-%m-%d").date()
    )
    assert isinstance(author_response.birth_date, date)
    assert author_response.biography == author_data["biography"]


async def test_get_authors(async_client: AsyncClient, create_three_authors):
    response = await async_client.get("/api/v1/authors")
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    author_ids = []
    for author in response_json:
        try:
            AuthorResponse(**author)
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
        author_ids.append(author["id"])
    assert isinstance(
        response_json, list
    ), f"Expected a list, but got {type(response_json).__name__}"
    assert (
        len(response_json) == 3
    ), f"Expected 3 authors, but got {len(response_json)}"
    assert len(author_ids) == len(
        set(author_ids)
    ), "Duplicate author IDs found"


async def test_update_author(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_author: AuthorResponse,
):
    new_author_data = {
        "name": "new name",
        "birth_date": "1999-12-24",
        "biography": "new biography",
    }
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    author_id = create_author.id
    response = await async_client.patch(
        f"/api/v1/authors/update/{author_id}",
        json=new_author_data,
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        author_response = AuthorResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert author_response.id == create_author.id, "Author ID does not match"
    assert (
        author_response.name == new_author_data["name"]
    ), "Author 'name' does not match"
    assert (
        author_response.birth_date
        == datetime.strptime(new_author_data["birth_date"], "%Y-%m-%d").date()
    ), "Author 'birth_date' does not match"
    assert (
        author_response.biography == new_author_data["biography"]
    ), "Author 'biography' does not match"


async def test_delete_author(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_author: AuthorResponse,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    author_id = create_author.id
    response = await async_client.delete(
        f"/api/v1/authors/delete/{author_id}",
        headers=headers,
    )
    response_json = response.json()
    assert response.status_code == 200
    assert (
        "Author deleted successfully" in response_json["message"]
    ), f"Expected 'Author deleted successfully'. but got {response_json["message"]}"
