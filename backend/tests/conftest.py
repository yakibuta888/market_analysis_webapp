# tests/conftest.py
import os
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from typing import Callable

from src.domain.helpers.path import get_project_root
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.infrastructure.mock.mock_service import MockUserService
from src.infrastructure.database.database import get_engine, Base


@pytest.fixture(scope='session', autouse=True)
def set_env_vars():
    original_database = os.getenv("MYSQL_DATABASE")
    os.environ["MYSQL_DATABASE"] = "test_database"
    yield
    # テスト終了後に元の環境変数に戻す
    os.environ["MYSQL_DATABASE"] = original_database if original_database is not None else ''

def mock_user_repository():
    user_repository = MockUserRepository()
    test_user = UserEntity(
        id=1,
        email=Email("test@example.com"),
        hashed_password=Password("hashed_password123"),
        name=Name("Test User")
    )
    user_repository.create(test_user)
    return user_repository

@pytest.fixture(scope="session")
def mock_user_service():
    user_repository = mock_user_repository()
    return MockUserService(user_repository)

@pytest.fixture(scope="session", autouse=True)
def apply_test_migrations(set_env_vars: Callable[[], None]):
    project_root = get_project_root()
    alembic_cfg = Config(os.path.join(project_root, "alembic_test.ini"))
    command.upgrade(alembic_cfg, "head")  # マイグレーションの適用
    yield
    command.downgrade(alembic_cfg, "base")  # テスト完了後にマイグレーションをロールバック

@pytest.fixture(scope="session")
def test_engine(apply_test_migrations: None):
    engine = get_engine()  # テスト用エンジンの取得
    Base.metadata.create_all(engine)  # テスト用データベーススキーマの作成
    yield engine
    # NOTE: alembicのdowngradeでスキーマを削除するため、drop_allを行うとテーブルの削除が重複するため、エラーが発生する。alembicを利用しない時はコメントアウトを外す。
    # Base.metadata.drop_all(engine)  # テスト完了後にスキーマを削除

@pytest.fixture(scope="session")
def test_session_factory(test_engine: Engine):
    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return SessionFactory

@pytest.fixture(scope="function")
def db_session(test_session_factory: sessionmaker[Session]):
    SessionLocal = scoped_session(test_session_factory)
    session = SessionLocal()
    # テスト前にデータベース内のデータをクリアする
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        SessionLocal.remove()

@pytest.fixture(scope="function")
def test_session():
    # インメモリSQLiteデータベースを作成
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # データベーススキーマを作成
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
