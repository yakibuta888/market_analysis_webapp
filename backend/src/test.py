from datetime import date
from sqlalchemy import text

from src.domain.services.asset_service import AssetService
from src.domain.services.settlement_service import SettlementService
from src.domain.services.volume_oi_service import VolumeOIService
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.mysql.futures_data_repository_mysql import FuturesDataRepositoryMysql
from src.infrastructure.mysql.settlement_repository_mysql import SettlementRepositoryMysql
from src.infrastructure.mysql.volume_oi_repository_mysql import VolumeOIRepositoryMysql
from src.infrastructure.database.database import db_session
from src.infrastructure.scraping import cme_scraper


if __name__ == "__main__":
    # asset_service = AssetService(AssetRepositoryMysql(db_session()))
    # settlement_service = SettlementService(SettlementRepositoryMysql(db_session()))
    # volume_oi_service = VolumeOIService(VolumeOIRepositoryMysql(db_session()))

    # futuresdata_repository = FuturesDataRepositoryMysql(db_session())

    # asset_name = 'crude_oil'
    # trade_date = date(2024, 4, 2)

    # result = futuresdata_repository.fetch_by_asset_and_date(asset_name, trade_date)

    # print(result)

    # from src.application.web.api.models.futures_data_model import FuturesDataRequest
    # from pydantic import ValidationError

    # # 正しいデータでのテスト
    # try:
    #     request = FuturesDataRequest(
    #         asset_name="Gold",
    #         trade_dates=["2023-01-01", "2023-01-02"]
    #     )
    #     print(request)
    # except ValidationError as e:
    #     print("バリデーションエラーが発生しました:", e.json())

    # # 不正な日付形式でのテスト
    # try:
    #     request = FuturesDataRequest(
    #         asset_name="Gold",
    #         trade_dates=["2023-01-32"]  # 存在しない日付
    #     )
    #     print(request)
    # except ValidationError as e:
    #     print("バリデーションエラーが発生しました:", e.json())

    # # 資産名が空のテスト
    # try:
    #     request = FuturesDataRequest(
    #         asset_name="",
    #         trade_dates=["2023-01-01"]
    #     )
    #     print(request)
    # except ValidationError as e:
    #     print("バリデーションエラーが発生しました:", e.json())

    import requests

    url = 'https://script.google.com/macros/s/AKfycbxV5HzkXC3ewwAilkcJ4JXxUWMhHK7ICwbcJoL7Z5cY5fHw3CGb89wXcVMITg0JPjf_Tg/exec'
    data = {
        "action": "sendVerificationEmail",
        "email": "ms1kz.hsh5n+test-register@gmail.com",
        "password": "testp@ssw0rd",
        "name": "Test Register"
    }

    response = requests.post(url, json=data)

    print(response.text)
