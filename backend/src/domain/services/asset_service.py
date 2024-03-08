#src/domain/services/asset_service.py
import json
from sqlalchemy.orm import Session

from src.settings import logger
from src.infrastructure.database.models import Asset
from src.domain.entities.asset_entity import AssetEntity
from src.domain.entities.asset_entity import Name
from src.domain.repositories.asset_repository import AssetRepository

class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    def add_asset(self, name: str):
        try:
            # エンティティのバリデーションを実行
            asset_entity = AssetEntity.new_entity(name=Name(name))
            self.asset_repository.create(asset_entity)
            logger.info(f"資産 '{name}' が追加されました。")
        except ValueError as e:
            # バリデーションエラーが発生した場合
            logger.error(f"バリデーションエラー: {e}")
            raise e
        except Exception as e:
            # その他のエラーが発生した場合
            logger.error(f"データベースエラー: {e}")
            raise e

    def remove_asset(self, name: str):
        try:
            # 資産名に基づいて資産を検索
            if self.asset_repository.exists_by_name(Name(name)):
                # 資産が存在する場合、削除
                self.asset_repository.delete(Name(name))
                logger.info(f"資産 '{name}' が削除されました。")
            else:
                logger.warning(f"資産 '{name}' が見つかりません。")
        except Exception as e:
            logger.error(f"データベースエラー: {e}")
            raise e

    def initialize_assets_from_config(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)

        for asset_name in config.keys():
            try:
                # 既に存在する資産を確認
                if not self.asset_repository.exists_by_name(Name(asset_name)):
                    # 資産が存在しない場合、新しい資産エンティティを作成し追加
                    asset_entity = AssetEntity.new_entity(name=Name(asset_name))
                    self.asset_repository.create(asset_entity)
                    logger.info(f"資産 '{asset_name}' を追加しました。")
                else:
                    logger.info(f"資産 '{asset_name}' は既に存在します。")
            except ValueError as e:
                logger.error(f"バリデーションエラー: {e}")
                raise e
            except Exception as e:
                logger.error(f"資産 '{asset_name}' の追加中にエラーが発生しました: {e}")
                raise e
