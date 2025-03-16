from datetime import datetime

import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from src.core.exceptions.messages import ErrorMessage
from src.schemas.author import AuthorResponse
from src.schemas.book import BookLoanResponse, BookResponse
from src.schemas.genre import GenreResponse
from src.schemas.users import UserCreateResponseTest


async def test_create_book(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_author: AuthorResponse,
    create_genre: GenreResponse,
):
    book_data = {
        "title": "Война и мир",
        "published_at": "1865-03-10",
        "author_ids": create_author.id,
        "genre_ids": create_genre.id,
    }
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.post(
        f"/api/v1/books/create",
        json=book_data,
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        book_response = BookResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")

    assert isinstance(book_response.id, int), "Invalid ID"
    assert book_response.id > 0, "Invalid ID"
    assert book_response.title == book_data["title"]
    assert book_response.description is None
    assert (
        book_response.published_at
        == datetime.strptime(book_data["published_at"], "%Y-%m-%d").date()
    )
    assert book_response.available_copies == 0
    assert len(book_response.authors) == 1
    assert book_response.authors[0].name == create_author.name
    assert len(book_response.genres) == 1
    assert book_response.genres[0].name == create_genre.name


async def test_get_books(async_client: AsyncClient, create_three_books: None):
    response = await async_client.get("/api/v1/books")
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    book_ids = []
    for book in response_json:
        try:
            BookResponse(**book)
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
        book_ids.append(book["id"])
    assert isinstance(
        response_json, list
    ), f"Expected a list, but got {type(response_json).__name__}"
    assert (
        len(response_json) == 3
    ), f"Expected 3 books, but got {len(response_json)}"
    assert len(book_ids) == len(set(book_ids)), "Duplicate author IDs found"


async def test_update_book(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
):
    new_book_data = {
        "title": "new title",
        "description": "new description",
        "published_at": "1855-03-10",
        "available_copies": 10,
    }
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    book_id = create_book.id
    response = await async_client.patch(
        f"/api/v1/books/update/{book_id}",
        json=new_book_data,
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        book_response = BookResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
    assert book_response.id == create_book.id, "Book ID does not match"
    assert (
        book_response.title == new_book_data["title"]
    ), "Book 'title' does not match"
    assert (
        book_response.description == new_book_data["description"]
    ), "Book 'description' does not match"
    assert (
        book_response.published_at
        == datetime.strptime(new_book_data["published_at"], "%Y-%m-%d").date()
    ), "Book 'published_at' does not match"
    assert (
        book_response.available_copies == new_book_data["available_copies"]
    ), "Book 'available_copies' does not match"


async def test_delete_book(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    book_id = create_book.id
    response = await async_client.delete(
        f"/api/v1/books/delete/{book_id}",
        headers=headers,
    )
    response_json = response.json()
    assert response.status_code == 200
    assert (
        "Book deleted successfully" in response_json["message"]
    ), f"Expected 'Book deleted successfully'. but got {response_json["message"]}"


async def test_lend_book(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
    create_reader: UserCreateResponseTest,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.post(
        f"/api/v1/books/lend",
        json={"book_id": create_book.id, "user_id": str(create_reader.id)},
        headers=headers,
    )
    response_json = response.json()

    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    try:
        book_loan_response = BookLoanResponse(**response_json)
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")

    assert isinstance(book_loan_response.id, int), "Invalid ID"
    assert book_loan_response.id > 0, "Invalid ID"
    assert book_loan_response.user_id == create_reader.id
    assert book_loan_response.book_id == create_book.id
    assert isinstance(book_loan_response.loan_date, datetime)
    assert isinstance(book_loan_response.return_date, datetime)
    assert book_loan_response.returned is False


async def test_return_book(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
    create_reader: UserCreateResponseTest,
):
    headers_admin = {"Authorization": f"Bearer {create_admin.access_token}"}
    response_lend = await async_client.post(
        f"/api/v1/books/lend",
        json={"book_id": create_book.id, "user_id": str(create_reader.id)},
        headers=headers_admin,
    )

    headers_reader = {"Authorization": f"Bearer {create_reader.access_token}"}
    loan_id = response_lend.json()["id"]
    response_return = await async_client.post(
        f"/api/v1/books/return-book/{loan_id}",
        json={"loan_id": loan_id},
        headers=headers_reader,
    )
    response_return_json = response_return.json()
    assert (
        response_return.status_code == 200
    ), f"Unexpected status code: {response_return.status_code}, Response JSON: {response_return_json}"
    assert (
        "Book returned successfully" in response_return_json["message"]
    ), f"Expected 'Book returned successfully'. but got {response_return_json["message"]}"


async def test_get_popular_books(
    async_client: AsyncClient, create_three_books: None
):
    response = await async_client.get(
        f"/api/v1/books/statistics/popular-books",
    )
    response_json = response.json()
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    book_ids = []
    for book in response_json:
        assert "loan_count" in book, f"Expected 'loan_count' in book"
        try:
            BookResponse(**book)
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
        book_ids.append(book["id"])
    assert isinstance(
        response_json, list
    ), f"Expected a list, but got {type(response_json).__name__}"
    assert (
        len(response_json) == 3
    ), f"Expected 3 books, but got {len(response_json)}"
    assert len(book_ids) == len(set(book_ids)), "Duplicate author IDs found"


async def test_create_book_invalid_data(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
):
    book_data = {
        "published_at": "invalid_date",
        "author_ids": "invalid_id",
        "genre_ids": "invalid_id",
    }
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    response = await async_client.post(
        f"/api/v1/books/create",
        json=book_data,
        headers=headers,
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
    assert (
        len(error_details) == 4
    ), f"Expected 4 errors, but got {len(error_details)}"


async def test_delete_book_not_exists(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    book_id = 1
    response = await async_client.delete(
        f"/api/v1/books/delete/{book_id}",
        headers=headers,
    )
    response_json = response.json()
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "detail" in response_json
    ), f"'detail' key not found in response: {response_json}"
    assert response_json["detail"] == ErrorMessage.BOOK_NOT_FOUND


async def test_lend_book_no_copies(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
    create_reader: UserCreateResponseTest,
):
    headers = {"Authorization": f"Bearer {create_admin.access_token}"}
    await async_client.post(
        f"/api/v1/books/lend",
        json={"book_id": create_book.id, "user_id": str(create_reader.id)},
        headers=headers,
    )
    second_response = await async_client.post(
        f"/api/v1/books/lend",
        json={"book_id": create_book.id, "user_id": str(create_admin.id)},
        headers=headers,
    )
    second_response_json = second_response.json()
    assert (
        second_response.status_code == 404
    ), f"Unexpected status code: {second_response.status_code}, Response JSON: {second_response_json}"
    assert (
        "detail" in second_response_json
    ), f"'detail' key not found in response: {second_response_json}"
    assert second_response_json["detail"] == ErrorMessage.BOOK_COPY_NOT_FOUND


async def test_return_book_already_returned(
    async_client: AsyncClient,
    create_admin: UserCreateResponseTest,
    create_book: BookResponse,
    create_reader: UserCreateResponseTest,
):
    headers_admin = {"Authorization": f"Bearer {create_admin.access_token}"}
    response_lend = await async_client.post(
        f"/api/v1/books/lend",
        json={"book_id": create_book.id, "user_id": str(create_reader.id)},
        headers=headers_admin,
    )

    headers_reader = {"Authorization": f"Bearer {create_reader.access_token}"}
    loan_id = response_lend.json()["id"]
    await async_client.post(
        f"/api/v1/books/return-book/{loan_id}",
        json={"loan_id": loan_id},
        headers=headers_reader,
    )
    second_response_return = await async_client.post(
        f"/api/v1/books/return-book/{loan_id}",
        json={"loan_id": loan_id},
        headers=headers_reader,
    )
    second_response_return_json = second_response_return.json()
    assert (
        second_response_return.status_code == 404
    ), f"Unexpected status code: {second_response_return.status_code}, Response JSON: {second_response_return_json}"
    assert (
        "detail" in second_response_return_json
    ), f"'detail' key not found in response: {second_response_return_json}"
    assert (
        second_response_return_json["detail"]
        == ErrorMessage.BOOK_LOAN_NOT_FOUND
    )
