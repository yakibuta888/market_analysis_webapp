# src/domain/value_objects/password.py

import bcrypt
from dataclasses import dataclass, field

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Password(DataClassBase):
    _hashed_password: str = field(repr=False)

    def __init__(self, hashed_password: str):
        # 外部から直接インスタンス化できないように例外を投げる
        raise NotImplementedError("Password value object must be created through 'create' or 'from_db' methods")

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    @staticmethod
    def _validate_password(password: str) -> None:
        # ここにパスワードの強度を検証するロジックを追加
        if len(password) < 8:
            raise ValueError("パスワードは8文字以上である必要があります。")
        # 他のバリデーションルールを追加

    @classmethod
    def _internal_create(cls, hashed_password: str):
        obj = object.__new__(cls)
        object.__setattr__(obj, '_hashed_password', hashed_password)
        return obj

    @classmethod
    def create(cls, plain_password: str):
        cls._validate_password(plain_password)
        hashed_password = cls._hash_password(plain_password)
        return cls._internal_create(hashed_password)

    @classmethod
    def from_db(cls, hashed_password: str):
        return cls._internal_create(hashed_password)
