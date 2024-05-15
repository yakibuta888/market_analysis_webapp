# src/application/web/api/models/futures_data_model.py
from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel, field_validator, Field
from typing import Any

from src.domain.logics.validate_trade_date import validate_and_convert_trade_date
from src.settings import logger


class FuturesDataResponse(BaseModel):
    data: list[dict[str, Any]] = Field(default_factory=list, description="取引データのリスト")


class FuturesDataRequest(BaseModel):
    asset_name: str = Field(..., description="資産名", min_length=1)
    trade_dates: list[date] = Field(..., description="取引日（複数指定可）")


    @field_validator('trade_dates', mode='before')
    def validate_and_convert_trade_dates(cls, values: list[str] | list[date]) -> list[date]:
        result: list[date] = []
        for value in values:
            date_value = validate_and_convert_trade_date(value)
            if date_value is None:
                raise ValueError(f"Invalid date value: {value}")
            result.append(date_value)
        return result
