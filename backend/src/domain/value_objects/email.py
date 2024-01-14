from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Email(DataClassBase):
    email: str

    def __post_init__(self):
        self._validate_email(self.email)

    @staticmethod
    def _validate_email(email: str) -> None:
        if "@" not in email:
            raise ValueError("無効なメールアドレスです。")

    def to_primitive(self) -> str:
        return self.email
