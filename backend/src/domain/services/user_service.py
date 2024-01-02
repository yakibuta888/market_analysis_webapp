
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str):
        # ユーザー作成ロジック
        pass
