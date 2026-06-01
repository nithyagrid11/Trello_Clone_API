def test_create_board(client):

    client.post(
        "/auth/register",
        json={
            "email": "owner@test.com",
            "password": "password123",
            "first_name": "Owner",
            "last_name": "User"
        }
    )
    login = client.post(
        "/auth/login",
        data={
            "username": "owner@test.com",
            "password": "password123"
        }
    )
    token = login.json()["access_token"]
    response = client.post(
        "/boards/",
        json={
            "name": "Project Board",
            "description": "Test Board"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Project Board"