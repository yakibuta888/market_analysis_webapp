# src/domain/repositories/volume_oi_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.value_objects.trade_date import TradeDate
from src.infrastructure.database.models import VolumeOI as VolumeOIModel


class VolumeOIRepository(ABC):
    @abstractmethod
    def create(self, volume_oi_entity: VolumeOIEntity) -> VolumeOIModel:
        raise NotImplementedError

    def update(self, volume_oi_entity: VolumeOIEntity) -> VolumeOIModel:
        raise NotImplementedError

    def check_data_is_final_or_none(self, asset_id: int, trade_date: TradeDate) -> bool | None:
        raise NotImplementedError
