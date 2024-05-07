# tests/infrastructure/repositories/test_settlement_repository_mysql.py
import pytest
from datetime import date, datetime
from pytest_mock import MockerFixture
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
        change="+2.0",
        settle="12.0",
        est_volume=100,
        prior_day_oi=200,
        last_updated=datetime(2024, 3, 6, 12, 0, 0),
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
        change="+2.0",
        settle="12.0",
        est_volume=100,
        prior_day_oi=200,
        last_updated=datetime(2024, 3, 8, 12, 0, 0)
    )


@pytest.fixture
def db_settlements(db_session: Session, asset: AssetModel):
    settlements = [
        SettlementModel(
            asset_id=asset.id,
            trade_date=date(2024, 3, 11),
            month="2024-06",
            open="9.0",
            high="16.3",
            low="7.0",
            last="12.3",
            change="-'2",
            settle="12.0",
            est_volume=110,
            prior_day_oi=250,
            last_updated=datetime(2024, 3, 6, 12, 0, 0),
        ),
        SettlementModel(
            asset_id=asset.id,
            trade_date=date(2024, 3, 11),
            month="2024-07",
            open="11.0",
            high="16.0A",
            low="9'05",
            last="1300.0B",
            change="+3.0",
            settle="13.0",
            est_volume=200,
            prior_day_oi=300,
            last_updated=datetime(2024, 3, 6, 12, 0, 0),
        )
    ]
    db_session.bulk_save_objects(settlements)
    db_session.commit()
    return settlements


def test_create_settlement(db_session: Session, asset: AssetModel, settlement_entity: SettlementEntity):
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    saved_settlement = db_session.query(SettlementModel).filter_by(asset_id=settlement_entity.asset_id).first()
    assert saved_settlement is not None
    assert saved_settlement.asset_id == asset.id
    assert saved_settlement.trade_date == settlement_entity.trade_date.to_date()
    assert saved_settlement.month == settlement_entity.month.to_db_format()
    assert saved_settlement.settle == settlement_entity.settle
    assert saved_settlement.last_updated == settlement_entity.last_updated


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
        change="+3.0",
        settle="13.0",
        est_volume=200,
        prior_day_oi=300,
        last_updated=datetime(2024, 3, 7, 12, 0, 0)
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
    assert updated_settlement.last_updated == updated_entity.last_updated


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
        change="+2.5",
        settle="23.5",
        est_volume=150,
        prior_day_oi=250,
        last_updated=datetime(2024, 3, 7, 12, 0, 0)
    )

    # 更新メソッドを呼び出し、レコードが見つからない場合に例外が発生することを確認
    with pytest.raises(ValueError) as excinfo:
        repository.update(non_existing_entity)
    assert "Settlement not found" in str(excinfo.value)


def test_update_settlement_db_error(db_session: Session, asset: AssetModel, settlement_entity: SettlementEntity, mocker: MockerFixture):
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    # データベース操作中にエラーが発生するようにモックを設定
    mocker.patch.object(db_session, 'commit', side_effect=Exception("Database error"))

    # 既に存在するエンティティを更新しようとするが、データベースエラーにより例外が発生することを確認
    with pytest.raises(Exception) as excinfo:
        repository.update(settlement_entity)
    assert "Database error" in str(excinfo.value)


def test_check_last_updated_with_existing_data(db_session: Session, asset: AssetModel, db_settlements: list[SettlementModel]):
    repository = SettlementRepositoryMysql(session=db_session)

    # Finalでないデータの確認
    trade_date = TradeDate.from_string("Monday, 11 Mar 2024")
    last_updated = repository.check_last_updated_or_none(asset.id, trade_date)
    assert last_updated == datetime(2024, 3, 6, 12, 0, 0)


def test_check_data_is_final_with_non_existing_data(db_session: Session):
    repository = SettlementRepositoryMysql(session=db_session)

    # 存在しないデータに対する確認
    trade_date = TradeDate.from_string("Saturday, 09 Mar 2024")
    last_updated = repository.check_last_updated_or_none(999, trade_date)  # 存在しないasset_idとtrade_date
    assert last_updated is None

def test_fetch_settlements_by_name_and_date(db_session: Session, db_settlements: list[SettlementModel], asset: AssetModel):
    repository = SettlementRepositoryMysql(db_session)
    asset_name = asset.name
    trade_date = date(2024, 3, 11)

    # メソッドを実行
    settlements = repository.fetch_settlements_by_name_and_date(asset_name, trade_date)

    expected_values = [
        {
            'month': YearMonth(2024, 6),
            'open': "9.0",
            'high': "16.3",
            'low': "7.0",
            'last': "12.3",
            'change': "-'2",
            'settle': "12.0",
            'est_volume': 110,
            'prior_day_oi': 250,
            'last_updated': datetime(2024, 3, 6, 12, 0, 0)
        },
        {
            'month': YearMonth(2024, 7),
            'open': "11.0",
            'high': "16.0A",
            'low': "9'05",
            'last': "1300.0B",
            'change': "+3.0",
            'settle': "13.0",
            'est_volume': 200,
            'prior_day_oi': 300,
            'last_updated': datetime(2024, 3, 6, 12, 0, 0)
        }
    ]

    # 検証: 取得された決済データが期待通りであることを確認
    assert len(settlements) == len(expected_values)
    assert all(isinstance(settlement, SettlementEntity) for settlement in settlements)
    assert all(settlement.asset_id == asset.id for settlement in settlements)
    assert all(settlement.trade_date == TradeDate(trade_date) for settlement in settlements)

    for settlement, expected in zip(settlements, expected_values):
        assert settlement.month == expected['month']
        assert settlement.open == expected['open']
        assert settlement.high == expected['high']
        assert settlement.low == expected['low']
        assert settlement.last == expected['last']
        assert settlement.change == expected['change']
        assert settlement.settle == expected['settle']
        assert settlement.est_volume == expected['est_volume']
        assert settlement.prior_day_oi == expected['prior_day_oi']
        assert settlement.last_updated == expected['last_updated']
