from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Address(DataClassBase):
    street: str
    city: str
    zip_code: str
