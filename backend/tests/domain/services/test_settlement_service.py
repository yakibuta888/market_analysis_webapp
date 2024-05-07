# tests/domain/services/test_settlement_service.py
import pandas as pd
import pytest
from datetime import date, datetime
from unittest.mock import MagicMock

from src.domain.entities.settlement_entity import SettlementEntity
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


@pytest.fixture
def settlement_service(mock_settlement_repository: MagicMock):
    return SettlementService(settlement_repository=mock_settlement_repository)


def test_save_settlements_from_dataframe(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)
    settlement_service.save_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)

    assert mock_settlement_repository.create.called
    create_call_args = mock_settlement_repository.create.call_args[0][0]
    assert create_call_args.asset_id == asset_id
    assert create_call_args.trade_date == TradeDate(date(2024, 3, 8))
    assert create_call_args.month == YearMonth(2024, 4)
    assert create_call_args.settle == "12.0"
    assert create_call_args.last_updated == last_updated


def test_update_settlements_from_dataframe_success(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    asset_id = 2
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 6, 12, 0, 0)
    settlement_service.update_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)

    assert mock_settlement_repository.update.called
    update_call_args = mock_settlement_repository.update.call_args[0][0]
    assert update_call_args.asset_id == asset_id
    assert update_call_args.trade_date == TradeDate(date(2024, 3, 8))
    assert update_call_args.month == YearMonth(2024, 4)
    assert update_call_args.settle == "12.0"
    assert update_call_args.last_updated == last_updated


def test_update_settlements_from_dataframe_with_invalid_data(settlement_df: pd.DataFrame, settlement_service: SettlementService):
    settlement_df.at[0, 'month'] = "Invalid Month"
    asset_id = 3
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)

    with pytest.raises(ValueError) as excinfo:
        settlement_service.update_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)
    assert "Invalid month format" in str(excinfo.value)


def test_update_settlements_from_dataframe_repository_exception(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    mock_settlement_repository.update.side_effect = Exception("Update error")
    asset_id = 4
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)

    with pytest.raises(Exception) as excinfo:
        settlement_service.update_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)
    assert "Update error" in str(excinfo.value)


def test_check_data_is_latest_or_not_exsist_with_latest_date(mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)
    mock_settlement_repository.check_last_updated_or_none.return_value = datetime(2024, 3, 7, 12, 0, 0)

    is_latest_or_none = settlement_service.check_data_is_latest_or_not_exsist(asset_id, trade_date, last_updated)

    mock_settlement_repository.check_last_updated_or_none.assert_called_once_with(asset_id, TradeDate(date(2024, 3, 8)))
    assert is_latest_or_none is True


def test_check_data_is_latest_or_not_exsist_with_not_latest_date(mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    asset_id = 2
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)
    mock_settlement_repository.check_last_updated_or_none.return_value = datetime(2024, 3, 6, 12, 0, 0)

    is_latest_or_none = settlement_service.check_data_is_latest_or_not_exsist(asset_id, trade_date, last_updated)

    mock_settlement_repository.check_last_updated_or_none.assert_called_once_with(asset_id, TradeDate(date(2024, 3, 8)))
    assert is_latest_or_none is False


def test_check_data_is_latest_or_not_exsist_with_invalid_date(settlement_service: SettlementService):
    asset_id = 2
    trade_date = "Invalid Date Format"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)

    with pytest.raises(ValueError) as excinfo:
        settlement_service.check_data_is_latest_or_not_exsist(asset_id, trade_date, last_updated)
    assert "Invalid date format" in str(excinfo.value)


def test_new_entity_by_scraping_with_fraction(settlement_df: pd.DataFrame, mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    # 分数形式のchangeとsettleをテストデータに追加
    settlement_df.at[0, 'change'] = "-'27"
    settlement_df.at[0, 'settle'] = "+'010"

    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)

    # 分数形式の値も正しく処理されるかをテスト
    settlement_service.save_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)

    create_call_args = mock_settlement_repository.create.call_args[0][0]
    assert create_call_args.change == "-'27"
    assert create_call_args.settle == "+'010"


def test_new_entity_by_scraping_with_invalid_format(settlement_df: pd.DataFrame, settlement_service: SettlementService):
    # 無効な形式の値をテストデータに設定
    settlement_df.at[0, 'change'] = "invalid"
    settlement_df.at[0, 'settle'] = "also invalid"

    asset_id = 1
    trade_date = "Friday, 08 Mar 2024"
    last_updated = datetime(2024, 3, 7, 12, 0, 0)

    # 無効な形式の値が適切に処理される（例えばNoneになる）ことをテスト
    with pytest.raises(ValueError):
        settlement_service.save_settlements_from_dataframe(asset_id=asset_id, trade_date=trade_date, df=settlement_df, last_updated=last_updated)


def test_make_settlements_dataframe_by_name_and_date(mock_settlement_repository: MagicMock, settlement_service: SettlementService):
    mock_settlement_repository.fetch_settlements_by_name_and_date.return_value = [
        SettlementEntity(
            id=1,
            asset_id=1,
            trade_date=TradeDate(date(2024, 3, 8)),
            month=YearMonth(2024, 4),
            open="1,000",
            high="1,505A",
            low="950B",
            last="-",
            change="+200.8",
            settle="20'12",
            est_volume=500,
            prior_day_oi=1000,
            last_updated = datetime(2024, 3, 7, 12, 0, 0)
        )
    ]
    asset_name = "DummyAsset"
    trade_date = date(2024, 3, 8)
    df = settlement_service.make_settlements_dataframe_by_name_and_date(asset_name, trade_date)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["trade_date", "month", "open", "high", "low", "last", "change", "settle", "est_volume", "prior_day_oi", "last_updated"]
    assert df.iloc[0]["trade_date"] == date(2024, 3, 8)
    assert df.iloc[0]["month"] == "2024-04"
    assert df.iloc[0]["open"] == 1000.0
    assert df.iloc[0]["high"] == 1505.0
    assert df.iloc[0]["low"] == 950.0
    assert df.iloc[0]["last"] == None
    assert df.iloc[0]["change"] == 200.8
    assert df.iloc[0]["settle"] == 20.375
    assert df.iloc[0]["est_volume"] == 500
    assert df.iloc[0]["prior_day_oi"] == 1000
    assert df.iloc[0]["last_updated"] == datetime(2024, 3, 7, 12, 0, 0)
