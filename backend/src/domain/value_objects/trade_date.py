# src/domain/value_objects/trade_date.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import re

from src.domain.helpers.dataclass import DataClassBase

@dataclass(frozen=True, eq=True)
class TradeDate(DataClassBase):
    value: date

    def __post_init__(self):
        if not isinstance(self.value, date): # type: ignore
            raise ValueError("TradeDate must be a date instance.")

    @staticmethod
    def from_string(date_str: str) -> TradeDate:
        """
        文字列形式の日付からTradeDateオブジェクトを作成します。
        日付の形式は 'Friday, 08 Mar 2024' のようになっていることを想定します。
        """
        try:
            # 文字列から日付を抽出し、dateオブジェクトに変換します。
            # この例では 'Friday, 08 Mar 2024' の形式を想定していますが、必要に応じて調整してください。
            match = re.match(r"^\w+, (\d{2}) (\w{3}) (\d{4})$", date_str)
            if match is not None:
                day, month, year = match.groups()
                month_number = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}[month]
                trade_date = date(int(year), month_number, int(day))
                return TradeDate(trade_date)
            else:
                raise ValueError(f"Invalid date format: {date_str}")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date_str}") from e

    def to_date(self) -> date:
        """
        TradeDateオブジェクトをdate型に変換します。
        """
        return self.value

    def to_string(self, format: str = "%Y-%m-%d") -> str:
        """
        TradeDateオブジェクトを指定されたフォーマットの文字列に変換します。
        デフォルトのフォーマットはISO 8601 (YYYY-MM-DD) です。
        """
        return self.value.strftime(format)
