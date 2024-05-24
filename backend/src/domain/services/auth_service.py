# src/domain/services/auth_service.py

from sqlalchemy.orm import Session

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.services.user_service import UserService
from src.domain.value_objects.password import Password


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service


    def authenticate_user(self, email: str, password: str) -> UserEntity:
        try:
            user_entity = self.user_service.fetch_user_by_email(email)
            if not Password.verify_password(password, user_entity.hashed_password):
                raise InvalidUserInputError("Incorrect password")
            return user_entity
        except UserNotFoundError as e:
            raise e
        except InvalidUserInputError as e:
            raise e
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")
