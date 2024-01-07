import bcrypt
from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase

@dataclass(frozen=True, eq=True)
class Password(DataClassBase):
    hashed_password: str

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    @classmethod
    def create(cls, plain_password: str):
        cls._validate_password(plain_password)
        hashed_password = cls.hash_password(plain_password)
        return cls(hashed_password=hashed_password)

    @staticmethod
    def _validate_password(password: str) -> None:
        # ここにパスワードの強度を検証するロジックを追加
        if len(password) < 8:
            raise ValueError("パスワードは8文字以上である必要があります。")
        # 他のバリデーションルールを追加
