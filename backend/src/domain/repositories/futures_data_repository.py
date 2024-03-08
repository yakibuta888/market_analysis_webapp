from abc import ABC, abstractmethod
from datetime import date

from src.domain.entities.futures_data_entity import FuturesDataEntity


class FuturesDataRepository(ABC):
    @abstractmethod
    def fetch_by_asset_and_date(self, asset_name: str, trade_date: date) -> list[FuturesDataEntity]:
        pass
