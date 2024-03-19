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
