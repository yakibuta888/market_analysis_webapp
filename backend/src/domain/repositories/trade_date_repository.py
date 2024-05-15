#src/domain/repositories/trade_date_repository.py
from abc import ABC, abstractmethod
from datetime import date

from src.domain.entities.trade_date_entity import TradeDateEntity

class TradeDateRepository(ABC):
    @abstractmethod
    def fetch_trade_dates(self, asset_name: str, start_date: date | None, end_date: date | None, skip: int, limit: int) -> list[TradeDateEntity]:
        pass
