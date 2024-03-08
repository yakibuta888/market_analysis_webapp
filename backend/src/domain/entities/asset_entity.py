# src/domain/entities/asset_entity.py
from __future__ import annotations
from dataclasses import dataclass

from src.domain.helpers.dataclass import DataClassBase
from src.domain.value_objects.name import Name
from src.infrastructure.database.models import Asset as AssetModel

@dataclass(frozen=True, eq=True)
class AssetEntity(DataClassBase):
    id: int | None
    name: Name

    @classmethod
    def new_entity(cls, name: Name) -> AssetEntity:
        return cls(id=None, name=name)

    @classmethod
    def from_db(cls, asset_db: AssetModel) -> AssetEntity:
        return cls(
            id=asset_db.id,
            name=Name(asset_db.name)
        )

# TODO: 未実装
    def change_name(self, new_name: str) -> AssetEntity:
        return AssetEntity(self.id, Name(new_name))
