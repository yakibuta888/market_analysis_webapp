# tests/infrastructure/test_user_repository.py

from sqlalchemy.orm import Session

from src.infrastructure.repositories.user_repository_mysql import UserRepositoryMysql
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.name import Name
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email


def test_create_user(db_session: Session):
    # リポジトリのメソッドをテスト
    test_user_repository_mysql = UserRepositoryMysql(db_session)
    user_entity = UserEntity(
        id=1,
        email=Email("test@example.com"),
        password_hash=Password.create("strongpassword123"),
        name=Name("Test User")
    )
    test_user_repository_mysql.create(user_entity)
    db_user = test_user_repository_mysql.fetch_by_email(Email("test@example.com"))
    assert db_user.email == user_entity.email.email
    assert db_user.name == user_entity.name.name
