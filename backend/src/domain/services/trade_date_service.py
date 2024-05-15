#src/domain/services/trade_date_service.py
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.trade_date_entity import TradeDateEntity
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.repositories.trade_date_repository import TradeDateRepository
from src.settings import logger


class TradeDateService:
    def __init__(self, trade_date_repository: TradeDateRepository):
        self.trade_date_repository = trade_date_repository

    def fetch_trade_dates(self, asset_name: str, start_date: date | None, end_date: date | None, skip: int, limit: int) -> list[TradeDateEntity]:
        """
        指定された資産名と日付範囲に基づいて取引日を取得します。

        :param asset_name: 資産名
        :param start_date: 開始日
        :param end_date: 終了日
        :param skip: 取得開始位置
        :param limit: 取得件数
        :return: TradeDateEntityのリスト
        """
        try:
            if not asset_name:
                raise InvalidInputError("資産名が指定されていません。")

            if start_date and end_date and start_date > end_date:
                raise InvalidInputError("開始日が終了日より後です。")

            return self.trade_date_repository.fetch_trade_dates(asset_name, start_date, end_date, skip, limit)

        except InvalidInputError as e:
            logger.error(f"Invalid input error: {e}")
            raise e

        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {e}")
            raise RepositoryError("Error accessing data repository.")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise RepositoryError("An unexpected error occurred.")
