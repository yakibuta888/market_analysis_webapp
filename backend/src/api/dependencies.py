import os

from src.settings import logger
from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_repository_mysql import UserRepositoryMysql
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name


def get_user_repository() -> UserRepository:
    if os.environ.get('TEST_ENVIRONMENT') == 'True':
        logger.info("Fetching MockUserRepository")
        return MockUserRepository()
    else:
        return MockUserRepository()
    # else:
    #     logger.info("Fetching UserRepositoryMysql")
    #     return UserRepositoryMysql()

def get_user_service():
    user_repository = get_user_repository()
    return UserService(user_repository)
