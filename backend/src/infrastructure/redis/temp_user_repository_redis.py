# src/infrastructure/redis/temp_user_repository_redis.py
import json
import os
import redis

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.repositories.temp_user_repository import TempUserRepository
from src.infrastructure.database.models import User as UserModel


class TempUserRepositoryRedis(TempUserRepository):
    def __init__(
        self,
        redis_host: str = os.getenv('REDIS_HOST', 'localhost'),
        redis_port: int = int(os.getenv('REDIS_PORT', 6379)),
        redis_db: int = int(os.getenv('REDIS_DB', 0))
    ):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


    def save_temp_user(self, user_entity: UserEntity, expiration: int = 3600):
        user_data = json.dumps(user_entity.to_dict())
        self.redis_client.setex(user_entity.email, expiration, user_data)


    def fetch_temp_user_by_email(self, email: str) -> UserEntity:
        user_data: str | None = self.redis_client.get(email)
        if user_data is None:
            raise UserNotFoundError("Temp user not found")
        self._delete_temp_user(email)
        user_dict = json.loads(user_data)
        user_model = UserModel(**user_dict)
        return UserEntity.from_db(user_model)


    def _delete_temp_user(self, email: str):
        self.redis_client.delete(email)
