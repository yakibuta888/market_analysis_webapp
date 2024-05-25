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
