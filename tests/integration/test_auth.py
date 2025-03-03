async def test_login(async_client, create_reader):
    response = await async_client.post(
        "/api/v1/auth",
        json={
            "email": create_reader["email"],
            "password": create_reader["password"],
        },
    )
    response_json = response.json()

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" in response_json
    ), f"'refresh_token' not found in response JSON: {response_json}"


async def test_refresh_jwt(async_client, create_reader):
    headers = {"Authorization": f"Bearer {create_reader["refresh_token"]}"}
    response = await async_client.post("/api/v1/auth/refresh", headers=headers)
    response_json = response.json()

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" not in response_json
    ), f"'refresh_token' should not be present in response JSON: {response_json}"


async def test_login_invalid_credentials(async_client):
    response = await async_client.post(
        "/api/v1/auth",
        json={
            "email": "invalid_email@example.com",
            "password": "password",
        },
    )
    response_json = response.json()

    assert (
        response.status_code == 401
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" not in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" not in response_json
    ), f"'refresh_token' not found in response JSON: {response_json}"
    assert (
        response_json["detail"] == "Invalid credentials"
    ), f"Unexpected detail message: {response_json['detail']}"


async def test_refresh_jwt_with_access(async_client, create_reader):
    headers = {"Authorization": f"Bearer {create_reader["access_token"]}"}
    response = await async_client.post("/api/v1/auth/refresh", headers=headers)
    response_json = response.json()

    assert (
        response.status_code == 401
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" not in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" not in response_json
    ), f"'refresh_token' should not be present in response JSON: {response_json}"
    assert (
        response_json["detail"]
        == "Invalid token type 'access' expected 'refresh'"
    ), f"Unexpected detail message: {response_json['detail']}"


async def test_refresh_jwt_with_invalid_token(async_client, create_reader):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await async_client.post("/api/v1/auth/refresh", headers=headers)
    response_json = response.json()

    assert (
        response.status_code == 401
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" not in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" not in response_json
    ), f"'refresh_token' should not be present in response JSON: {response_json}"
    assert (
        response_json["detail"] == "Invalid token"
    ), f"Unexpected detail message: {response_json['detail']}"


async def test_refresh_jwt_not_auth(async_client, create_reader):
    response = await async_client.post("/api/v1/auth/refresh")
    response_json = response.json()

    assert (
        response.status_code == 403
    ), f"Unexpected status code: {response.status_code}, Response JSON: {response_json}"
    assert (
        "access_token" not in response_json
    ), f"'access_token' not found in response JSON: {response_json}"
    assert (
        "refresh_token" not in response_json
    ), f"'refresh_token' should not be present in response JSON: {response_json}"
    assert (
        response_json["detail"] == "Not authenticated"
    ), f"Unexpected detail message: {response_json['detail']}"
