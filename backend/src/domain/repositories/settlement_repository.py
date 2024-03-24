# src/domain/repositories/settlement_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.value_objects.trade_date import TradeDate
from src.infrastructure.database.models import Settlement as SettlementModel


class SettlementRepository(ABC):
    @abstractmethod
    def create(self, settlement_entity: SettlementEntity) -> SettlementModel:
        raise NotImplementedError

    def update(self, settlement_entity: SettlementEntity) -> SettlementModel:
        raise NotImplementedError

    def check_data_is_final_or_none(self, asset_id: int, trade_date: TradeDate) -> bool | None:
        raise NotImplementedError
