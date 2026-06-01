from app.models.user import User

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"


def test_duplicate_email_registration(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Email already registered"
    )

def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):

    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid email or password"
    )


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid email or password"
    )