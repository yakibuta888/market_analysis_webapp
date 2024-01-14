from .domain_error import DomainError


class InvalidUserInputError(DomainError):
    """ユーザーの入力が無効な場合のエラー"""
    pass
