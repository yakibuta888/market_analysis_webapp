# src/domain/services/auth_service.py
from datetime import timedelta

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.credentials_error import CredentialsError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.infrastructure.authentication.jwt_token import create_access_token, verify_token
from src.domain.services.user_service import UserService
from src.domain.value_objects.password import Password


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service


    def _authenticate_user(self, email: str, password: str) -> UserEntity:
        user_entity = self.user_service.fetch_user_by_email(email)
        if not Password.verify_password(password, user_entity.hashed_password):
            raise InvalidUserInputError("Incorrect password")
        return user_entity


    def _generate_token(self, user: UserEntity) -> str:
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return access_token


    def authenticate_and_generate_token(self, email: str, password: str) -> str:
        try:
            user_entity = self._authenticate_user(email, password)
            return self._generate_token(user_entity)
        except UserNotFoundError as e:
            raise e
        except InvalidUserInputError as e:
            raise e
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")


    def get_current_user(self, token: str) -> UserEntity:
        try:
            email = verify_token(token)
            return self.user_service.fetch_user_by_email(email)
        except CredentialsError as e:
            raise e
        except UserNotFoundError as e:
            raise e
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")
