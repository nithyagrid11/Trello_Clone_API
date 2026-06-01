def test_create_section(client):

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
    board = client.post(
        "/boards/",
        json={
            "name": "Board",
            "description": "Board Desc"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    board_id = board.json()["id"]
    response = client.post(
        "/sections/",
        json={
            "name": "Todo",
            "description": "Tasks",
            "board_id": board_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Todo"