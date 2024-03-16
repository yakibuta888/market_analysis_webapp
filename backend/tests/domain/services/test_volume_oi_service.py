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
        'trade_date': ['Friday, 08 Mar 2024'],
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

    service.save_volume_oi_from_dataframe(volume_oi_df, asset_id)

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
        change=1020
    ))
    mock_volume_oi_repository.create.assert_has_calls([expected_call])

def test_save_volume_oi_from_dataframe_with_error(mock_volume_oi_repository: Mock, volume_oi_df: pd.DataFrame):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    # mock_volume_oi_repository.create.side_effect = Exception("Save error")
    invalid_df = volume_oi_df.copy()
    invalid_df['trade_date'] = 'invalid date'

    # エラーが発生した場合、適切に処理されるかテスト
    with pytest.raises(ValueError) as excinfo:
        service.save_volume_oi_from_dataframe(invalid_df, asset_id)
    assert "Invalid date format" in str(excinfo.value)

def test_save_volume_oi_from_dataframe_with_error_negative_close(mock_volume_oi_repository: Mock, volume_oi_df: pd.DataFrame):
    service = VolumeOIService(mock_volume_oi_repository)
    asset_id = 1
    # mock_volume_oi_repository.create.side_effect = Exception("Save error")
    invalid_df = volume_oi_df.copy()
    invalid_df['at_close'] = '-100'

    # エラーが発生した場合、適切に処理されるかテスト
    with pytest.raises(ValueError) as excinfo:
        service.save_volume_oi_from_dataframe(invalid_df, asset_id)
    assert "must be greater than or equal to 0" in str(excinfo.value)
