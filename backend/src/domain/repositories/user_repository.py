from abc import ABC, abstractmethod
from src.domain.entities.user_entity import UserEntity
from src.domain.value_objects.email import Email
from src.infrastructure.database.models import User as UserModel

class UserRepository(ABC):
    @abstractmethod
    def create(self, user_entity: UserEntity) -> UserModel:
        pass

    @abstractmethod
    def fetch_by_id(self, user_id: int) -> UserModel:
        pass

    @abstractmethod
    def fetch_by_email(self, email: Email) -> UserModel:
        pass

    @abstractmethod
    def update(self, user_entity: UserEntity) -> UserModel:
        pass
