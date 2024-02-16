# tests/conftest.py

import os
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from ..alembic.config import generate_alembic_config
from src.domain.helpers.path import get_project_root
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.infrastructure.mock.mock_service import MockUserService
from src.infrastructure.database.database import get_engine, Base


def mock_user_repository():
    user_repository = MockUserRepository()
    test_user = UserEntity(
        id=1,
        email=Email("test@example.com"),
        password_hash=Password("hashed_password123"),
        name=Name("Test User")
    )
    user_repository.create(test_user)
    return user_repository

@pytest.fixture(scope="session")
def mock_user_service():
    user_repository = mock_user_repository()
    return MockUserService(user_repository)

@pytest.fixture(scope="session", autouse=True)
def setup_alembic_config():
    # テスト用のAlembic設定ファイルを生成
    generate_alembic_config(testing=True)
    yield

@pytest.fixture(scope="session", autouse=True)
def apply_migrations(setup_alembic_config: None):
    project_root = get_project_root()
    alembic_cfg = Config(os.path.join(project_root, "alembic.ini"))
    # テスト用のデータベース接続情報をAlembic設定にセット
    alembic_cfg.set_main_option("sqlalchemy.url", str(get_engine(testing=True).url))
    command.upgrade(alembic_cfg, "head")  # マイグレーションの適用
    yield
    command.downgrade(alembic_cfg, "base")  # テスト完了後にマイグレーションをロールバック

@pytest.fixture(scope="session")
def test_engine(apply_migrations: None):
    engine = get_engine(testing=True)  # テスト用エンジンの取得
    Base.metadata.create_all(engine)  # テスト用データベーススキーマの作成
    yield engine
    Base.metadata.drop_all(engine)  # テスト完了後にスキーマを削除

@pytest.fixture(scope="session")
def test_session_factory(test_engine: Engine):
    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return SessionFactory

@pytest.fixture(scope="function")
def db_session(test_session_factory: sessionmaker[Session]):
    SessionLocal = scoped_session(test_session_factory)
    # Base.metadata.create_all(bind=test_session_factory().bind)  # bindの指定を修正
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        SessionLocal.remove()
        # テスト用エンジンに基づいてテーブルを削除
        # Base.metadata.drop_all(bind=test_session_factory().bind)
