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
    user_repository.create(UserEntity(
        id=1,
        email=Email("existing@example.com"),
        hashed_password=Password.create("strongpassword123"),
        name=Name("Existing User")
    ))
    return UserService(user_repository)

def test_create_user(user_service: UserService):
    email, password, name = "test@example.com", "strongpassword123", "Test User"
    user_entity = user_service.create_user(email, password, name)

    assert user_entity.email.email == email
    assert user_entity.name.name == name
    # ここでは、パスワードのハッシュ値のみを確認します（平文のパスワードは返されません）
    assert user_entity.hashed_password.hashed_password is not None

def test_fetch_user_by_id(user_service: UserService):
    user_id = 1
    user_entity = user_service.fetch_user_by_id(user_id)

    assert user_entity is not None
    assert user_entity.id == user_id

# TODO
def test_fetch_user_by_email(user_service: UserService):
    pass

def test_change_user_attributes(user_service: UserService):
    user_id = 1
    new_email, new_password, new_name = "new@example.com", "newpassword123", "New Name"
    updated_user = user_service.change_user_attributes(user_id, new_email, new_password, new_name)

    assert updated_user.email.email == new_email
    assert updated_user.name.name == new_name
    # 新しいパスワードのハッシュが更新されたことを確認
    assert updated_user.hashed_password.hashed_password is not None

def test_user_creation_and_retrieval(user_service: UserService):
    email, password, name = "test@example.com", "strongpassword123", "Test User"
    created_user = user_service.create_user(email, password, name)

    # ユーザーが作成されていることを確認
    assert created_user is not None
    assert created_user.email.email == email
    assert created_user.name.name == name

    # 同じユーザーがfetch_by_idで取得できることを確認
    assert created_user.id is not None
    fetched_user = user_service.fetch_user_by_id(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.email.email == email
    assert fetched_user.name.name == name

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

# MockUserRepositoryのテストの拡張

def test_persistence_of_data_in_mock_repository():
    mock_repo = MockUserRepository()
    user_entity = UserEntity(
        id=None,
        email=Email("test@example.com"),
        hashed_password=Password.create("strongpassword123"),
        name=Name("Test User")
    )
    created_user = mock_repo.create(user_entity)
    assert created_user.id is not None
    fetched_user = mock_repo.fetch_by_id(created_user.id)
    assert fetched_user.email == user_entity.email.email

def test_exception_for_non_existent_user_in_mock_repository():
    mock_repo = MockUserRepository()
    non_existent_user_id = 999
    with pytest.raises(ValueError) as exc_info:
        mock_repo.fetch_by_id(non_existent_user_id)
    assert "User not found" in str(exc_info.value)
