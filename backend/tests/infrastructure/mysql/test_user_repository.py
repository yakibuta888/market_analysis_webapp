# tests/infrastructure/test_user_repository.py
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.settings import logger
from src.infrastructure.mysql.user_repository_mysql import UserRepositoryMysql
from src.infrastructure.database.models import User as UserModel
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email


@pytest.fixture(scope="function")
def user_repository(db_session: Session):
    return UserRepositoryMysql(db_session)


def test_create_user(user_repository: UserRepositoryMysql, db_session: Session):
    users_before = db_session.query(UserModel).all()
    logger.info(f"Users before insertion: {users_before}")

    # リポジトリのメソッドをテスト
    user_entity = UserEntity.new_entity(
        email="test@example.com",
        password="strongpassword123",
        name="Test User"
    )
    user_db = user_repository.create(user_entity)

    users_after = db_session.query(UserModel).all()
    logger.info(f"Users after insertion: {users_after}")

    assert user_db.email == user_entity.email
    assert user_db.name == user_entity.name


def test_fetch_user_by_id(user_repository: UserRepositoryMysql):
    user_entity = UserEntity.new_entity(
        email="test2@example.com",
        password="anotherpassword123",
        name="Another User"
    )
    user_db = user_repository.create(user_entity)
    fetched_user = user_repository.fetch_by_id(user_db.id)

    assert fetched_user.email == user_entity.email
    assert fetched_user.name == user_entity.name


def test_fetch_user_by_email(user_repository: UserRepositoryMysql):
    user_entity = UserEntity.new_entity(
        email="test3@example.com",
        password="yetanotherpassword123",
        name="Yet Another User"
    )
    user_repository.create(user_entity)
    fetched_user = user_repository.fetch_by_email(Email("test3@example.com"))

    assert fetched_user.email == user_entity.email
    assert fetched_user.name == user_entity.name


def test_fetch_user_by_id_not_found(user_repository: UserRepositoryMysql):
    with pytest.raises(ValueError) as excinfo:
        user_repository.fetch_by_id(999)

    assert "User with id 999 not found" in str(excinfo.value)


def test_fetch_user_by_email_not_found(user_repository: UserRepositoryMysql):
    with pytest.raises(ValueError) as excinfo:
        user_repository.fetch_by_email(Email("nonexistent@example.com"))

    assert "User with email nonexistent@example.com not found" in str(excinfo.value)


def test_create_duplicate_user(user_repository: UserRepositoryMysql):
    user_entity = UserEntity.new_entity(
        email="duplicate@example.com",
        password="password123",
        name="Duplicate User"
    )
    user_repository.create(user_entity)

    with pytest.raises(SQLAlchemyError) as excinfo:  # データベース固有の例外をここで捕捉する
        user_repository.create(user_entity)

    assert "Duplicate entry" in str(excinfo.value)  # エラーメッセージはデータベースによって異なる場合があるので注意
