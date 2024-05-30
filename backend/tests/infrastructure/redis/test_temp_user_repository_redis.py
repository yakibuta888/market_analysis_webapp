# tests/infrastructure/redis/test_temp_user_repository_redis.py
import json
import pytest
import fakeredis

from src.domain.entities.user_entity import UserEntity
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.infrastructure.redis.temp_user_repository_redis import TempUserRepositoryRedis
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.name import Name

@pytest.fixture
def redis_client():
    return fakeredis.FakeStrictRedis()

@pytest.fixture
def temp_user_repository(redis_client: fakeredis.FakeStrictRedis):
    repo = TempUserRepositoryRedis()
    repo.redis_client = redis_client
    return repo

@pytest.fixture
def user_entity():
    return UserEntity.new_entity(
        email="test@example.com",
        password="password123",
        name="Test User"
    )

def test_save_temp_user(temp_user_repository: TempUserRepositoryRedis, user_entity: UserEntity):
    temp_user_repository.save_temp_user(user_entity, expiration=3600)
    saved_user_data: str | None = temp_user_repository.redis_client.get(user_entity.email)

    assert saved_user_data is not None
    saved_user_dict = json.loads(saved_user_data)
    assert saved_user_dict['email'] == user_entity.email
    assert saved_user_dict['hashed_password'] == user_entity.hashed_password
    assert saved_user_dict['name'] == user_entity.name

def test_fetch_temp_user_by_email(temp_user_repository: TempUserRepositoryRedis, user_entity: UserEntity):
    temp_user_repository.save_temp_user(user_entity, expiration=3600)
    fetched_user = temp_user_repository.fetch_temp_user_by_email(user_entity.email)

    assert fetched_user.email == user_entity.email
    assert fetched_user.hashed_password == user_entity.hashed_password
    assert fetched_user.name == user_entity.name
    assert temp_user_repository.redis_client.get(user_entity.email) is None

def test_fetch_temp_user_by_email_not_found(temp_user_repository: TempUserRepositoryRedis):
    with pytest.raises(UserNotFoundError):
        temp_user_repository.fetch_temp_user_by_email("nonexistent@example.com")

def test_delete_temp_user(temp_user_repository: TempUserRepositoryRedis, user_entity: UserEntity):
    temp_user_repository.save_temp_user(user_entity, expiration=3600)
    temp_user_repository._delete_temp_user(user_entity.email)

    assert temp_user_repository.redis_client.get(user_entity.email) is None
