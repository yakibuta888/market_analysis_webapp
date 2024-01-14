import pytest

from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.infrastructure.mock.mock_service import MockUserService


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
