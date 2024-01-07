
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user_entity import UserEntity
from src.infrastructure.database.models import User as UserModel

class MockUserRepository(UserRepository):
    def create(self, user_entity: UserEntity) -> UserModel:
        # モックデータを返す
        return UserModel(
            id=1,
            email=user_entity.email,
            password_hash=user_entity.password_hash,
            name=user_entity.name,
        )

    def fetch_by_id(self, user_id: int) -> UserModel:
        # モックデータを返す
        return UserModel(
            id=user_id,
            email="mock@example.com",
            password_hash="hashed_password",
            name="Mock",
        )

    def update(self, user_entity: UserEntity) -> UserModel:
        # モックデータを返す
        return UserModel(
            id=user_entity.id,
            email=user_entity.email,
            password_hash=user_entity.password_hash,
            name=user_entity.name,
        )
