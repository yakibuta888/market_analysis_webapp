# src/domain/services/volume_oi_service.py
import pandas as pd
from typing import NamedTuple

from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.repositories.volume_oi_repository import VolumeOIRepository
from src.domain.value_objects.trade_date import TradeDate
from src.settings import logger


_VOINamedTuple = NamedTuple('_VOINamedTuple', [
    ('month', str),
    ('globex', int),
    ('open_outcry', int),
    ('clear_port', int),
    ('total_volume', int),
    ('block_trades', int),
    ('efp', int),
    ('efr', int),
    ('tas', int),
    ('deliveries', int),
    ('at_close', int),
    ('change', int)
])


class VolumeOIService:
    def __init__(self, volume_oi_repository: VolumeOIRepository):
        self.volume_oi_repository = volume_oi_repository


    def _transform_dataframe_types(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_columns = ['globex', 'open_outcry', 'clear_port', 'total_volume', 'block_trades', 'efp', 'efr', 'tas', 'deliveries', 'at_close', 'change']
        for col in numeric_columns:
            df[col] = df[col].apply(lambda x: int(x.replace(',', '').replace('+', ''))) # type: ignore
        return df


    def _row_to_entity(self, row: _VOINamedTuple , asset_id: int, trade_date: str, is_final: bool) -> VolumeOIEntity:
        # DataFrameの行からEntityを生成
        return VolumeOIEntity.new_entity(
            asset_id=asset_id,
            trade_date=trade_date,
            month=row.month,
            globex=row.globex,
            open_outcry=row.open_outcry,
            clear_port=row.clear_port,
            total_volume=row.total_volume,
            block_trades=row.block_trades,
            efp=row.efp,
            efr=row.efr,
            tas=row.tas,
            deliveries=row.deliveries,
            at_close=row.at_close,
            change=row.change,
            is_final=is_final
        )


    def save_volume_oi_from_dataframe(self, asset_id: int, trade_date: str, df: pd.DataFrame, is_final: bool):
        # DataFrameの各列の型を変換する
        df = self._transform_dataframe_types(df)

        for row in df.itertuples(index=False):
            try:
                volume_oi_entity = self._row_to_entity(row, asset_id, trade_date, is_final)
                self.volume_oi_repository.create(volume_oi_entity)
            except ValueError as e:
                logger.error(f"Validation error for row {row}: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error saving volume and open interest data for row {row}: {e}")
                raise e
        else:
            logger.info(f"Volume and open interest data for asset {asset_id} - {trade_date} saved successfully.")


    def update_volume_oi_from_dataframe(self, asset_id: int, trade_date: str, df: pd.DataFrame, is_final: bool):
        # DataFrameの各列の型を変換する
        df = self._transform_dataframe_types(df)

        for row in df.itertuples(index=False):
            try:
                volume_oi_entity = self._row_to_entity(row, asset_id, trade_date, is_final)
                self.volume_oi_repository.update(volume_oi_entity)
            except ValueError as e:
                logger.error(f"Validation error for row {row}: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error updating volume and open interest data for row {row}: {e}")
                raise e
        else:
            logger.info(f"Volume and open interest data for asset {asset_id} - {trade_date} updated successfully.")


    def check_data_is_final(self, asset_id: int, trade_date: str) -> bool | None:
        try:
            trade_date_obj = TradeDate.from_string(trade_date)
        except ValueError as e:
            logger.error(f"Invalid date format: {trade_date}")
            raise e
        return self.volume_oi_repository.check_data_is_final_or_none(asset_id, trade_date_obj)
