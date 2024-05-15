# tests/infrastructure/mysql/test_futures_data_trade_date_repository.py
import pytest
from datetime import date, datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infrastructure.database.models import Asset, Settlement, VolumeOI
from src.infrastructure.mysql.futures_data_trade_date_repository_mysql import FuturesDataTradeDateRepositoryMysql
from src.domain.entities.trade_date_entity import TradeDateEntity

# テストデータのセットアップ
@pytest.fixture(scope="function")
def setup_data(db_session: Session):
    # テストデータをここでセットアップ
    asset = Asset(name="Gold")
    db_session.add(asset)
    db_session.flush()  # asset.idを即座に使用できるようにする

    settlements = [
        Settlement(
            asset_id=asset.id,
            trade_date=date(2023, 1, 1),
            month="2023-01",
            settle=1000,
            est_volume=250,
            prior_day_oi=310,
            last_updated=datetime(2022, 12, 28, 12, 0, 0)
        ),
        Settlement(
            asset_id=asset.id,
            trade_date=date(2023, 1, 2),
            month="2023-01",
            settle=1100,
            est_volume=300,
            prior_day_oi=320,
            last_updated=datetime(2022, 12, 29, 12, 0, 0)
        )
    ]
    for settlement in settlements:
        db_session.add(settlement)

    volume_ois = [
        VolumeOI(
            asset_id=asset.id,
            trade_date=date(2023, 1, 1),
            month="2023-01",
            total_volume=200,
            at_close=300,
            is_final=True
        ),
        VolumeOI(
            asset_id=asset.id,
            trade_date=date(2023, 1, 2),
            month="2023-01",
            total_volume=210,
            at_close=310,
            is_final=False
        )
    ]
    for volume_oi in volume_ois:
        db_session.add(volume_oi)

    db_session.commit()

    return asset.name


def test_fetch_trade_dates_basic(db_session: Session, setup_data: str):
    asset_name = setup_data
    repository = FuturesDataTradeDateRepositoryMysql(session=db_session)
    result = repository.fetch_trade_dates(asset_name, date(2023, 1, 1), date(2023, 1, 1), 0, 10)
    assert len(result) == 1
    assert isinstance(result[0], TradeDateEntity)
    assert result[0].trade_date == date(2023, 1, 1)


def test_fetch_trade_dates_with_none_dates(db_session: Session, setup_data: str):
    asset_name = setup_data
    repository = FuturesDataTradeDateRepositoryMysql(session=db_session)
    result = repository.fetch_trade_dates(asset_name, None, None, 0, 10)
    assert len(result) == 2  # すべての日付のデータが返される
    assert isinstance(result[0], TradeDateEntity)
    assert result[0].trade_date == date(2023, 1, 1)
    assert isinstance(result[1], TradeDateEntity)
    assert result[1].trade_date == date(2023, 1, 2)


def test_fetch_trade_dates_pagination(db_session: Session, setup_data: str):
    asset_name = setup_data
    repository = FuturesDataTradeDateRepositoryMysql(session=db_session)
    # 初めの1件のみを取得
    result = repository.fetch_trade_dates(asset_name, date(2023, 1, 1), date(2023, 1, 2), 0, 1)
    assert len(result) == 1


    # オフセットを設定してデータをスキップ
    result = repository.fetch_trade_dates(asset_name, date(2023, 1, 1), date(2023, 1, 2), 1, 10)
    assert len(result) == 1  # スキップされるため1件のみ返される
