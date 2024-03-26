from .infrastructure_error import InfrastructureError


class ElementNotFoundError(InfrastructureError):
    """要素が見つからなかった場合のエラー"""
    pass
