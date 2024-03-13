# src/domain/repositories/volume_oi_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.infrastructure.database.models import VolumeOI as VolumeOIModel


class VolumeOIRepository(ABC):
    @abstractmethod
    def create(self, volume_oi_entity: VolumeOIEntity) -> VolumeOIModel:
        pass
