# src/domain/entities/trade_date_entity.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class TradeDateEntity(DataClassBase):
    trade_date: date

    @classmethod
    def from_db_row(cls, row: tuple[date]) -> TradeDateEntity:
        """
        データベースから取得した行データを元に、TradeDateEntityインスタンスを生成します。
        :param row: データベースから取得した行データ。各列はエンティティの属性と一致する必要があります。
        :return: TradeDateEntityインスタンス
        """
        trade_date, = row
        return cls(
            trade_date=trade_date
        )
