# src/domain/services/settlement_service.py
import pandas as pd

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.repositories.settlement_repository import SettlementRepository
from src.settings import logger


class SettlementService:
    def __init__(self, settlement_repository: SettlementRepository):
        self.settlement_repository = settlement_repository

    def save_settlements_from_dataframe(self, df: pd.DataFrame, asset_id: int, is_final: bool):
        for row in df.itertuples():
            try:
                settlement_entity = SettlementEntity.new_entity_by_scraping(
                    asset_id=asset_id,
                    trade_date=str(row.trade_date),
                    month=str(row.month),
                    open=str(row.open),
                    high=str(row.high),
                    low=str(row.low),
                    last=str(row.last),
                    change=str(row.change),
                    settle=str(row.settle),
                    est_volume=str(row.est_volume),
                    prior_day_oi=str(row.prior_day_oi),
                    is_final=is_final
                )
                self.settlement_repository.create(settlement_entity)
            except ValueError as e:
                logger.error(f"Validation error for row {row}: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error saving settlement for row {row}: {e}")
                raise e
        logger.info(f"Settlements for asset {asset_id} - {settlement_entity.trade_date} saved successfully.")
