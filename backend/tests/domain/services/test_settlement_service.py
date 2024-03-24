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
    is_final = True
    service.save_settlements_from_dataframe(df=settlement_df, asset_id=asset_id, is_final=is_final)

    assert mock_settlement_repository.create.called
    create_call_args = mock_settlement_repository.create.call_args[0][0]
    assert create_call_args.asset_id == asset_id
    assert create_call_args.trade_date == TradeDate(date(2024, 3, 8))
    assert create_call_args.month == YearMonth(2024, 4)
    assert create_call_args.settle == 12.0
    assert create_call_args.is_final == is_final


def test_update_settlements_from_dataframe_success(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock):
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 2
    is_final = False
    service.update_settlements_from_dataframe(df=settlement_df, asset_id=asset_id, is_final=is_final)

    assert mock_settlement_repository.update.called
    update_call_args = mock_settlement_repository.update.call_args[0][0]
    assert update_call_args.asset_id == asset_id
    assert update_call_args.trade_date == TradeDate(date(2024, 3, 8))
    assert update_call_args.month == YearMonth(2024, 4)
    assert update_call_args.settle == 12.0
    assert update_call_args.is_final == is_final


def test_update_settlements_from_dataframe_with_invalid_data(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock):
    settlement_df.at[0, 'trade_date'] = 'Invalid Date'
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 3
    is_final = True

    with pytest.raises(ValueError):
        service.update_settlements_from_dataframe(df=settlement_df, asset_id=asset_id, is_final=is_final)


def test_update_settlements_from_dataframe_repository_exception(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock):
    mock_settlement_repository.update.side_effect = Exception("Update error")
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 4
    is_final = True

    with pytest.raises(Exception) as excinfo:
        service.update_settlements_from_dataframe(df=settlement_df, asset_id=asset_id, is_final=is_final)
    assert "Update error" in str(excinfo.value)


def test_check_data_is_final_or_none_with_valid_date(mock_settlement_repository: MagicMock):
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    mock_settlement_repository.check_data_is_final_or_none.return_value = True

    is_final = service.check_data_is_final(asset_id, trade_date)

    mock_settlement_repository.check_data_is_final_or_none.assert_called_once_with(asset_id, TradeDate(date(2024, 3, 8)))
    assert is_final is True

def test_check_data_is_final_or_none_with_invalid_date(mock_settlement_repository: MagicMock):
    service = SettlementService(settlement_repository=mock_settlement_repository)
    asset_id = 2
    trade_date = "Invalid Date Format"

    with pytest.raises(ValueError) as excinfo:
        service.check_data_is_final(asset_id, trade_date)
    assert "Invalid date format" in str(excinfo.value)
