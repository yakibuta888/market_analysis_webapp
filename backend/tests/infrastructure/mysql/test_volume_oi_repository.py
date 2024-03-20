# tests/infrastructure/repositories/test_volume_oi_repository.py
import pytest
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
        change=20,
        is_final=False
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
        change=20,
        is_final=True
    )

@pytest.fixture
def updated_entity(volume_oi_entity: VolumeOIEntity):
    return VolumeOIEntity(
        id=None,
        asset_id=volume_oi_entity.asset_id,
        trade_date=volume_oi_entity.trade_date,
        month=volume_oi_entity.month,
        globex=200,
        open_outcry=100,
        clear_port=50,
        total_volume=350,
        block_trades=20,
        efp=10,
        efr=4,
        tas=6,
        deliveries=2,
        at_close=300,
        change=-40,
        is_final=True
    )


def test_create_volume_oi(db_session: Session, volume_oi_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)
    repository.create(volume_oi_entity)

    saved_volume_oi = db_session.query(VolumeOIModel).filter_by(asset_id=volume_oi_entity.asset_id).first()
    assert saved_volume_oi is not None
    assert saved_volume_oi.asset_id == volume_oi_entity.asset_id
    assert saved_volume_oi.trade_date == volume_oi_entity.trade_date.to_date()
    assert saved_volume_oi.month == volume_oi_entity.month.to_db_format()
    assert saved_volume_oi.total_volume == volume_oi_entity.total_volume
    assert saved_volume_oi.at_close == volume_oi_entity.at_close
    assert saved_volume_oi.is_final == volume_oi_entity.is_final


def test_create_volume_oi_with_invalid_asset(db_session: Session, invalid_volume_oi_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)

    with pytest.raises(IntegrityError) as excinfo:
        repository.create(invalid_volume_oi_entity)

    # 期待されるエラー（外部キー制約違反など）が発生したことを確認
    assert "foreign key constraint fails" in str(excinfo.value)


def test_update_volume_oi(db_session: Session, volume_oi_entity: VolumeOIEntity, updated_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)
    repository.create(volume_oi_entity)

    repository.update(updated_entity)

    updated_volume_oi = db_session.query(VolumeOIModel).filter_by(
        asset_id=updated_entity.asset_id,
        trade_date=updated_entity.trade_date.to_date(),
        month=updated_entity.month.to_db_format()
    ).one_or_none()

    assert updated_volume_oi is not None
    assert updated_volume_oi.asset_id == volume_oi_entity.asset_id
    assert updated_volume_oi.trade_date == volume_oi_entity.trade_date.to_date()
    assert updated_volume_oi.month == volume_oi_entity.month.to_db_format()
    assert updated_volume_oi.globex == updated_entity.globex
    assert updated_volume_oi.open_outcry == updated_entity.open_outcry
    assert updated_volume_oi.clear_port == updated_entity.clear_port
    assert updated_volume_oi.total_volume == updated_entity.total_volume
    assert updated_volume_oi.block_trades == updated_entity.block_trades
    assert updated_volume_oi.efp == updated_entity.efp
    assert updated_volume_oi.efr == updated_entity.efr
    assert updated_volume_oi.tas == updated_entity.tas
    assert updated_volume_oi.deliveries == updated_entity.deliveries
    assert updated_volume_oi.at_close == updated_entity.at_close
    assert updated_volume_oi.change == updated_entity.change
    assert updated_volume_oi.is_final == updated_entity.is_final


def test_update_volume_oi_not_found(db_session: Session, volume_oi_entity: VolumeOIEntity):
    repository = VolumeOIRepositoryMysql(db_session)
    repository.create(volume_oi_entity)

    non_existing_entity = VolumeOIEntity(
        id=None,
        asset_id=volume_oi_entity.asset_id,
        trade_date=TradeDate(date(2024, 3, 9)),    # 存在しないtrade_dateを指定
        month=volume_oi_entity.month,
        globex=200,
        open_outcry=100,
        clear_port=50,
        total_volume=350,
        block_trades=20,
        efp=10,
        efr=4,
        tas=6,
        deliveries=2,
        at_close=300,
        change=-40,
        is_final=True
    )

    with pytest.raises(ValueError) as excinfo:
        repository.update(non_existing_entity)

    assert "Volume and open interest data not found." in str(excinfo.value)


def test_update_volume_oi_db_error(db_session: Session, volume_oi_entity: VolumeOIEntity, updated_entity: VolumeOIEntity, mocker):
    repository = VolumeOIRepositoryMysql(db_session)
    repository.create(volume_oi_entity)

    mocker.patch.object(db_session, "commit", side_effect=Exception("Database error"))

    with pytest.raises(Exception) as excinfo:
        repository.update(updated_entity)

    assert "Database error" in str(excinfo.value)
