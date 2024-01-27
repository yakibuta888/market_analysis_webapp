# tests/infrastructure/test_user_repository.py

import pytest
from _pytest.monkeypatch import MonkeyPatch
from src.infrastructure.database.database import Base, engine
from src.api.dependencies import get_user_repository
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.name import Name
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email


@pytest.fixture(scope="function")
def user_repository_mysql(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("TEST_DATABASE", "True")
    monkeypatch.setenv("TEST_ENVIRONMENT", "False")
    # テスト用データベースエンジンを作成
    Base.metadata.create_all(bind=engine)  # テーブルを作成
    try:
        return get_user_repository()
    finally:
        Base.metadata.drop_all(bind=engine)  # テスト後にテーブルを削除

def test_create_user(user_repository_mysql: UserRepository):
    # リポジトリのメソッドをテスト
    user_entity = UserEntity(
        id=1,
        email=Email("test@example.com"),
        password_hash=Password.create("strongpassword123"),
        name=Name("Test User")
    )
    user_repository_mysql.create(user_entity)
    db_user = user_repository_mysql.fetch_by_email(Email("test@example.com"))
    assert db_user.email == user_entity.email.email
    assert db_user.name == user_entity.name.name
