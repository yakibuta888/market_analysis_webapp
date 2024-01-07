from src.domain.entities.user_entity import UserEntity
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.database.models import User as UserModel


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str, password: str) -> UserEntity:
        user_entity = UserEntity.new_entity(
            name=Name(name),
            email=Email(email),
            password_hash=Password(password)
        )
        user_db: UserModel = self.user_repository.create(user_entity)
        return UserEntity.from_db(user_db)

    def fetch_user_by_id(self, user_id: int) -> UserEntity:
        user_db: UserModel = self.user_repository.fetch_by_id(user_id)
        return UserEntity.from_db(user_db)

    def change_user_attributes(self, user_id: int, new_name: str | None = None, new_email: str | None = None, new_password: str | None = None) -> UserEntity:
        user_entity = self.fetch_user_by_id(user_id)
        if new_name is not None:
            user_entity.change_name(new_name)
        if new_email is not None:
            user_entity.change_email(new_email)
        if new_password is not None:
            user_entity.change_password(new_password)
        user_db = self.user_repository.update(user_entity)
        return UserEntity.from_db(user_db)
