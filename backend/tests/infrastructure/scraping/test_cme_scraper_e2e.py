# tests/infrastructure/scraping/test_cme_scraper_e2e.py
import pytest
from datetime import date
from sqlalchemy.orm import Session
from typing import Generator

from src.infrastructure.scraping import cme_scraper
from src.domain.entities.asset_entity import AssetEntity
from src.domain.services.asset_service import AssetService
from src.domain.services.settlement_service import SettlementService
from src.domain.services.volume_oi_service import VolumeOIService
from src.domain.value_objects.name import Name
from src.domain.exceptions.element_not_found_error import ElementNotFoundError
from src.infrastructure.database.models import Asset as AssetModel
from src.infrastructure.database.models import Settlement as SettlementModel
from src.infrastructure.database.models import VolumeOI as VolumeOIModel
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.mysql.settlement_repository_mysql import SettlementRepositoryMysql
from src.infrastructure.mysql.volume_oi_repository_mysql import VolumeOIRepositoryMysql
from src.settings import logger


@pytest.fixture(scope="function")
def asset_service(test_session: Session) -> AssetService:
    return AssetService(AssetRepositoryMysql(test_session))


@pytest.fixture(scope="function")
def settlement_service(test_session: Session) -> SettlementService:
    return SettlementService(SettlementRepositoryMysql(test_session))


@pytest.fixture(scope="function")
def volume_oi_service(test_session: Session) -> VolumeOIService:
    return VolumeOIService(VolumeOIRepositoryMysql(test_session))


@pytest.fixture(scope="function")
def test_setup(asset_service: AssetService, test_session: Session):
    # テストデータベースに必要なアセットを挿入
    asset_service.add_asset('crude_oil')
    asset_service.add_asset('gold')
    asset_service.add_asset('russian_ruble')

    yield

    # テストデータベースから関連するsettlementsとvolume_oiレコードを削除
    test_session.query(SettlementModel).delete()
    test_session.query(VolumeOIModel).delete()
    test_session.commit()

    # テストデータベースからアセットを削除
    asset_service.remove_asset('crude_oil')
    asset_service.remove_asset('gold')
    asset_service.remove_asset('russian_ruble')



def test_e2e_scrape_to_database(asset_service: AssetService, settlement_service: SettlementService, volume_oi_service: VolumeOIService, test_session: Session, test_setup: None):
    try:
        # スクレイピング処理の実行
        cme_scraper.scrape_settlements(asset_service, settlement_service)
        cme_scraper.scrape_volume_and_open_interest(asset_service, volume_oi_service)

        # データベースにデータが正しく保存されたか検証
        settlements = test_session.query(SettlementModel).all()
        assert len(settlements) > 0

        # 保存されたデータの具体的な内容を検証
        # 例：特定のsettlementのデータが期待通りであることを確認
        # NOTE: 実際のデータは5日程度で使えなくなるため、リリース前にテストを実行すること
        # specific_settlement = test_session.query(SettlementModel).filter_by(asset_id=1, trade_date=date(2024, 3, 25)).first()
        # assert specific_settlement is not None
        # assert specific_settlement.month == '2024-05'
        # assert specific_settlement.settle == 81.95

        volume_ois = test_session.query(VolumeOIModel).all()
        assert len(volume_ois) > 0
    except ElementNotFoundError as e:
        pytest.fail(f"Unexpected error occurred: {str(e)}")
