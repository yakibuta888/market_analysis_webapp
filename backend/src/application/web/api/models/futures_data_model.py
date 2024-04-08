# src/application/web/api/models/futures_data_model.py

from datetime import datetime, date
from fastapi import Query
from pydantic import BaseModel, validator, Field
from typing import List, Any


class FuturesDataResponse(BaseModel):
    data: List[dict[str, Any]] = Field(default_factory=list, description="取引データのリスト")


class FuturesDataRequest(BaseModel):
    asset_name: str = Field(..., description="資産名", min_length=1)
    trade_dates: List[date] = Field(..., description="取引日（複数指定可）")

    @validator('trade_dates', each_item=True, pre=True)
    def validate_and_convert_trade_dates(cls, value: str):
        try:
            # 文字列形式の取引日をdatetime.dateオブジェクトに変換
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
            if parsed_date > datetime.now().date():
                raise ValueError("取引日は過去または今日でなければなりません。")
            return parsed_date
        except ValueError as e:
            # ValueErrorを捕捉し、カスタムエラーメッセージを発生させる
            raise ValueError(f"trade_dateが無効な日付フォーマットです。YYYY-MM-DD形式である必要があります。: {value}") from e
