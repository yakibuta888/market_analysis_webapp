# src/domain/services/settlement_service.py
import pandas as pd

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.repositories.settlement_repository import SettlementRepository
from src.domain.value_objects.trade_date import TradeDate
from src.settings import logger


class SettlementService:
    def __init__(self, settlement_repository: SettlementRepository):
        self.settlement_repository = settlement_repository

    def save_settlements_from_dataframe(self, asset_id: int, trade_date: str, df: pd.DataFrame, is_final: bool):
        for row in df.itertuples():
            try:
                settlement_entity = SettlementEntity.new_entity_by_scraping(
                    asset_id=asset_id,
                    trade_date=trade_date,
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
        logger.info(f"Settlements for asset {asset_id} - {trade_date} saved successfully.")

    def update_settlements_from_dataframe(self, asset_id: int, trade_date: str, df: pd.DataFrame, is_final: bool):
        for row in df.itertuples():
            try:
                settlement_entity = SettlementEntity.new_entity_by_scraping(
                    asset_id=asset_id,
                    trade_date=trade_date,
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
                self.settlement_repository.update(settlement_entity)
            except ValueError as e:
                logger.error(f"Validation error for row {row}: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error updating settlement for row {row}: {e}")
                raise e
        logger.info(f"Settlements for asset {asset_id} - {trade_date} updated successfully.")

    def check_data_is_final(self, asset_id: int, trade_date: str) -> bool | None:
        try:
            trade_date_obj = TradeDate.from_string(trade_date)
        except ValueError as e:
            logger.error(f"Invalid date format: {trade_date}")
            raise e
        return self.settlement_repository.check_data_is_final_or_none(asset_id, trade_date_obj)
