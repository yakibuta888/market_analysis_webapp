from .domain_error import DomainError


class InvalidInputError(DomainError):
    """カスタム例外クラス: 無効な入力に対するエラー"""
    pass
