# src/infrastructure/mysql/user_repository_mysql.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.user_entity import UserEntity
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.infrastructure.database.models import User as UserModel
from src.settings import logger


class UserRepositoryMysql(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_entity: UserEntity) -> UserModel:
        try:
            user_db = UserModel(
                email=user_entity.email,
                hashed_password=user_entity.hashed_password,
                name=user_entity.name,
            )
            self.session.add(user_db)
            self.session.commit()
            self.session.refresh(user_db)
            return user_db
        except SQLAlchemyError as e:
            logger.error(f"Failed to create user: {str(e)}")
            self.session.rollback()
            raise e


    def fetch_by_id(self, user_id: int) -> UserModel:
        user_db = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if user_db is None:
            raise ValueError(f"User with id {user_id} not found")
        return user_db


    def fetch_by_email(self, email: Email) -> UserModel:
        user_db = self.session.query(UserModel).filter(UserModel.email == email.email).first()
        if user_db is None:
            raise ValueError(f"User with email {email.email} not found")
        return user_db


    # TODO: 未実装
    def update(self, user_entity: UserEntity) -> UserModel:
        return super().update(user_entity)
