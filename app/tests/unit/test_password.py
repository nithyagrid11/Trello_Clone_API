from app.utils.password import (hash_password,verify_password)

def test_hash_password_changes_value():
    password = "mypassword"
    hashed = hash_password(password)
    assert hashed != password

def test_verify_password_success():
    password = "mypassword"
    hashed = hash_password(password)
    assert verify_password(
        password,
        hashed
    ) is True

def test_verify_password_failure():
    password = "mypassword"
    hashed = hash_password(password)
    assert verify_password(
        "wrongpassword",
        hashed
    ) is False