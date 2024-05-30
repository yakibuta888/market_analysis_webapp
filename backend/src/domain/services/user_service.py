# src/domain/services/user_service.py
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.database.models import User as UserModel
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.settings import logger


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    def create_user(self, email: str, password: str, name: str) -> UserEntity:
        try:
            user_entity = UserEntity.new_entity(
                email=email,
                password=password,
                name=name
            )
            user_db: UserModel = self.user_repository.create(user_entity)
            return UserEntity.from_db(user_db)
        except (ValueError, NotImplementedError) as e:
            logger.error(f"An error occurred while creating user: {str(e)}")
            raise InvalidUserInputError(str(e))
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while creating user: {str(e)}")
            raise RepositoryError(f"An error occurred while creating user: {str(e)}")


    def save_user(self, user_entity: UserEntity) -> UserEntity:
        try:
            user_db: UserModel = self.user_repository.create(user_entity)
            return UserEntity.from_db(user_db)
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while saving user: {str(e)}")
            raise RepositoryError(f"An error occurred while saving user: {str(e)}")


    def fetch_user_by_id(self, user_id: int) -> UserEntity:
        try:
            user_db: UserModel = self.user_repository.fetch_by_id(user_id)
            return UserEntity.from_db(user_db)
        except ValueError as e:
            raise UserNotFoundError(f"User not found. id: {user_id}\n details: {e}")


    def fetch_user_by_email(self, email: str) -> UserEntity:
        try:
            user_db: UserModel = self.user_repository.fetch_by_email(Email(email))
            return UserEntity.from_db(user_db)
        except ValueError as e:
            raise UserNotFoundError(f"User not found. email: {email}\n details: {e}")


    def change_user_attributes(self, user_id: int, new_email: str | None = None, new_password: str | None = None, new_name: str | None = None) -> UserEntity:
        user_entity = self.fetch_user_by_id(user_id)
        try:
            if new_email is not None:
                user_entity = user_entity.change_email(new_email)
            if new_password is not None:
                user_entity = user_entity.change_password(new_password)
            if new_name is not None:
                user_entity = user_entity.change_name(new_name)
            user_db = self.user_repository.update(user_entity)
        except ValueError as e:
            raise InvalidUserInputError(str(e))
        return UserEntity.from_db(user_db)
