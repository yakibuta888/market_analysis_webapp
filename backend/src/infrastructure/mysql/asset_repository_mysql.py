# src/infrastructures/repositories/asset_repository_mysql.py
from sqlalchemy.orm import Session

from src.domain.entities.asset_entity import AssetEntity
from src.domain.exceptions.asset_not_found_error import AssetNotFoundError
from src.domain.repositories.asset_repository import AssetRepository
from src.domain.value_objects.name import Name
from src.infrastructure.database.models import Asset as AssetModel
from src.settings import logger


class AssetRepositoryMysql(AssetRepository):
    def __init__(self, session: Session):
        self.session = session

# HACK: session.bigin()を利用すると、'A transaction is already begun on this Session.'エラーが発生するため、try/exceptブロックでcommit/rollbackを実行しています。
    def create(self, asset_entity: AssetEntity) -> AssetModel:
        try:
            asset_db = AssetModel(name=asset_entity.name.name)
            self.session.add(asset_db)
            self.session.commit()
            return asset_db
        except Exception as e:
            self.session.rollback()
            logger.error(f"データベースエラー: {e}")
            raise e

    def fetch_all(self) -> list[AssetModel]:
        assets = self.session.query(AssetModel).all()
        if assets == []:
            raise AssetNotFoundError("Assets not found")
        return assets

    def fetch_by_name(self, name: Name) -> AssetModel:
        asset_db = self.session.query(AssetModel).filter(AssetModel.name == name.name).first()
        if asset_db is None:
            raise AssetNotFoundError(f"Asset with name {name.name} not found")
        return asset_db

    def exists_by_name(self, name: Name) -> bool:
        asset_db = self.session.query(AssetModel).filter(AssetModel.name == name.name).first()
        return asset_db is not None

# TODO: 未実装
    def update(self, asset_entity: AssetEntity) -> AssetModel:
        # FIXME: idで検索し、新しい名前で更新するように実装してください
        asset_db = self.fetch_by_name(asset_entity.name)
        asset_db.name = asset_entity.name.name
        self.session.commit()
        return asset_db

    def delete(self, name: Name) -> None:
        try:
            asset_db = self.fetch_by_name(name)
            self.session.delete(asset_db)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"データベースエラー: {e}")
            raise e
