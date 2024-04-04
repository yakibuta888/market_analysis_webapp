# src/domain/services/settlement_service.py
import pandas as pd
from datetime import date

from src.domain.entities.settlement_entity import SettlementEntity
from src.domain.logics.convert_price_format import convert_price_format
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

    def make_settlements_dataframe_by_name_and_date(self, asset_name: str, trade_date: date) -> pd.DataFrame:
        """指定されたasset_nameとtrade_dateに基づいて決済データを取得し、DataFrameを作成する"""
        settlements = self.settlement_repository.fetch_settlements_by_name_and_date(asset_name, trade_date)

        # DataFrameの作成
        df = pd.DataFrame([{
            'trade_date': settlement.trade_date.value,
            'month': str(settlement.month),
            'open': convert_price_format(settlement.open),
            'high': convert_price_format(settlement.high),
            'low': convert_price_format(settlement.low),
            'last': convert_price_format(settlement.last),
            'change': convert_price_format(settlement.change),
            'settle': convert_price_format(settlement.settle),
            'est_volume': settlement.est_volume,
            'prior_day_oi': settlement.prior_day_oi,
            'is_final': settlement.is_final
        } for settlement in settlements])

        # 数値型に変換できなかったデータはNaNになるため、必要に応じて処理を行う
        return df
