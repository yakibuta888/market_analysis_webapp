# src/domain/services/auth_service.py

from sqlalchemy.orm import Session
from src.domain.entities.user_entity import UserEntity
from src.domain.services.user_service import UserService
from src.domain.value_objects.password import Password
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError

def authenticate_user(db: Session, email: str, password: str) -> UserEntity | None:
    try:
        user_entity = UserService.fetch_user_by_email(email)
        if not Password.verify_password(password, user_entity.hashed_password):
            return None
        return user_entity
    except Exception as e:
        raise InvalidUserInputError(f"Invalid credentials: {e}")
