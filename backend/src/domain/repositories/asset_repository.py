# src/domain/repositories/asset_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.asset_entity import AssetEntity
from src.domain.value_objects.name import Name
from src.infrastructure.database.models import Asset as AssetModel


class AssetRepository(ABC):
    @abstractmethod
    def create(self, asset_entity: AssetEntity) -> AssetModel:
        pass

    @abstractmethod
    def fetch_all(self) -> list[AssetModel]:
        pass

    @abstractmethod
    def fetch_by_name(self, name: Name) -> AssetModel:
        pass

    @abstractmethod
    def exists_by_name(self, name: Name) -> bool:
        pass

    @abstractmethod
    def update(self, asset_entity: AssetEntity) -> AssetModel:
        pass

    @abstractmethod
    def delete(self, name: Name) -> None:
        pass
