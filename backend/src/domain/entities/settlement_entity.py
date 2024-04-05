# src/domain/entities/settlement_entity.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.domain.helpers.dataclass import DataClassBase
from src.domain.logics.validate_price_format import validate_price_format
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from src.infrastructure.database.models import Settlement as SettlementModel


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
    change: str | None
    settle: str | None
    est_volume: int
    prior_day_oi: int
    is_final: bool

    def __post_init__(self):
        self._validate_volume(self.est_volume)
        self._validate_oi(self.prior_day_oi)
        self._validate_price_format()

    @staticmethod
    def _validate_volume(est_volume: int) -> None:
        if est_volume < 0:
            raise ValueError("Volume must be greater than or equal to 0.")

    @staticmethod
    def _validate_oi(prior_day_oi: int) -> None:
        if prior_day_oi < 0:
            raise ValueError("OI must be greater than or equal to 0.")

    def _validate_price_format(self):
        # 価格関連の属性が適切なフォーマットであるか検証
        for field in ['open', 'high', 'low', 'last', 'change', 'settle']:
            value = getattr(self, field)
            if value is not None and not validate_price_format(value):
                raise ValueError(f"Invalid price format for {field}: {value}")

    @classmethod
    def new_entity_by_scraping(cls, asset_id: int, trade_date: str, month: str, open: str, high: str, low: str, last: str, change: str, settle: str, est_volume: str, prior_day_oi: str, is_final: bool) -> SettlementEntity:
        return cls(
            id=None,
            asset_id=asset_id,
            trade_date=TradeDate.from_string(trade_date),
            month=YearMonth.from_string(month),
            open=open,
            high=high,
            low=low,
            last=last,
            change=change,
            settle=settle,
            est_volume=int(est_volume.replace(",", "")),
            prior_day_oi=int(prior_day_oi.replace(",", "")),
            is_final=is_final
        )

    @classmethod
    def from_db(cls, db_row: SettlementModel) -> SettlementEntity:
        return cls(
            id=db_row.id,
            asset_id=db_row.asset_id,
            trade_date=TradeDate(db_row.trade_date),
            month=YearMonth.from_db_format(db_row.month),
            open=db_row.open,
            high=db_row.high,
            low=db_row.low,
            last=db_row.last,
            change=db_row.change,
            settle=db_row.settle,
            est_volume=db_row.est_volume,
            prior_day_oi=db_row.prior_day_oi,
            is_final=db_row.is_final
        )
