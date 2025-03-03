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
