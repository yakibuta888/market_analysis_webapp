# src/domain/services/volume_oi_service.py
import pandas as pd
from typing import Any, Dict
from sqlalchemy.orm import Session

from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.repositories.volume_oi_repository import VolumeOIRepository
from src.settings import logger

class VolumeOIService:
    def __init__(self, volume_oi_repository: VolumeOIRepository):
        self.volume_oi_repository = volume_oi_repository

    def save_volume_oi_from_dataframe(self, df: pd.DataFrame, asset_id: int):
        # DataFrameの各列の型を変換する
        df = self._transform_dataframe_types(df)

        for _, row in df.iterrows():
            try:
                volume_oi_entity = self._row_to_entity(row, asset_id)
                self.volume_oi_repository.create(volume_oi_entity)
            except ValueError as e:
                logger.error(f"Validation error for row {row.to_dict()}: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error saving volume and open interest data for row {row.to_dict()}: {e}")
                raise e

        logger.info(f"Volume and open interest data for asset {asset_id} saved successfully.")

    def _transform_dataframe_types(self, df: pd.DataFrame) -> pd.DataFrame:
        # 必要に応じて型変換を行う
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
        # 他の数値列に対して適切な型変換を行う
        numeric_columns = ['globex', 'open_outcry', 'clear_port', 'total_volume', 'block_trades', 'efp', 'efr', 'tas', 'deliveries', 'at_close', 'change']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        return df

    def _row_to_entity(self, row: pd.Series, asset_id: int) -> VolumeOIEntity:
        # DataFrameの行からEntityを生成
        return VolumeOIEntity.new_entity(
            asset_id=asset_id,
            trade_date=row['trade_date'],
            month=row['month'],
            globex=row['globex'],
            open_outcry=row['open_outcry'],
            clear_port=row['clear_port'],
            total_volume=row['total_volume'],
            block_trades=row['block_trades'],
            efp=row['efp'],
            efr=row['efr'],
            tas=row['tas'],
            deliveries=row['deliveries'],
            at_close=row['at_close'],
            change=row['change']
        )
