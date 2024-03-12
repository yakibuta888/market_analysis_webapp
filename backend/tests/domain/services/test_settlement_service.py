# tests/domain/services/test_settlement_service.py
import pandas as pd
import pytest
from datetime import date
from unittest.mock import MagicMock

from src.domain.services.settlement_service import SettlementService
from src.domain.repositories.settlement_repository import SettlementRepository
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth


@pytest.fixture
def mock_settlement_repository() -> SettlementRepository:
    return MagicMock(spec=SettlementRepository)

@pytest.fixture
def settlement_df():
    data = {
        'trade_date': ['Friday, 08 Mar 2024'],
        'month': ['APR 24'],
        'open': ["10.0"],
        'high': ["15.0"],
        'low': ["8.0A"],
        'last': ["12.0B"],
        'change': ["-.25"],
        'settle': ["12.0"],
        'est_volume': ["2,100"],
        'prior_day_oi': ["200"]
    }
    return pd.DataFrame(data)

def test_save_settlements_from_dataframe(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock):
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 1
    service.save_settlements_from_dataframe(df=settlement_df, asset_id=asset_id)

    assert mock_settlement_repository.create.called
    create_call_args = mock_settlement_repository.create.call_args[0][0]
    assert create_call_args.asset_id == asset_id
    assert create_call_args.trade_date == TradeDate(date(2024, 3, 8))
    assert create_call_args.month == YearMonth(2024, 4)
