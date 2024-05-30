# tests/domain/services/test_auth_service.py

import pytest
from jose import jwt
from unittest.mock import Mock, patch

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.credentials_error import CredentialsError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.services.auth_service import AuthService
from src.domain.services.email_service import EmailService
from src.domain.services.user_service import UserService
from src.domain.repositories.temp_user_repository import TempUserRepository
from src.infrastructure.authentication.jwt_token import create_access_token, verify_token, SECRET_KEY, ALGORITHM
from src.infrastructure.authentication.verification_token import generate_verification_token


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def temp_user_repository_mock():
    return Mock(spec=TempUserRepository)


@pytest.fixture
def email_service_mock():
    email_service = Mock(spec=EmailService)
    email_service.send_verification_email = Mock()
    return email_service

@pytest.fixture
def auth_service(user_service_mock: Mock, temp_user_repository_mock: Mock, email_service_mock: Mock):
    return AuthService(user_service=user_service_mock, email_service=email_service_mock, temp_user_repository=temp_user_repository_mock)


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


@patch("src.domain.services.auth_service.generate_verification_token")
def test_register_user_success(mock_generate_verification_token: Mock, auth_service: AuthService, temp_user_repository_mock: Mock, email_service_mock: Mock):
    email = "test@example.com"
    password = "strongpassword123"
    name = "Test User"
    token = "fixed_verification_token"
    mock_generate_verification_token.return_value = token

    message = auth_service.register_user(email, password, name)

    temp_user_repository_mock.save_temp_user.assert_called_once()
    email_service_mock.send_verification_email.assert_called_once_with(email, token)
    assert "アカウントの確認のため、Eメールをご確認ください。" in message


def test_register_user_invalid_input(auth_service: AuthService):
    with pytest.raises(InvalidUserInputError):
        auth_service.register_user("invalidemail", "password", "Test User")


def test_confirm_registration_success(auth_service: AuthService, temp_user_repository_mock: Mock, user_service_mock: Mock):
    email = "test@example.com"
    password = "strongpassword123"
    name = "Test User"
    token = generate_verification_token(email)
    temp_user = UserEntity.new_entity(email=email, password=password, name=name)

    temp_user_repository_mock.fetch_temp_user_by_email.return_value = temp_user
    user_service_mock.save_user.return_value = temp_user

    access_token = auth_service.confirm_registration(token)

    temp_user_repository_mock.fetch_temp_user_by_email.assert_called_once_with(email)
    user_service_mock.save_user.assert_called_once_with(temp_user)
    assert access_token is not None


def test_confirm_registration_invalid_token(auth_service: AuthService):
    with pytest.raises(CredentialsError):
        auth_service.confirm_registration("invalid_token")


def test_confirm_registration_user_not_found(auth_service: AuthService, temp_user_repository_mock: Mock):
    token = generate_verification_token("test@example.com")
    temp_user_repository_mock.fetch_temp_user_by_email.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError):
        auth_service.confirm_registration(token)


def test_confirm_registration_invalid_user_input(auth_service: AuthService, temp_user_repository_mock: Mock, user_service_mock: Mock):
    email = "test@example.com"
    token = generate_verification_token(email)
    temp_user = UserEntity.new_entity(email=email, password="password", name="Test User")
    temp_user_repository_mock.fetch_temp_user_by_email.return_value = temp_user
    user_service_mock.save_user.side_effect = RepositoryError("Repository error")

    with pytest.raises(RepositoryError):
        auth_service.confirm_registration(token)
