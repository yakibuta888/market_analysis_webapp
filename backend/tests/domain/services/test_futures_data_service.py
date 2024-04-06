# tests/domain/services/test_futures_data_service.py
import pytest
from datetime import date, datetime
import pandas as pd

from src.domain.entities.futures_data_entity import FuturesDataEntity
from src.domain.exceptions.dataframe_validation_error import DataFrameValidationError
from src.domain.services.futures_data_service import FuturesDataService, InvalidInputError, RepositoryError
from src.domain.repositories.futures_data_repository import FuturesDataRepository
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_futures_data_repository():
    mock_repo = MagicMock()
    mock_entities = [
        FuturesDataEntity(
            asset_id=1,
            asset_name="TestAsset",
            trade_date=TradeDate(date(2024, 3, 8)),
            month=YearMonth(2024, 4),
            settle=1234.56,
            volume=1000,
            open_interest=2000
        ),
        FuturesDataEntity(
            asset_id=1,
            asset_name="TestAsset",
            trade_date=TradeDate(date(2024, 3, 8)),
            month=YearMonth(2024, 5),
            settle=1230.00,
            volume=950,
            open_interest=1950
        )
    ]
    mock_repo.fetch_by_asset_and_date.return_value = mock_entities
    return mock_repo


@pytest.fixture
def mock_service():
    return FuturesDataService(futures_data_repository=MagicMock(spec=FuturesDataRepository))


# 正常な動作のテスト
def test_make_dataframe_success(mock_futures_data_repository: MagicMock):
    service = FuturesDataService(futures_data_repository=mock_futures_data_repository)
    df = service.make_dataframe("TestAsset", date(2024, 3, 8))

    # DataFrameが空でないことを確認
    assert not df.empty

    # DataFrameの行数を検証
    assert len(df) == 2

    # 具体的な値で検証
    expected_df = pd.DataFrame({
        'month': [datetime(2024, 4, 1), datetime(2024, 5, 1)],
        'settle': [1234.56, 1230.00],
        'volume': [1000, 950],
        'open_interest': [2000, 1950]
    })

    pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df.reset_index(drop=True))


# 無効な入力値に対するテスト
@pytest.mark.parametrize("asset_name,trade_date", [
    (None, date(2024, 3, 8)),  # 資産名がNone
    ("TestAsset", None),  # 取引日がNone
    ("", date(2024, 3, 8)),  # 資産名が空文字
    ("TestAsset", ""),  # 取引日が空文字（不適切な型）
])
def test_make_dataframe_invalid_input(asset_name: str, trade_date: date):
    service = FuturesDataService(futures_data_repository=MagicMock(spec=FuturesDataRepository))

    with pytest.raises(InvalidInputError):
        service.make_dataframe(asset_name=asset_name, trade_date=trade_date)


# リポジトリからのエラーをテスト
@patch("src.domain.services.futures_data_service.FuturesDataService.make_dataframe")
def test_make_dataframe_repository_error(mock_make_dataframe: MagicMock):
    mock_make_dataframe.side_effect = RepositoryError("データベース操作中にエラーが発生しました。")
    service = FuturesDataService(futures_data_repository=MagicMock(spec=FuturesDataRepository))

    with pytest.raises(RepositoryError):
        service.make_dataframe(asset_name="TestAsset", trade_date=date(2024, 3, 8))


# 正常な入力に対するテスト
def test_add_settlement_spread_normal(mock_service: FuturesDataService):
    df = pd.DataFrame({
        'month': pd.to_datetime(['2021-01', '2021-02', '2021-03']),
        'settle': [100, 105, 102],
    })
    expected_spread = [0, 5, -3]  # 期待されるスプレッドの値
    result_df = mock_service.add_settlement_spread(df)
    assert all(result_df['settle_spread'] == expected_spread), "スプレッドが正しく計算されていません。"


# 空のDataFrameに対するテスト
def test_add_settlement_spread_empty_df(mock_service: FuturesDataService):
    df = pd.DataFrame()
    with pytest.raises(DataFrameValidationError):
        mock_service.add_settlement_spread(df)


# 必要なカラムが不足している場合のテスト
def test_add_settlement_spread_missing_columns(mock_service: FuturesDataService):
    df = pd.DataFrame({
        'month': pd.to_datetime(['2021-01', '2021-02']),
        # 'settle' カラムが欠けている
    })
    with pytest.raises(DataFrameValidationError):
        mock_service.add_settlement_spread(df)


# `month`カラムのデータ型が不正な場合のテスト
def test_add_settlement_spread_invalid_month_type(mock_service: FuturesDataService):
    df = pd.DataFrame({
        'month': ['2021-01', '2021-02'],  # 日付型でない
        'settle': [100, 105],
    })
    # ここではTypeErrorを想定していますが、実際のエラーハンドリングに応じて変更してください。
    with pytest.raises(DataFrameValidationError):
        mock_service.add_settlement_spread(df)
