# src/domain/services/futures_data_service.py
import pandas as pd
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.futures_data_entity import FuturesDataEntity
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.repositories.futures_data_repository import FuturesDataRepository
from src.settings import logger


class FuturesDataService:
    def __init__(self, futures_data_repository: FuturesDataRepository):
        self.futures_data_repository = futures_data_repository

    def make_dataframe(self, asset_name: str, trade_date: date) -> pd.DataFrame:
        """
        指定された資産名と取引日に基づいてデータを取得し、PandasのDataFrameに変換します。

        :param asset_name: 資産名
        :param trade_date: 取引日
        :return: FuturesDataEntityのリストをDataFrameに変換したもの
        """
        try:
            if not asset_name or not trade_date:
                raise InvalidInputError("資産名または取引日が指定されていません。")

            futures_data_entities: list[FuturesDataEntity] = self.futures_data_repository.fetch_by_asset_and_date(asset_name, trade_date)

            # データが空の場合は空のDataFrameを返す
            if not futures_data_entities:
                return pd.DataFrame()

            # FuturesDataEntityのリストからDataFrameを作成
            df = pd.DataFrame([{
                'month': entity.month.to_datetime(),
                'settle': entity.settle,
                'volume': entity.volume,
                'open_interest': entity.open_interest
            } for entity in futures_data_entities])

            return df

        except InvalidInputError as e:
            # 特定のエラー（例: 無効な入力値）を処理
            logger.error(f"エラー: {e}")
            raise e

        except SQLAlchemyError as e:
            # SQLAlchemyやデータベース関連のエラーを処理
            logger.error(f"データベースエラー: {e}")
            raise RepositoryError("データベース操作中にエラーが発生しました。")

        except Exception as e:
            # 予期せぬ例外のキャッチ
            logger.error(f"予期せぬエラー: {e}")
            raise RepositoryError("予期せぬエラーが発生しました。")
