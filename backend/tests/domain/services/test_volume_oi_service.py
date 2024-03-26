# tests/domain/services/test_volume_oi_service.py
import pandas as pd
import pytest
from unittest.mock import Mock, call

from src.domain.services.volume_oi_service import VolumeOIService
from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from datetime import date

@pytest.fixture
def mock_volume_oi_repository():
    # VolumeOIRepositoryのモックを作成
    return Mock()

@pytest.fixture
def volume_oi_df():
    # テスト用のDataFrameを作成
    data = {
        'month': ['APR 24'],
        'globex': ["1,500"],
        'open_outcry': ["0"],
        'clear_port': ["25"],
        'total_volume': ["17,275"],
        'block_trades': ["10"],
        'efp': ["5"],
        'efr': ["0"],
        'tas': ["3"],
        'deliveries': ["1"],
        'at_close': ["2,150"],
        'change': ["+1,020"],
    }
    return pd.DataFrame(data)


def test_save_volume_oi_from_dataframe(mock_volume_oi_repository: Mock, volume_oi_df: pd.DataFrame):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    is_final = True
    service.save_volume_oi_from_dataframe(asset_id, trade_date, volume_oi_df, is_final)

    # 確認：createメソッドが適切なエンティティで呼び出されているか
    expected_call = call(VolumeOIEntity(
        id=None,
        asset_id=asset_id,
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        globex=1500,
        open_outcry=0,
        clear_port=25,
        total_volume=17275,
        block_trades=10,
        efp=5,
        efr=0,
        tas=3,
        deliveries=1,
        at_close=2150,
        change=1020,
        is_final=is_final
    ))
    mock_volume_oi_repository.create.assert_has_calls([expected_call])


def test_save_volume_oi_from_dataframe_with_error(mock_volume_oi_repository: Mock, volume_oi_df: pd.DataFrame):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    is_final = True
    # mock_volume_oi_repository.create.side_effect = Exception("Save error")
    invalid_df = volume_oi_df.copy()
    invalid_df['month'] = 'invalid month'

    # エラーが発生した場合、適切に処理されるかテスト
    with pytest.raises(ValueError) as excinfo:
        service.save_volume_oi_from_dataframe(asset_id, trade_date, invalid_df, is_final)
    assert "Invalid month format" in str(excinfo.value)


def test_save_volume_oi_from_dataframe_with_error_negative_close(mock_volume_oi_repository: Mock, volume_oi_df: pd.DataFrame):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    is_final = True
    # mock_volume_oi_repository.create.side_effect = Exception("Save error")
    invalid_df = volume_oi_df.copy()
    invalid_df['at_close'] = '-100'

    # エラーが発生した場合、適切に処理されるかテスト
    with pytest.raises(ValueError) as excinfo:
        service.save_volume_oi_from_dataframe(asset_id, trade_date, invalid_df, is_final)
    assert "must be greater than or equal to 0" in str(excinfo.value)


def test_update_volume_oi_from_dataframe_success(volume_oi_df: pd.DataFrame, mock_volume_oi_repository: Mock):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 2
    trade_date = "Friday, 08 Mar 2024"
    is_final = False
    service.update_volume_oi_from_dataframe(asset_id, trade_date, volume_oi_df, is_final)

    expected_call = call(VolumeOIEntity(
        id=None,
        asset_id=asset_id,
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        globex=1500,
        open_outcry=0,
        clear_port=25,
        total_volume=17275,
        block_trades=10,
        efp=5,
        efr=0,
        tas=3,
        deliveries=1,
        at_close=2150,
        change=1020,
        is_final=is_final
    ))
    mock_volume_oi_repository.update.assert_has_calls([expected_call])


def test_update_volume_oi_from_dataframe_with_invalid_data(volume_oi_df: pd.DataFrame, mock_volume_oi_repository: Mock):
    volume_oi_df.at[0, 'month'] = 'Invalid month'
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 3
    trade_date = "Friday, 08 Mar 2024"
    is_final = True

    with pytest.raises(ValueError):
        service.update_volume_oi_from_dataframe(asset_id, trade_date, volume_oi_df, is_final)


def test_update_volume_oi_from_dataframe_repository_exception(volume_oi_df: pd.DataFrame, mock_volume_oi_repository: Mock):
    mock_volume_oi_repository.update.side_effect = Exception("Update error")
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 4
    trade_date = "Friday, 08 Mar 2024"
    is_final = True

    with pytest.raises(Exception) as excinfo:
        service.update_volume_oi_from_dataframe(asset_id, trade_date, volume_oi_df, is_final)
    assert "Update error" in str(excinfo.value)


def test_check_data_is_final_or_none_with_valid_date(mock_volume_oi_repository: Mock):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    trade_date = "Fridey, 08 Mar 2024"
    mock_volume_oi_repository.check_data_is_final_or_none.return_value = True

    is_final = service.check_data_is_final(asset_id, trade_date)

    mock_volume_oi_repository.check_data_is_final_or_none.assert_called_once_with(asset_id, TradeDate(date(2024, 3, 8)))
    assert is_final is True


def test_check_data_is_final_or_none_with_invalid_date(mock_volume_oi_repository: Mock):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 2
    trade_date = "Invalid Date"

    with pytest.raises(ValueError) as excinfo:
        service.check_data_is_final(asset_id, trade_date)
    assert "Invalid date format" in str(excinfo.value)
