# src/infrastructure/repositories/volume_oi_repository_mysql.py
from sqlalchemy.orm import Session

from src.domain.entities.volume_oi_entity import VolumeOIEntity
from src.domain.repositories.volume_oi_repository import VolumeOIRepository
from src.infrastructure.database.models import VolumeOI as VolumeOIModel
from src.settings import logger

class VolumeOIRepositoryMysql(VolumeOIRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, volume_oi_entity: VolumeOIEntity) -> VolumeOIModel:
        try:
            volume_oi_model = VolumeOIModel(
                asset_id=volume_oi_entity.asset_id,
                trade_date=volume_oi_entity.trade_date.to_date(),
                month=volume_oi_entity.month.to_db_format(),
                globex=volume_oi_entity.globex,
                open_outcry=volume_oi_entity.open_outcry,
                clear_port=volume_oi_entity.clear_port,
                total_volume=volume_oi_entity.total_volume,
                block_trades=volume_oi_entity.block_trades,
                efp=volume_oi_entity.efp,
                efr=volume_oi_entity.efr,
                tas=volume_oi_entity.tas,
                deliveries=volume_oi_entity.deliveries,
                at_close=volume_oi_entity.at_close,
                change=volume_oi_entity.change,
                is_final=volume_oi_entity.is_final
            )
            self.session.add(volume_oi_model)
            self.session.commit()
            return volume_oi_model
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error saving volume and open interest data: {e}")
            raise e

    def update(self, volume_oi_entity: VolumeOIEntity) -> VolumeOIModel:
        try:
            volume_oi_model = self.session.query(VolumeOIModel).filter(
                VolumeOIModel.asset_id == volume_oi_entity.asset_id,
                VolumeOIModel.trade_date == volume_oi_entity.trade_date.to_date(),
                VolumeOIModel.month == volume_oi_entity.month.to_db_format()
            ).one_or_none()
            if volume_oi_model:
                volume_oi_model.globex = volume_oi_entity.globex
                volume_oi_model.open_outcry = volume_oi_entity.open_outcry
                volume_oi_model.clear_port = volume_oi_entity.clear_port
                volume_oi_model.total_volume = volume_oi_entity.total_volume
                volume_oi_model.block_trades = volume_oi_entity.block_trades
                volume_oi_model.efp = volume_oi_entity.efp
                volume_oi_model.efr = volume_oi_entity.efr
                volume_oi_model.tas = volume_oi_entity.tas
                volume_oi_model.deliveries = volume_oi_entity.deliveries
                volume_oi_model.at_close = volume_oi_entity.at_close
                volume_oi_model.change = volume_oi_entity.change
                volume_oi_model.is_final = volume_oi_entity.is_final
                self.session.commit()
                logger.info(f"Updated volume and open interest data for asset {volume_oi_entity.asset_id} on {volume_oi_entity.trade_date}.")
                return volume_oi_model
            else:
                logger.warning(f"No record found for asset {volume_oi_entity.asset_id} on {volume_oi_entity.trade_date}. Update skipped.")
                raise ValueError("Volume and open interest data not found.")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating volume and open interest data: {e}")
            raise e
