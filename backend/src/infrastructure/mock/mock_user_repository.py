
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.infrastructure.database.models import User as UserModel


class MockUserRepository(UserRepository):
    def __init__(self):
        self.users: dict[int, UserModel] = {}
        self.next_id: int = 1


    def create(self, user_entity: UserEntity) -> UserModel:
        user_db = UserModel(
            id=self.next_id,
            name=user_entity.name,  # Value Objectから値を抽出
            email=user_entity.email,  # 同上
            hashed_password=user_entity.hashed_password  # 同上
        )
        self.users[self.next_id] = user_db
        self.next_id += 1
        return user_db


    def fetch_by_id(self, user_id: int) -> UserModel:
        user_db = self.users.get(user_id)
        if not user_db:
            raise ValueError("User not found")
        return user_db


    def fetch_by_email(self, email: Email) -> UserModel:
        user_db = next((user for user in self.users.values() if user.email == email.email), None)
        if not user_db:
            raise ValueError("User not found")
        return user_db


    def update(self, user_entity: UserEntity) -> UserModel:
        if user_entity.id in self.users:
            updated_user = self.users[user_entity.id]
            updated_user.name = user_entity.name
            updated_user.email = user_entity.email
            updated_user.hashed_password = user_entity.hashed_password
            return updated_user
        else:
            raise ValueError("User not found")
