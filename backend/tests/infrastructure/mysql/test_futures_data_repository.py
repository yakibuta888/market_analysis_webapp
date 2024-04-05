# tests/infrastructure/mysql/test_futures_data_repository.py
import pytest
from datetime import date
from sqlalchemy.orm import Session

from src.infrastructure.database.models import Asset, Settlement, VolumeOI
from src.infrastructure.mysql.futures_data_repository_mysql import FuturesDataRepositoryMysql
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth

@pytest.fixture
def asset_and_data(db_session: Session):
    # 資産情報の追加
    asset = Asset(name="TestAsset")
    db_session.add(asset)
    db_session.flush()  # asset.idを即座に使用できるようにする

    # 決済情報の追加
    settlement = Settlement(
        asset_id=asset.id,
        trade_date=date(2024, 3, 8),
        month="2024-04",
        settle=1000,
        est_volume=250,
        prior_day_oi=310,
        is_final=True
    )
    db_session.add(settlement)

    # 出来高・建玉情報の追加
    volume_oi = VolumeOI(
        asset_id=asset.id,
        trade_date=date(2024, 3, 8),
        month="2024-04",
        total_volume=200,
        at_close=300,
        is_final=False
    )
    db_session.add(volume_oi)
    db_session.commit()

    return asset.name, date(2024, 3, 8)

def test_fetch_by_asset_and_date(db_session: Session, asset_and_data: tuple[str, date]):
    asset_name, trade_date = asset_and_data
    repository = FuturesDataRepositoryMysql(session=db_session)
    results = repository.fetch_by_asset_and_date(asset_name, trade_date)

    assert len(results) == 1
    entity = results[0]
    assert entity.asset_name == asset_name
    assert entity.trade_date == TradeDate(trade_date)
    assert entity.month == YearMonth.from_string("APR 2024")
    assert entity.settle == 1000
    assert entity.volume == 200
    assert entity.open_interest == 300
