from jose import jwt
from app.utils.jwt import create_access_token
from app.config import settings

def test_create_access_token_returns_string():
    token = create_access_token(
        {"sub": "test@example.com"}
    )
    assert isinstance(token, str)

def test_token_contains_email():
    token = create_access_token(
        {"sub": "test@example.com"}
    )
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    assert payload["sub"] == "test@example.com"

def test_token_contains_expiration():
    token = create_access_token(
        {"sub": "test@example.com"}
    )
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    assert "exp" in payload