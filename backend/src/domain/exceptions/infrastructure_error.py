class InfrastructureError(Exception):
    """インフラストラクチャー層のエラーの基底クラス"""

    def __init__(self, message: str) -> None:
        """コンストラクタ

        Args:
            message (str): エラーメッセージ
        """
        self.message = message
        super().__init__(message)
