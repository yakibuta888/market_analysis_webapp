from abc import ABC, abstractmethod
from src.domain.entities.user_entity import UserEntity


class TempUserRepository(ABC):
    @abstractmethod
    def save_temp_user(self, user_entity: UserEntity, expiration: int) -> None:
        pass

    @abstractmethod
    def fetch_temp_user_by_email(self, email: str) -> UserEntity:
        pass

    @abstractmethod
    def _delete_temp_user(self, email: str) -> None:
        pass
