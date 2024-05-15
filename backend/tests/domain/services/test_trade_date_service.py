# tests/domain/services/test_trade_date_service.py
import pytest
from unittest.mock import Mock
from datetime import date, timedelta

from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.trade_date_entity import TradeDateEntity
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.services.trade_date_service import TradeDateService

@pytest.fixture
def mock_trade_date_repository():
    return Mock()

@pytest.fixture
def trade_date_service(mock_trade_date_repository: Mock):
    return TradeDateService(trade_date_repository=mock_trade_date_repository)

def test_fetch_trade_dates_successful(trade_date_service: TradeDateService, mock_trade_date_repository: Mock):
    # テストデータの設定
    test_date = date.today()
    mock_trade_date_repository.fetch_trade_dates.return_value = [TradeDateEntity(trade_date=test_date)]

    # テスト実行
    result = trade_date_service.fetch_trade_dates("Gold", test_date, test_date, 0, 10)

    # 検証
    assert len(result) == 1
    assert result[0].trade_date == test_date
    mock_trade_date_repository.fetch_trade_dates.assert_called_once_with("Gold", test_date, test_date, 0, 10)

def test_fetch_trade_dates_invalid_asset_name(trade_date_service: TradeDateService, mock_trade_date_repository: Mock):
    with pytest.raises(InvalidInputError):
        trade_date_service.fetch_trade_dates("", date.today(), date.today(), 0, 10)

    assert not mock_trade_date_repository.fetch_trade_dates.called

def test_fetch_trade_dates_invalid_date_range(trade_date_service: TradeDateService, mock_trade_date_repository: Mock):
    start_date = date.today()
    end_date = start_date - timedelta(days=1)
    with pytest.raises(InvalidInputError):
        trade_date_service.fetch_trade_dates("Gold", start_date, end_date, 0, 10)

    assert not mock_trade_date_repository.fetch_trade_dates.called

def test_fetch_trade_dates_repository_error(trade_date_service: TradeDateService, mock_trade_date_repository: Mock):
    mock_trade_date_repository.fetch_trade_dates.side_effect = SQLAlchemyError("DB Error")
    with pytest.raises(RepositoryError):
        trade_date_service.fetch_trade_dates("Gold", date.today(), date.today(), 0, 10)

    mock_trade_date_repository.fetch_trade_dates.assert_called_once_with("Gold", date.today(), date.today(), 0, 10)
