# tests/infrastructure/authentication/test_jwt_token.py
import os
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.authentication.jwt_token import create_access_token, verify_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.domain.exceptions.credentials_error import CredentialsError


def test_create_access_token():
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    assert token is not None
    assert isinstance(token, str)

    # Decode the token to check its contents
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "test@example.com"
    assert "exp" in decoded_data

    # Check expiration time
    expire = datetime.fromtimestamp(decoded_data["exp"], timezone.utc)
    assert expire > datetime.now(timezone.utc) + expires_delta - timedelta(seconds=10)


def test_verify_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, timedelta(minutes=15))

    class MockDepends:
        def __init__(self, token: str):
            self.token = token

        def __call__(self):
            return self.token

    # Valid token should return email
    assert verify_token(token=MockDepends(token)()) == "test@example.com"

    # Invalid token should raise CredentialsError
    with pytest.raises(CredentialsError):
        verify_token(token=MockDepends("invalid_token")())

    # Expired token should raise CredentialsError
    expired_token = create_access_token(data, timedelta(seconds=-1))
    with pytest.raises(CredentialsError):
        verify_token(token=MockDepends(expired_token)())


def test_verify_token_missing_sub():
    data = {"no_sub": "missing@example.com"}
    token = create_access_token(data, timedelta(minutes=15))

    class MockDepends:
        def __init__(self, token: str):
            self.token = token

        def __call__(self):
            return self.token

    with pytest.raises(CredentialsError):
        verify_token(token=MockDepends(token)())


def test_create_access_token_with_default_expiration():
    data = {"sub": "test_default_exp@example.com"}
    token = create_access_token(data)

    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "test_default_exp@example.com"
    assert "exp" in decoded_data

    expire = datetime.fromtimestamp(decoded_data["exp"], timezone.utc)
    assert expire > datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_MINUTES - timedelta(seconds=10)
    assert expire < datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_MINUTES + timedelta(seconds=10)
