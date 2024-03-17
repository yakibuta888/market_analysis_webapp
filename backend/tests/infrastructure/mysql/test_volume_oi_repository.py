# tests/infrastructure/repositories/test_volume_oi_repository.py
import pytest
from datetime import date
from sqlalchemy.orm import Session

from src.infrastructure.database.models import Asset as AssetModel
from src.infrastructure.database.models import VolumeOI as VolumeOIModel
from src.infrastructure.mysql.volume_oi_repository_mysql import VolumeOIRepositoryMysql
from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth

@pytest.fixture
def asset(db_session: Session):
    asset_model = AssetModel(name="Test Asset")
    db_session.add(asset_model)
    db_session.commit()
    return asset_model

@pytest.fixture
def volume_oi_entity(asset: AssetModel):
    return VolumeOIEntity(
        id=None,
        asset_id=asset.id,
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        globex=100,
        open_outcry=50,
        clear_port=25,
        total_volume=175,
        block_trades=10,
        efp=5,
        efr=2,
        tas=3,
        deliveries=1,
        at_close=150,
        change=20
    )

@pytest.fixture
def invalid_volume_oi_entity():
    return VolumeOIEntity(
        id=None,
        asset_id=-1,    # 存在しないasset_idを指定
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        globex=100,
        open_outcry=50,
        clear_port=25,
        total_volume=175,
        block_trades=10,
        efp=5,
        efr=2,
        tas=3,
        deliveries=1,
        at_close=150,
        change=20
    )

def test_create_volume_oi(db_session: Session, volume_oi_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)
    repository.create(volume_oi_entity)

    saved_volume_oi = db_session.query(VolumeOIModel).filter_by(asset_id=volume_oi_entity.asset_id).first()
    assert saved_volume_oi is not None
    assert saved_volume_oi.asset_id == volume_oi_entity.asset_id
    assert saved_volume_oi.trade_date == volume_oi_entity.trade_date.to_date()
    assert saved_volume_oi.month == volume_oi_entity.month.to_db_format()

def test_create_volume_oi_with_invalid_asset(db_session: Session, invalid_volume_oi_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)

    with pytest.raises(Exception) as excinfo:
        repository.create(invalid_volume_oi_entity)

    # 期待されるエラー（外部キー制約違反など）が発生したことを確認
    assert "foreign key constraint fails" in str(excinfo.value)
