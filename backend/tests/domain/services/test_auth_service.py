# tests/domain/services/test_auth_service.py

import pytest
from jose import jwt
from unittest.mock import Mock

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.credentials_error import CredentialsError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name
from src.infrastructure.authentication.jwt_token import create_access_token, verify_token, SECRET_KEY, ALGORITHM


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def auth_service(user_service_mock: Mock):
    return AuthService(user_service=user_service_mock)


def test_authenticate_user_success(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "valid_password"

    user_entity = UserEntity.new_entity(
        email=email,
        password=password,
        name="Test User"
    )

    user_service_mock.fetch_user_by_email.return_value = user_entity

    authenticated_user = auth_service._authenticate_user(email, password)

    assert authenticated_user == user_entity
    user_service_mock.fetch_user_by_email.assert_called_once_with(email)


def test_authenticate_user_invalid_password(auth_service:AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "invalid_password"
    valid_password = "valid_password"

    user_entity = UserEntity.new_entity(
        email=email,
        password=valid_password,
        name="Test User"
    )

    user_service_mock.fetch_user_by_email.return_value = user_entity

    with pytest.raises(InvalidUserInputError) as exc_info:
        auth_service._authenticate_user(email, password)

    assert str(exc_info.value) == "Incorrect password"
    user_service_mock.fetch_user_by_email.assert_called_once_with(email)


def test_authenticate_user_user_not_found(auth_service:AuthService, user_service_mock: Mock):
    email = "nonexistent@example.com"
    password = "any_password"

    user_service_mock.fetch_user_by_email.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError) as exc_info:
        auth_service._authenticate_user(email, password)

    assert str(exc_info.value) == "User not found"
    user_service_mock.fetch_user_by_email.assert_called_once_with(email)


def test_generate_token_success(auth_service: AuthService):
    user_entity = UserEntity.new_entity(
        email="test@example.com",
        password="strongpassword123",
        name="Test User"
    )

    token = auth_service._generate_token(user_entity)

    assert token is not None
    assert verify_token(token) == user_entity.email
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    assert "exp" in payload


def test_authenticate_and_generate_token_success(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "strongpassword123"
    user_entity = UserEntity.new_entity(
        email=email,
        password=password,
        name="Test User"
    )

    user_service_mock.fetch_user_by_email.return_value = user_entity

    token = auth_service.authenticate_and_generate_token(email, password)

    assert token is not None
    assert verify_token(token) == email


def test_authenticate_and_generate_token_user_not_found(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "strongpassword123"

    user_service_mock.fetch_user_by_email.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError):
        auth_service.authenticate_and_generate_token(email, password)


def test_authenticate_and_generate_token_invalid_password(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "wrongpassword"
    correct_password = "correctpassword"
    user_entity = UserEntity.new_entity(
        email=email,
        password=correct_password,
        name="Test User"
    )

    user_service_mock.fetch_user_by_email.return_value = user_entity

    with pytest.raises(InvalidUserInputError):
        auth_service.authenticate_and_generate_token(email, password)


def test_authenticate_and_generate_token_unexpected_error(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    password = "any_password"

    user_service_mock.fetch_user_by_email.side_effect = Exception("Unexpected error")

    with pytest.raises(Exception) as exc_info:
        auth_service.authenticate_and_generate_token(email, password)

    assert "An unexpected error occurred" in str(exc_info.value)
    user_service_mock.fetch_user_by_email.assert_called_once_with(email)


def test_get_current_user_success(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    token = create_access_token({"sub": email})
    password = "strongpassword123"
    user_entity = UserEntity.new_entity(
        email=email,
        password=password,
        name="Test User"
    )

    user_service_mock.fetch_user_by_email.return_value = user_entity

    user = auth_service.get_current_user(token)

    assert user == user_entity
    assert user.email == email
    user_service_mock.fetch_user_by_email.assert_called_once_with(email)


def test_get_current_user_invalid_token(auth_service: AuthService, user_service_mock: Mock):
    token = "invalid.token.value"

    with pytest.raises(CredentialsError):
        auth_service.get_current_user(token)


def test_get_current_user_user_not_found(auth_service: AuthService, user_service_mock: Mock):
    email = "test@example.com"
    token = create_access_token({"sub": email})

    user_service_mock.fetch_user_by_email.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError):
        auth_service.get_current_user(token)
