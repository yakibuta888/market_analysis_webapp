# tests/domain/services/test_user_service.py
import pytest
from src.domain.entities.user_entity import UserEntity
from src.domain.services.user_service import UserService
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.exceptions.user_not_found_error import UserNotFoundError


# テスト用のUserServiceインスタンスをセットアップ
@pytest.fixture
def user_service() -> UserService:
    user_repository = MockUserRepository()
    user_repository.create(
        UserEntity.new_entity(
            email="existing@example.com",
            password="strongpassword123",
            name="Existing User"
        )
    )
    return UserService(user_repository)


def test_create_user(user_service: UserService):
    email, password, name = "test@example.com", "strongpassword123", "Test User"
    user_entity = user_service.create_user(email, password, name)

    assert user_entity.email == email
    assert user_entity.name == name
    assert Password.verify_password(password, user_entity.hashed_password)


def test_fetch_user_by_id(user_service: UserService):
    user_id = 1
    user_entity = user_service.fetch_user_by_id(user_id)

    assert user_entity.id == user_id
    assert user_entity.email == "existing@example.com"
    assert user_entity.name == "Existing User"


def test_fetch_user_by_email(user_service: UserService):
    user_entity = user_service.fetch_user_by_email("existing@example.com")

    assert user_entity.email == "existing@example.com"
    assert user_entity.name == "Existing User"


def test_change_user_attributes(user_service: UserService):
    user_id = 1
    new_email, new_password, new_name = "new@example.com", "newpassword123", "New Name"
    updated_user = user_service.change_user_attributes(user_id, new_email, new_password, new_name)

    assert updated_user.email == new_email
    assert updated_user.name == new_name
    assert Password.verify_password(new_password, updated_user.hashed_password)


def test_user_creation_and_retrieval(user_service: UserService):
    email, password, name = "test@example.com", "strongpassword123", "Test User"
    created_user = user_service.create_user(email, password, name)

    # ユーザーが作成されていることを確認
    assert created_user is not None
    assert created_user.email == email
    assert created_user.name == name

    # 同じユーザーがfetch_by_idで取得できることを確認
    assert created_user.id is not None
    fetched_user = user_service.fetch_user_by_id(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.email == email
    assert fetched_user.name == name


# UserServiceのテストの拡張

def test_create_user_with_invalid_email(user_service: UserService):
    invalid_email, valid_password, valid_name = "invalidemail", "strongpassword123", "Test User"
    with pytest.raises(InvalidUserInputError) as exc_info:
        user_service.create_user(invalid_email, valid_password, valid_name)
    assert "無効なメールアドレスです。" in exc_info.value.message

def test_fetch_non_existent_user(user_service: UserService):
    non_existent_user_id = 999
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.fetch_user_by_id(non_existent_user_id)
    assert f"User not found. id: {non_existent_user_id}" in exc_info.value.message

def test_fetch_user_by_invalid_email(user_service: UserService):
    invalid_email = "invalidemail"
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.fetch_user_by_email(invalid_email)
    assert f"User not found. email: {invalid_email}" in exc_info.value.message

def test_fetch_user_by_email_with_non_existent_email(user_service: UserService):
    non_existent_email = "non_existent@example.com"
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.fetch_user_by_email(non_existent_email)
    assert f"User not found. email: {non_existent_email}" in exc_info.value.message

def test_change_user_attributes_for_non_existent_user(user_service: UserService):
    non_existent_user_id = 999
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.change_user_attributes(non_existent_user_id)
    assert f"User not found. id: {non_existent_user_id}" in exc_info.value.message

def test_change_user_attributes_with_invalid_email(user_service: UserService):
    user_id = 1
    invalid_email = "invalidemail"
    with pytest.raises(InvalidUserInputError) as exc_info:
        user_service.change_user_attributes(user_id, new_email=invalid_email)
    assert "無効なメールアドレスです。" in exc_info.value.message

def test_change_user_attributes_with_invalid_password(user_service: UserService):
    user_id = 1
    invalid_password = "short"
    with pytest.raises(InvalidUserInputError) as exc_info:
        user_service.change_user_attributes(user_id, new_password=invalid_password)
    assert "パスワードは8文字以上である必要があります。" in exc_info.value.message

def test_change_user_attributes_with_invalid_name(user_service: UserService):
    user_id = 1
    invalid_name = ""
    with pytest.raises(InvalidUserInputError) as exc_info:
        user_service.change_user_attributes(user_id, new_name=invalid_name)
    assert "名前は空にできません。" in exc_info.value.message


# MockUserRepositoryのテストの拡張

def test_persistence_of_data_in_mock_repository():
    mock_repo = MockUserRepository()
    user_entity = UserEntity.new_entity(
        email="test@example.com",
        password="strongpassword123",
        name="Test User"
    )
    created_user = mock_repo.create(user_entity)
    assert created_user.id is not None
    fetched_user = mock_repo.fetch_by_id(created_user.id)
    assert fetched_user.email == user_entity.email
    fetched_user_by_email = mock_repo.fetch_by_email(Email(user_entity.email))
    assert fetched_user_by_email.id == created_user.id

def test_exception_for_non_existent_user_in_mock_repository():
    mock_repo = MockUserRepository()
    non_existent_user_id = 999
    with pytest.raises(ValueError) as exc_info:
        mock_repo.fetch_by_id(non_existent_user_id)
    assert "User not found" in str(exc_info.value)

def test_exception_for_non_existent_email_in_mock_repository():
    mock_repo = MockUserRepository()
    non_existent_email = Email("non_existent@example.com")
    with pytest.raises(ValueError) as exc_info:
        mock_repo.fetch_by_email(non_existent_email)
    assert "User not found" in str(exc_info.value)
