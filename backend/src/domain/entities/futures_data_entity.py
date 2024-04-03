#src/domain/entities/futures_data_entity.py
from __future__ import annotations
from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from src.infrastructure.database.models import User as UserModel


@dataclass(frozen=True, eq=True)
class FuturesDataEntity(DataClassBase):
    asset_id: int
    asset_name: str
    trade_date: TradeDate
    month: YearMonth
    settle: float
    volume: int
    open_interest: int

    @classmethod
    def new_entity(cls, email: Email, hashed_password: Password, name: Name) -> UserEntity:
        return cls(id=None, email=email, hashed_password=hashed_password, name=name)

    @classmethod
    def from_db(cls, user_db: UserModel) -> UserEntity:
        return cls(
            id=user_db.id,
            email=Email(user_db.email),
            hashed_password=Password(user_db.hashed_password),
            name=Name(user_db.name)
        )

    def change_name(self, new_name: str) -> UserEntity:
        return UserEntity(self.id, self.email, self.hashed_password, Name(new_name))

    def change_email(self, new_email: str) -> UserEntity:
        return UserEntity(self.id, Email(new_email), self.hashed_password, self.name)

    def change_password(self, new_password: str) -> UserEntity:
        return UserEntity(self.id, self.email, Password(new_password), self.name)
