# tests/infrastructure/test_user_repository.py

from sqlalchemy.orm import Session

from src.settings import logger
from src.infrastructure.mysql.user_repository_mysql import UserRepositoryMysql
from src.infrastructure.database.models import User as UserModel
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.name import Name
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email


def test_create_user(db_session: Session):
    users_before = db_session.query(UserModel).all()
    logger.info(f"Users before insertion: {users_before}")

    # リポジトリのメソッドをテスト
    test_user_repository_mysql = UserRepositoryMysql(db_session)
    user_entity = UserEntity(
        id=1,
        email=Email("test@example.com"),
        hashed_password=Password.create("strongpassword123"),
        name=Name("Test User")
    )
    test_user_repository_mysql.create(user_entity)

    users_after = db_session.query(UserModel).all()
    logger.info(f"Users after insertion: {users_after}")

    db_user = test_user_repository_mysql.fetch_by_email(Email("test@example.com"))
    assert db_user.email == user_entity.email.email
    assert db_user.name == user_entity.name.name

    logger.info(f"User fetched by email: {db_user}")
