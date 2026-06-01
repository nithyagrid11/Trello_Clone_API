def test_get_me(client):

    client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    login = client.post(
        "/auth/login",
        data={
            "username": "user@test.com",
            "password": "password123"
        }
    )
    token = login.json()["access_token"]
    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"