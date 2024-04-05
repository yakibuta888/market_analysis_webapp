# src/domain/value_objects/year_month.py
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
        """文字列 'APR 24' または 'APR 2024' を YearMonth オブジェクトに変換する"""
        month_str = month_str.strip().upper()

        # 不正な省略形を修正
        month_str = month_str.replace("JLY", "JUL")

        # 入力値の検証
        parts = month_str.split(" ")
        if len(parts) != 2 or not parts[0].isalpha() or not parts[1].isdigit():
            raise ValueError(f"Invalid month format: {month_str}")

        # 年のフォーマットを調整
        format_str = "%b %Y" if len(parts[1]) == 4 else "%b %y"

        try:
            parsed_date = datetime.strptime(month_str, format_str)
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

    def to_datetime(self) -> datetime:
        """
        YearMonth オブジェクトを datetime オブジェクトに変換する。
        変換される datetime オブジェクトは、指定された年月の最初の日 (1日) を表す。
        """
        return datetime(self.year, self.month, 1)
