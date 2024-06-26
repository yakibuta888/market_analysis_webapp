# tests/application/web/api/test_auth_router.py
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from src.main import app
from src.application.web.api.dependencies import get_auth_service
from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.credentials_error import CredentialsError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.services.auth_service import AuthService
from src.infrastructure.authentication.jwt_token import create_access_token
from src.infrastructure.database.models import User as UserModel
# モックされた認証サービスとユーザーサービス
@pytest.fixture
def auth_service_mock():
    return Mock(spec=AuthService)

# テストクライアントのセットアップ
@pytest.fixture
def client(auth_service_mock: Mock):
    app.dependency_overrides[get_auth_service] = lambda: auth_service_mock
    return TestClient(app)


def test_login_success(client: TestClient, auth_service_mock: Mock):
    email = "test@example.com"
    password = "strongpassword123"
    token = create_access_token({"sub": email})
    auth_service_mock.authenticate_and_generate_token.return_value = token

    response = client.post("/login", json={"email": email, "password": password})

    assert response.status_code == 200
    response_token = response.json()
    assert response_token["access_token"] == token
    assert response_token["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, auth_service_mock: Mock):
    login_data = {
        "email": "test@example.com",
        "password": "invalid_password"
    }
    auth_service_mock.authenticate_and_generate_token.side_effect = InvalidUserInputError("Invalid credentials")

    response = client.post("/login", json=login_data)

    assert response.status_code == 400
    detail = json.loads(response.json()['detail'])
    assert "InvalidUserInputError" in detail['error_type']


def test_login_user_not_found(client: TestClient, auth_service_mock: Mock):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "any_password"
    }
    auth_service_mock.authenticate_and_generate_token.side_effect = UserNotFoundError("User not found")

    response = client.post("/login", json=login_data)

    assert response.status_code == 404
    detail = json.loads(response.json()['detail'])
    assert "UserNotFoundError" in detail['error_type']


def test_login_unexpected_error(auth_service_mock: Mock, client: TestClient):
    email = "test@example.com"
    password = "strongpassword123"
    auth_service_mock.authenticate_and_generate_token.side_effect = Exception("Unexpected error")

    response = client.post("/login", json={"email": email, "password": password})

    assert response.status_code == 500
    detail = json.loads(response.json()['detail'])
    assert "InternalServerError" in detail['error_type']


def test_read_users_me_success(client: TestClient, auth_service_mock: Mock):
    email = "test@example.com"
    token = create_access_token({"sub": email})
    user_entity = UserEntity.from_db(
        UserModel(
            id=1,
            email=email,
            hashed_password="valid_password",
            name="Test User"
        )
    )
    auth_service_mock.get_current_user.return_value = user_entity

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == email
    assert user_data["name"] == "Test User"


def test_read_users_me_invalid_token(client: TestClient, auth_service_mock: Mock):
    token = "invalid_token"
    auth_service_mock.get_current_user.side_effect = CredentialsError("Could not validate credentials")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 401
    detail = json.loads(response.json()['detail'])
    assert "CredentialsError" in detail['error_type']


def test_read_users_me_user_not_found(client: TestClient, auth_service_mock: Mock):
    email = "nonexistent@example.com"
    token = create_access_token({"sub": email})
    auth_service_mock.get_current_user.side_effect = UserNotFoundError("User not found")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 404
    detail = json.loads(response.json()['detail'])
    assert "UserNotFoundError" in detail['error_type']


def test_read_users_me_unexpected_error(client: TestClient, auth_service_mock: Mock):
    token = create_access_token({"sub": "test@example.com"})
    auth_service_mock.get_current_user.side_effect = Exception("Unexpected error")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 500
    detail = json.loads(response.json()['detail'])
    assert "InternalServerError" in detail['error_type']


def test_register_user_success(client: TestClient, auth_service_mock: Mock):
    user_create_model = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "name": "Test User"
    }
    expected_message = "Please check your email to verify your account."
    auth_service_mock.register_user.return_value = expected_message

    response = client.post("/register", json=user_create_model)

    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    auth_service_mock.register_user.assert_called_once_with(
        user_create_model["email"], user_create_model["password"], user_create_model["name"]
    )


def test_register_user_invalid_input(client: TestClient, auth_service_mock: Mock):
    user_create_model = {
        "email": "invalid_email",
        "password": "weak",
        "name": "Test User"
    }
    auth_service_mock.register_user.side_effect = InvalidUserInputError("Invalid input")

    response = client.post("/register", json=user_create_model)

    assert response.status_code == 400
    detail = json.loads(response.json()['detail'])
    assert "InvalidUserInputError" in detail['error_type']
    assert "Invalid input" in detail['detail']
    auth_service_mock.register_user.assert_called_once_with(
        user_create_model["email"], user_create_model["password"], user_create_model["name"]
    )


def test_register_user_unexpected_error(client: TestClient, auth_service_mock: Mock):
    user_create_model = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "name": "Test User"
    }
    auth_service_mock.register_user.side_effect = Exception("Unexpected error")

    response = client.post("/register", json=user_create_model)

    assert response.status_code == 500
    detail = json.loads(response.json()['detail'])
    assert "InternalServerError" in detail['error_type']
    assert "Unexpected error" in detail['detail']
    auth_service_mock.register_user.assert_called_once_with(
        user_create_model["email"], user_create_model["password"], user_create_model["name"]
    )


def test_verify_user_success(client: TestClient, auth_service_mock: Mock):
    token = "valid_token"
    expected_access_token = "valid_access_token"
    auth_service_mock.confirm_registration.return_value = expected_access_token

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 200
    assert response.json() == {"access_token": expected_access_token, "token_type": "bearer"}
    auth_service_mock.confirm_registration.assert_called_once_with(token)


def test_verify_user_invalid_input(client: TestClient):
    token = ""

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 400
    detail = json.loads(response.json()['detail'])
    assert "InvalidUserInputError" in detail['error_type']
    assert "Token not provided" in detail['detail']


def test_verify_user_invalid_token(client: TestClient, auth_service_mock: Mock):
    token = "invalid_token"
    auth_service_mock.confirm_registration.side_effect = CredentialsError("Invalid or expired token")

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 401
    detail = json.loads(response.json()['detail'])
    assert "CredentialsError" in detail['error_type']
    assert "Invalid or expired token" in detail['detail']
    auth_service_mock.confirm_registration.assert_called_once_with(token)


def test_verify_user_user_not_found(client: TestClient, auth_service_mock: Mock):
    token = "valid_token"
    auth_service_mock.confirm_registration.side_effect = UserNotFoundError("User not found")

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 404
    detail = json.loads(response.json()['detail'])
    assert "UserNotFoundError" in detail['error_type']
    assert "User not found" in detail['detail']
    auth_service_mock.confirm_registration.assert_called_once_with(token)


def test_verify_user_repository_error(client: TestClient, auth_service_mock: Mock):
    token = "valid_token"
    auth_service_mock.confirm_registration.side_effect = RepositoryError("Repository error")

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 500
    detail = json.loads(response.json()['detail'])
    assert "RepositoryError" in detail['error_type']
    assert "Repository error" in detail['detail']
    auth_service_mock.confirm_registration.assert_called_once_with(token)


def test_verify_user_unexpected_error(client: TestClient, auth_service_mock: Mock):
    token = "valid_token"
    auth_service_mock.confirm_registration.side_effect = Exception("Unexpected error")

    response = client.get(f"/verify?token={token}")

    assert response.status_code == 500
    detail = json.loads(response.json()['detail'])
    assert "InternalServerError" in detail['error_type']
    assert "Unexpected error" in detail['detail']
    auth_service_mock.confirm_registration.assert_called_once_with(token)
