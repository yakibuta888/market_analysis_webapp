# tests/infrastructure/repositories/test_settlement_repository_mysql.py
import pytest
from src.domain.entities.settlement_entity import SettlementEntity
from src.infrastructure.repositories.settlement_repository_mysql import SettlementRepositoryMysql
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Settlement as SettlementModel

@pytest.fixture
def settlement_entity():
    return SettlementEntity(
        id=None,
        asset_id=1,
        trade_date='2024-03-08',
        month='2024-04',
        open=10.0,
        high=15.0,
        low=8.0,
        last=12.0,
        change=2.0,
        settle=12.0,
        est_volume=100,
        prior_day_oi=200
    )

def test_create_settlement(db_session: Session, settlement_entity: SettlementEntity):
    repository = SettlementRepositoryMysql(session=db_session)
    repository.create(settlement_entity)

    saved_settlement = db_session.query(SettlementModel).filter_by(asset_id=settlement_entity.asset_id).first()
    assert saved_settlement is not None
    assert saved_settlement.trade_date == settlement_entity.trade_date.to_date()
    assert saved_settlement.month == settlement_entity.month.to_db_format()
