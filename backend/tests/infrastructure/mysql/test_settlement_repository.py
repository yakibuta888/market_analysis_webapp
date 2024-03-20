# tests/infrastructure/repositories/test_settlement_repository_mysql.py
import pytest
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from src.infrastructure.mysql.settlement_repository_mysql import SettlementRepositoryMysql
from src.infrastructure.database.models import Asset as AssetModel
from src.infrastructure.database.models import Settlement as SettlementModel


@pytest.fixture
def asset(db_session: Session):
    asset = AssetModel(name="TestAsset")
    db_session.add(asset)
    db_session.commit()
    return asset

@pytest.fixture
def settlement_entity(asset: AssetModel):
    return SettlementEntity(
        id=None,
        asset_id=asset.id,
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        open="10.0",
        high="15.0",
        low="8.0",
        last="12.0",
        change=2.0,
        settle=12.0,
        est_volume=100,
        prior_day_oi=200,
        is_final=False
    )

@pytest.fixture
def invalid_settlement_entity():
    return SettlementEntity(
        id=None,
        asset_id=-1,    # 存在しないasset_idを指定
        trade_date=TradeDate(date(2024, 3, 8)),
        month=YearMonth(2024, 4),
        open="10.0",
        high="15.0",
        low="8.0",
        last="12.0",
        change=2.0,
        settle=12.0,
        est_volume=100,
        prior_day_oi=200,
        is_final=True
    )


def test_create_settlement(db_session: Session, asset: AssetModel, settlement_entity: SettlementEntity):
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    saved_settlement = db_session.query(SettlementModel).filter_by(asset_id=settlement_entity.asset_id).first()
    assert saved_settlement is not None
    assert saved_settlement.asset_id == asset.id
    assert saved_settlement.trade_date == settlement_entity.trade_date.to_date()
    assert saved_settlement.month == settlement_entity.month.to_db_format()
    assert saved_settlement.settle == settlement_entity.settle
    assert saved_settlement.is_final == settlement_entity.is_final


def test_create_settlement_invalid_asset_id(db_session: Session, invalid_settlement_entity: SettlementEntity):
    repository = SettlementRepositoryMysql(session=db_session)

    # 存在しないasset_idを指定してエンティティを作成しようとすると、例外が発生することを確認
    with pytest.raises(IntegrityError) as excinfo:
        repository.create(invalid_settlement_entity)

    assert "foreign key constraint fails" in str(excinfo.value)


def test_update_settlement(db_session: Session, asset: AssetModel, settlement_entity: SettlementEntity):
    # まず、SettlementEntityを作成してDBに保存
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    # DBに保存されたデータを更新するための新しいエンティティを作成
    updated_entity = SettlementEntity(
        id=None,
        asset_id=settlement_entity.asset_id,
        trade_date=settlement_entity.trade_date,
        month=settlement_entity.month,
        open="11.0",
        high="16.0",
        low="9.0",
        last="13.0",
        change=3.0,
        settle=13.0,
        est_volume=200,
        prior_day_oi=300,
        is_final=True
    )

    # 更新メソッドを呼び出し
    repository.update(updated_entity)

    # 更新されたデータをDBから取得して検証
    updated_settlement = db_session.query(SettlementModel).filter_by(
        asset_id=updated_entity.asset_id,
        trade_date=updated_entity.trade_date.to_date(),
        month=updated_entity.month.to_db_format()
    ).one()

    assert updated_settlement.open == updated_entity.open
    assert updated_settlement.high == updated_entity.high
    assert updated_settlement.low == updated_entity.low
    assert updated_settlement.last == updated_entity.last
    assert updated_settlement.change == updated_entity.change
    assert updated_settlement.settle == updated_entity.settle
    assert updated_settlement.est_volume == updated_entity.est_volume
    assert updated_settlement.prior_day_oi == updated_entity.prior_day_oi
    assert updated_settlement.is_final == updated_entity.is_final


def test_update_settlement_not_found(db_session: Session, asset: AssetModel):
    repository = SettlementRepositoryMysql(session=db_session)

    # 存在しないエンティティを更新しようとする
    non_existing_entity = SettlementEntity(
        id=None,
        asset_id=asset.id,
        trade_date=TradeDate(date(2024, 4, 1)),
        month=YearMonth(2024, 5),
        open="20.0",
        high="25.0",
        low="18.0",
        last="23.0",
        change=2.5,
        settle=23.5,
        est_volume=150,
        prior_day_oi=250,
        is_final=True
    )

    # 更新メソッドを呼び出し、レコードが見つからない場合に例外が発生することを確認
    with pytest.raises(ValueError) as excinfo:
        repository.update(non_existing_entity)
    assert "Settlement not found" in str(excinfo.value)


def test_update_settlement_db_error(db_session: Session, asset: AssetModel, settlement_entity: SettlementEntity, mocker):
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    # データベース操作中にエラーが発生するようにモックを設定
    mocker.patch.object(db_session, 'commit', side_effect=Exception("Database error"))

    # 既に存在するエンティティを更新しようとするが、データベースエラーにより例外が発生することを確認
    with pytest.raises(Exception) as excinfo:
        repository.update(settlement_entity)
    assert "Database error" in str(excinfo.value)
