# src/infrastructure/repositories/settlement_repository_mysql.py
from sqlalchemy.orm import Session

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.repositories.settlement_repository import SettlementRepository
from src.infrastructure.database.models import Settlement as SettlementModel
from src.settings import logger


class SettlementRepositoryMysql(SettlementRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, settlement_entity: SettlementEntity) -> SettlementModel:
        try:
            settlement_model = SettlementModel(
                asset_id=settlement_entity.asset_id,
                trade_date=settlement_entity.trade_date.to_date(),
                month=settlement_entity.month.to_db_format(),
                open=settlement_entity.open,
                high=settlement_entity.high,
                low=settlement_entity.low,
                last=settlement_entity.last,
                change=settlement_entity.change,
                settle=settlement_entity.settle,
                est_volume=settlement_entity.est_volume,
                prior_day_oi=settlement_entity.prior_day_oi,
                is_final=settlement_entity.is_final
            )
            self.session.add(settlement_model)
            self.session.commit()
            return settlement_model
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error saving settlement: {e}")
            raise e
