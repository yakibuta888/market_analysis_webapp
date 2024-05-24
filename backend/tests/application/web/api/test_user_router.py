# tests/application/web/api/test_user_router.py
import json
from fastapi.testclient import TestClient

from src.settings import logger
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.infrastructure.mock.mock_service import MockUserService
from tests.conftest import mock_user_service
from src.application.web.api.dependencies import get_user_service
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.main import app  # FastAPIアプリケーションインスタンスをインポート


client = TestClient(app)


def test_create_user_success(mock_user_service: MockUserService):
    logger.info("Starting test_create_user_success")
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123", "name": "Test User"})
    response_data = response.json()
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response data: {response_data}")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == "test@example.com"
    assert response.json()["name"] == "Test User"

def test_create_user_invalid_input(mock_user_service: MockUserService):
    logger.info("Starting test_create_user_invalid_input")
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    response = client.post("/users/", json={"email": "invalid-email", "password": "pwd", "name": ""})
    response_data = response.json()
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response data: {response_data}")
    detail_data = json.loads(response_data["detail"])
    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert detail_data["error_type"] == "InvalidUserInputError"
    assert detail_data["message"] == "Invalid input"
    assert detail_data["detail"] == "無効なメールアドレスです。"

def test_fetch_user_success(mock_user_service: MockUserService):
    logger.info("Starting test_fetch_user_success")
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    user_id = 1  # 既に存在するユーザーのID
    response = client.get(f"/users/{user_id}")
    response_data = response.json()
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response data: {response_data}")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_fetch_user_not_found(mock_user_service: MockUserService):
    logger.info("Starting test_fetch_user_not_found")
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    user_id = 999  # 存在しないユーザーのID
    response = client.get(f"/users/{user_id}")
    response_data = response.json()
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response data: {response_data}")
    detail_data = json.loads(response_data["detail"])
    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert detail_data["error_type"] == "UserNotFoundError"
    assert detail_data["message"] == "User not found"
    assert f"User not found. id: {user_id}" in detail_data["detail"]
