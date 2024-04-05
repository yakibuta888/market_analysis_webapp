#src/domain/entities/futures_data_entity.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.domain.helpers.dataclass import DataClassBase
from src.domain.logics.convert_price_format import convert_price_format
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth


@dataclass(frozen=True, eq=True)
class FuturesDataEntity(DataClassBase):
    asset_id: int
    asset_name: str
    trade_date: TradeDate
    month: YearMonth
    settle: float | None
    volume: int
    open_interest: int


    @classmethod
    def from_db_row(cls, row: tuple[int, str, date, str, str, int, int]) -> FuturesDataEntity:
        """
        データベースから取得した行データを元に、FuturesDataEntityインスタンスを生成します。
        :param row: データベースから取得した行データ。各列はエンティティの属性と一致する必要があります。
        :return: FuturesDataEntityインスタンス
        """
        asset_id, asset_name, trade_date, month, settle, volume, open_interest = row
        return cls(
            asset_id=asset_id,
            asset_name=asset_name,
            trade_date=TradeDate(trade_date),
            month=YearMonth.from_db_format(month),
            settle=convert_price_format(settle),
            volume=volume,
            open_interest=open_interest
        )
