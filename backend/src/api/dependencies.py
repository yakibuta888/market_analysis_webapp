
from ..infrastructure.repositories.user_repository import UserRepository
from ..domain.services.user_service import UserService

def get_user_repository():
    # 依存性としてユーザーリポジトリを提供する
    return UserRepository()

def get_user_service():
    # 依存性としてユーザーサービスを提供する
    repository = get_user_repository()
    return UserService(repository)
