#src/domain/entities/user_entity.py
from __future__ import annotations
from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase
from src.domain.value_objects.name import Name
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.database.models import User as UserModel


@dataclass(frozen=True, eq=True)
class UserEntity(DataClassBase):
    id: int | None
    _email: Email
    _hashed_password: Password
    _name: Name

    @property
    def email(self) -> str:
        return self._email.email

    @property
    def hashed_password(self) -> str:
        return self._hashed_password.hashed_password

    @property
    def name(self) -> str:
        return self._name.name

    @classmethod
    def new_entity(cls, email: str, hashed_password: str, name: str) -> UserEntity:
        try:
            email_vo=Email(email)
            hashed_password_vo=Password.create(hashed_password)
            name_vo=Name(name)
            return cls(id=None, _email=email_vo, _hashed_password=hashed_password_vo, _name=name_vo)
        except ValueError as e:
            raise e
        except NotImplementedError as e:
            raise e

    @classmethod
    def from_db(cls, user_db: UserModel) -> UserEntity:
        return cls(
            id=user_db.id,
            _email=Email(str(user_db.email)),
            _hashed_password=Password.from_db(str(user_db.hashed_password)),
            _name=Name(str(user_db.name))
        )

    def change_name(self, new_name: str) -> UserEntity:
        return UserEntity(self.id, self._email, self._hashed_password, Name(new_name))

    def change_email(self, new_email: str) -> UserEntity:
        return UserEntity(self.id, Email(new_email), self._hashed_password, self._name)

    def change_password(self, new_password: str) -> UserEntity:
        return UserEntity(self.id, self._email, Password.create(new_password), self._name)
