from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository


class MockUserService(UserService):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        # モックの設定（例：固定のユーザーデータを返すようにする）
