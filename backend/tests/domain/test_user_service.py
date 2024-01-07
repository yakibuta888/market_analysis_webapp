import pytest
from src.domain.entities.user_entity import UserEntity
from src.domain.services.user_service import UserService
from src.infrastructure.mock.mock_user_repository import MockUserRepository

# テスト用のUserServiceインスタンスをセットアップ
@pytest.fixture
def user_service() -> UserService:
    user_repository = MockUserRepository()
    return UserService(user_repository)

# ユーザー作成機能のテスト
def test_create_user(user_service : UserService):
    # テスト用のユーザーデータ
    test_user = UserEntity(id=1, email="test@example.com", password_hash="hashed_password", name="Test")

    # UserServiceを使用してユーザーを作成
    created_user = user_service.create_user(test_user)

    # 期待される振る舞いのアサーション
    assert created_user.id == test_user.id
    assert created_user.email == test_user.email
    assert created_user.password_hash == test_user.password_hash
