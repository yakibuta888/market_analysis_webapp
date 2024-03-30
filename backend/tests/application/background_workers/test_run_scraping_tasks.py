# tests/application/background_workers/test_run_scraping_tasks.py
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

from src.application.background_workers import run_scraping_tasks

@pytest.fixture
def asset_service_mock():
    return MagicMock()

@pytest.fixture
def settlement_service_mock():
    return MagicMock()

@pytest.fixture
def volume_oi_service_mock():
    return MagicMock()

# サービス生成関数のモック化
@patch('src.application.background_workers.run_scraping_tasks.AssetService')
@patch('src.application.background_workers.run_scraping_tasks.SettlementService')
@patch('src.application.background_workers.run_scraping_tasks.cme_scraper')
def test_run_settlements_scraping_task(cme_scraper_mock: MagicMock, SettlementServiceMock: MagicMock, AssetServiceMock: MagicMock):
    # モックサービスのインスタンスを作成
    mock_asset_service = MagicMock()
    mock_settlement_service = MagicMock()

    # モックファクトリメソッドがモックインスタンスを返すように設定
    AssetServiceMock.return_value = mock_asset_service
    SettlementServiceMock.return_value = mock_settlement_service

    # タスク実行
    run_scraping_tasks.run_settlements_scraping_task()

    # scrape_settlementsがモックサービスインスタンスで呼び出されたことを確認
    cme_scraper_mock.scrape_settlements.assert_called_once_with(mock_asset_service, mock_settlement_service)


@patch('src.application.background_workers.run_scraping_tasks.cme_scraper')
@patch('src.application.background_workers.run_scraping_tasks.VolumeOIService')
@patch('src.application.background_workers.run_scraping_tasks.AssetService')
def test_run_volume_oi_scraping_task(AssetServiceMock: MagicMock, VolumeOIServiceMock: MagicMock, cme_scraper_mock: MagicMock):
    # モックサービスインスタンスを作成
    mock_asset_service = MagicMock()
    mock_volume_oi_service = MagicMock()

    # モックファクトリメソッドがモックインスタンスを返すように設定
    AssetServiceMock.return_value = mock_asset_service
    VolumeOIServiceMock.return_value = mock_volume_oi_service

    # タスク実行
    run_scraping_tasks.run_volume_oi_scraping_task()

    # scrape_volume_and_open_interestがモックサービスインスタンスで呼び出されたことを確認
    cme_scraper_mock.scrape_volume_and_open_interest.assert_called_once_with(mock_asset_service, mock_volume_oi_service)


# テストケースでsys.argvをパッチする例
@mock.patch('sys.argv', ['run_scraping_tasks.py', 'settlement'])
def test_main_settlement_task_with_argv():
    # この中でsys.argvは['run_scraping_tasks.py', 'settlement']として模倣される
    with mock.patch('src.application.background_workers.run_scraping_tasks.run_settlements_scraping_task') as mock_task:
        run_scraping_tasks.main()
        mock_task.assert_called_once()


@mock.patch('sys.argv', ['run_scraping_tasks.py', 'volume_oi'])
def test_main_volume_oi_task_with_argv():
    with mock.patch('src.application.background_workers.run_scraping_tasks.run_volume_oi_scraping_task') as mock_task:
        run_scraping_tasks.main()
        mock_task.assert_called_once()
