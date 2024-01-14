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

    def to_primitive(self) -> str:
        return self.name
