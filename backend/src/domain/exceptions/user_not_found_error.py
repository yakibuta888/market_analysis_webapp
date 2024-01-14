from .domain_error import DomainError


class UserNotFoundError(DomainError):
    """ユーザーが見つからなかった場合のエラー"""
    pass
