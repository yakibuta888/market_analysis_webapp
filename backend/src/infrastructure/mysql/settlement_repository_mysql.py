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

    def update(self, settlement_entity: SettlementEntity) -> SettlementModel:
        try:
            settlement_model = self.session.query(SettlementModel).filter(
                SettlementModel.asset_id == settlement_entity.asset_id,
                SettlementModel.trade_date == settlement_entity.trade_date.to_date(),
                SettlementModel.month == settlement_entity.month.to_db_format()
            ).one_or_none()
            if settlement_model:
                settlement_model.open = settlement_entity.open
                settlement_model.high = settlement_entity.high
                settlement_model.low = settlement_entity.low
                settlement_model.last = settlement_entity.last
                settlement_model.change = settlement_entity.change
                settlement_model.settle = settlement_entity.settle
                settlement_model.est_volume = settlement_entity.est_volume
                settlement_model.prior_day_oi = settlement_entity.prior_day_oi
                settlement_model.is_final = settlement_entity.is_final
                self.session.commit()
                logger.info(f"Updated settlement data for asset {settlement_entity.asset_id} on {settlement_entity.trade_date}.")
                return settlement_model
            else:
                logger.warning(f"No record found for asset {settlement_entity.asset_id} on {settlement_entity.trade_date}. Update skipped.")
                raise ValueError("Settlement not found.")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating settlement: {e}")
            raise e
