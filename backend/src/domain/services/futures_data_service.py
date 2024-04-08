# src/domain/services/futures_data_service.py
import pandas as pd
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.futures_data_entity import FuturesDataEntity
from src.domain.exceptions.dataframe_validation_error import DataFrameValidationError
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.repositories.futures_data_repository import FuturesDataRepository
from src.settings import logger


class FuturesDataService:
    def __init__(self, futures_data_repository: FuturesDataRepository):
        self.futures_data_repository = futures_data_repository

    def make_dataframe(self, asset_name: str, trade_dates: list[date]) -> pd.DataFrame:
        """
        指定された資産名と複数の取引日に基づいてデータを取得し、PandasのDataFrameに変換します。
        各行には取引日（trade_date）列も追加されます。

        :param asset_name: 資産名
        :param trade_dates: 取引日のリスト
        :return: FuturesDataEntityのリストをDataFrameに変換したもの。各行には取引日も含まれます。
        """
        dfs = []
        try:
            if not asset_name or not trade_dates:
                raise InvalidInputError("資産名または取引日が指定されていません。")

            for trade_date in trade_dates:
                futures_data_entities: list[FuturesDataEntity] = self.futures_data_repository.fetch_by_asset_and_date(asset_name, trade_date)

                if futures_data_entities:
                    # FuturesDataEntityのリストからDataFrameを作成
                    temp_df = pd.DataFrame([{
                        'trade_date': entity.trade_date.to_date(),
                        'month': entity.month.to_datetime(),
                        'settle': entity.settle,
                        'volume': entity.volume,
                        'open_interest': entity.open_interest
                    } for entity in futures_data_entities])

                    dfs.append(temp_df)

            if dfs:
                # 複数のDataFrameを結合
                return pd.concat(dfs, ignore_index=True)
            else:
                # データが見つからない場合は空のDataFrameを返す
                return pd.DataFrame()

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


    def add_settlement_spread(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        DataFrameに清算値のスプレッドを追加します。
        DataFrameはtrade_dateとmonthでソートされ、同じtrade_dateの各monthで差を取ります。

        :param df: DataFrame
        :return: スプレッドを追加したDataFrame
        """

        required_columns = ['trade_date', 'month', 'settle']
        if df.empty:
            raise DataFrameValidationError("入力されたDataFrameは空です。")

        # 必要なカラムのチェック
        if not all(column in df.columns for column in required_columns):
            missing_columns = [column for column in required_columns if column not in df.columns]
            raise DataFrameValidationError(f"必要なカラムが不足しています: {missing_columns}")

        if df['month'].dtype != 'datetime64[ns]':
            raise DataFrameValidationError("monthカラムのデータ型がdatetime64[ns]ではありません。")

        try:
            # DataFrameをtrade_dateとmonthでソート
            df = df.sort_values(by=['trade_date', 'month']) # type: ignore

            # 各trade_dateごとにスプレッドを計算
            df['settle_spread'] = df.groupby('trade_date')['settle'].diff().fillna(0) # type: ignore

            return df

        except Exception as e:
            # 予期せぬエラーのキャッチと処理
            logger.error(f"DataFrameの処理中にエラーが発生しました: {e}")
            raise DataFrameValidationError(f"DataFrameの処理中にエラーが発生しました: {e}")
