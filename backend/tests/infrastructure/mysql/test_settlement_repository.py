# tests/infrastructure/repositories/test_settlement_repository_mysql.py
import pytest
from datetime import date
from sqlalchemy.orm import Session

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
