from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from src.domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class YearMonth(DataClassBase):
    year: int
    month: int

    @staticmethod
    def from_string(month_str: str) -> YearMonth:
        """文字列 'APR 24' を YearMonth オブジェクトに変換する"""
        month_str = month_str.strip().upper()
        try:
            parsed_date = datetime.strptime(month_str, "%b %y")
            return YearMonth(year=parsed_date.year, month=parsed_date.month)
        except ValueError as e:
            raise ValueError(f"Invalid month format: {month_str}") from e

    def to_db_format(self) -> str:
        """DBに保存するための文字列形式 'YYYY-MM' に変換する"""
        return f"{self.year}-{str(self.month).zfill(2)}"

    def __str__(self) -> str:
        """人が読みやすい形式 'YYYY-MM' で返す"""
        return self.to_db_format()

    @classmethod
    def from_db_format(cls, ym_str: str) -> YearMonth:
        """
        "YYYY-MM" 形式の文字列から YearMonth オブジェクトを生成する。
        """
        year, month = map(int, ym_str.split('-'))
        return cls(year, month)
