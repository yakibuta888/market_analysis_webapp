# src/domain/entities/settlement_entity.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.domain.helpers.dataclass import DataClassBase
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth


@dataclass(frozen=True, eq=True)
class SettlementEntity(DataClassBase):
    id: int | None
    asset_id: int
    trade_date: TradeDate
    month: YearMonth
    open: str | None
    high: str | None
    low: str | None
    last: str | None
    change: float | None
    settle: float
    est_volume: int
    prior_day_oi: int

    def __post_init__(self):
        self._validate_volume(self.est_volume)
        self._validate_oi(self.prior_day_oi)

    @staticmethod
    def _validate_volume(est_volume: int) -> None:
        if est_volume < 0:
            raise ValueError("Volume must be greater than or equal to 0.")

    @staticmethod
    def _validate_oi(prior_day_oi: int) -> None:
        if prior_day_oi < 0:
            raise ValueError("OI must be greater than or equal to 0.")

    @classmethod
    def new_entity_by_scraping(cls, asset_id: int, trade_date: str, month: str, open: str | None, high: str | None, low: str | None, last: str | None, change: str | None, settle: str, est_volume: str, prior_day_oi: str) -> SettlementEntity:
        return cls(
            id=None,
            asset_id=asset_id,
            trade_date=TradeDate.from_string(trade_date),
            month=YearMonth.from_string(month),
            open=open,
            high=high,
            low=low,
            last=last,
            change=float(change) if change else None,
            settle=float(settle),
            est_volume=int(est_volume),
            prior_day_oi=int(prior_day_oi))

    @classmethod
    def from_db(cls, asset_id: int, trade_date: date, month: str, open: str | None, high: str | None, low: str | None, last: str | None, change: float | None, settle: float, est_volume: int, prior_day_oi: int) -> SettlementEntity:
        return cls(
            id=None,
            asset_id=asset_id,
            trade_date=TradeDate(trade_date),
            month=YearMonth.from_db_format(month),
            open=open,
            high=high,
            low=low,
            last=last,
            change=change,
            settle=settle,
            est_volume=est_volume,
            prior_day_oi=prior_day_oi)
