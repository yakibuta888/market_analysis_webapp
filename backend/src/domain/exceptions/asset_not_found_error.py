from .domain_error import DomainError


class AssetNotFoundError(DomainError):
    """資産名が見つからなかった場合のエラー"""
    pass
