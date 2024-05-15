# src/application/web/api/models/trade_date_model.py
from datetime import date
from pydantic import BaseModel, Field, field_validator, ValidationInfo

from src.domain.logics.validate_trade_date import validate_and_convert_trade_date
from src.domain.logics.validate_positive_int_for_api import validate_positive_int


class TradeDateResponse(BaseModel):
    trade_dates: list[date] = Field(default_factory=list, description="List of available trade dates within the specified range.")


class TradeDateRequest(BaseModel):
    graph_type: str = Field(..., description="Type of the graph data.")
    asset_name: str = Field(..., description="Name of the asset.")
    start_date: date | None = Field(None, description="Start date for the date range filter.")
    end_date: date | None = Field(None, description="End date for the date range filter.")
    skip: int = Field(0, ge=0, description="Number of records to skip for pagination.")
    limit: int = Field(100, ge=1, description="Maximum number of records to return.")

    @field_validator('start_date', 'end_date', mode='before')
    def validate_and_convert_dates(cls, value: date | None) -> date | None:
        return validate_and_convert_trade_date(value)

    @field_validator('skip', 'limit', mode='before')
    def validate_positive_integers(cls, value: int, info: ValidationInfo) -> int:
        return validate_positive_int(value, info.field_name or f'{value}')
