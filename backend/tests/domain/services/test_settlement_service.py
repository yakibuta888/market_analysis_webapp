# tests/domain/services/test_settlement_service.py
import pandas as pd
import pytest
from unittest.mock import MagicMock
from src.domain.services.settlement_service import SettlementService
from src.domain.repositories.settlement_repository import SettlementRepository
from src.infrastructure.repositories.settlement_repository_mysql import SettlementRepositoryMysql

@pytest.fixture
def mock_settlement_repository() -> SettlementRepository:
    return MagicMock(spec=SettlementRepositoryMysql)

@pytest.fixture
def settlement_df():
    data = {
        'trade_date': ['2024-03-08'],
        'month': ['2024-04'],
        'open': [10.0],
        'high': [15.0],
        'low': [8.0],
        'last': [12.0],
        'change': [2.0],
        'settle': [12.0],
        'est_volume': [100],
        'prior_day_oi': [200]
    }
    return pd.DataFrame(data)

def test_save_settlements_from_dataframe(settlement_df, mock_settlement_repository):
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 1
    service.save_settlements_from_dataframe(df=settlement_df, asset_id=asset_id)

    assert mock_settlement_repository.create.called
    create_call_args = mock_settlement_repository.create.call_args[0][0]
    assert create_call_args.asset_id == asset_id
    assert create_call_args.trade_date == '2024-03-08'
    assert create_call_args.month == '2024-04'
