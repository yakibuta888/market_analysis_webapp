# src/domain/repositories/settlement_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.settlement_entity import SettlementEntity
from src.infrastructure.database.models import Settlement as SettlementModel


class SettlementRepository(ABC):
    @abstractmethod
    def create(self, settlement_entity: SettlementEntity) -> SettlementModel:
        pass
