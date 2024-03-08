# src/domain/value_objects/name.py
from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Name(DataClassBase):
    name: str

    def __post_init__(self):
        self._validate_name(self.name)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name:
            raise ValueError("名前は空にできません。")
        if len(name) > 64:
            raise ValueError("名前は64文字以内である必要があります。")

    def to_primitive(self) -> str:
        return self.name
