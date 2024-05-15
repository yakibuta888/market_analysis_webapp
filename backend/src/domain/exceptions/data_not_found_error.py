from .domain_error import DomainError


class DataNotFoundError(DomainError):
    """データが見つからなかった場合のエラー"""
    pass
