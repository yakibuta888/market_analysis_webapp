import json
import pytest
from datetime import datetime, timezone

import pandas as pd
from bs4 import BeautifulSoup
from pandas.testing import assert_frame_equal
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Generator, Any
from unittest.mock import Mock, MagicMock, patch, mock_open

from src.domain.services.asset_service import AssetService
from src.domain.services.settlement_service import SettlementService
from src.domain.repositories.asset_repository import AssetRepository
from src.infrastructure.scraping.cme_scraper import scrape_settlements, _fetch_asset_ids_urls, _parse_settlements_table


@pytest.fixture
def settlements_html():
    return """
    <table class="main-table-wrapper">
        <tbody>
            <tr>
                <td>Jan</td><td>1</td><td>2</td><td>3</td><td>4</td><td>+1</td><td>5</td><td>100</td><td>200</td>
            </tr>
        </tbody>
    </table>
    """

def test_parse_settlements_table(settlements_html: str):
    soup = BeautifulSoup(settlements_html, 'html.parser')
    results = list(_parse_settlements_table(soup))
    expected = [{
        'month': 'Jan', 'open': '1', 'high': '2', 'low': '3', 'last': '4',
        'change': '+1', 'settle': '5', 'est_volume': '100', 'prior_day_oi': '200'
    }]
    assert results == expected, "Parsed data does not match expected output."


@pytest.fixture
def mock_urls_config():
    return {
        "crude_oil": {
            "settlements": "https://example.com/crude_oil/settlements",
            "volume_and_open_interest": "https://example.com/crude_oil/volume"
        }
    }

@pytest.fixture
def mock_asset_repository():
    return Mock(spec=AssetRepository)

@pytest.fixture
def mock_asset_service(mock_asset_repository: Mock) -> AssetService:
    # このモックは、アセット名からアセットIDを取得する際に使用します。
    service = AssetService(mock_asset_repository)
    service.fetch_asset_id = lambda asset: {"crude_oil": 1}[asset]
    return service


def test_fetch_asset_ids_urls(mock_urls_config: dict[str, dict[str, str]], mock_asset_service: AssetService):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_urls_config))) as mock_file, \
         patch("os.path.join", return_value="fake_path/urls.json"):
        result = _fetch_asset_ids_urls('settlements', mock_asset_service)
        expected = {1: "https://example.com/crude_oil/settlements"}
        assert result == expected, "The function did not return the expected asset ID to URL mapping."


# WebDriverのモックと、モック化されたWebページのHTMLを返すための設定
@pytest.fixture
def mock_webdriver():
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
        mock_driver = Mock(spec=WebDriver)
        # mock_driverのpage_source属性を設定
        mock_driver.page_source = "<html>ダミーのHTMLコンテンツ</html>"

        # GetElementのモックを設定し、css_all_elementsが返す値を設定
        mock_get_element = Mock()
        mock_trade_date_element = Mock()
        mock_trade_date_element.text = "2021-01-01"
        mock_final_label_element = Mock()
        mock_final_label_element.text = 'DATA TYPE: PRELIMINARY'

        # css_all_elementsが返すリストを設定
        mock_get_element.css_all_elements.return_value = [mock_trade_date_element]
        mock_get_element.xpath.return_value = mock_final_label_element
        mock_get_element.xpath_all_elements.return_value = [mock_trade_date_element]

        yield mock_driver, mock_get_element

# AssetService, SettlementServiceのモック
@pytest.fixture
def mock_services():
    asset_service = Mock(spec=AssetService)
    settlement_service = Mock(spec=SettlementService)
    # 必要に応じてメソッドの戻り値を設定
    asset_service.fetch_asset_id.return_value = 1
    # 他の必要なメソッドのモックを設定
    settlement_service.check_data_is_latest_or_not_exsist.return_value = None  # DBにデータが存在しないことを模倣
    return asset_service, settlement_service

def test_scrape_settlements_integration(mock_webdriver: Generator[tuple[Mock, Mock], Any, None], mock_services: tuple[Mock, Mock]):
    mock_driver, mock_get_element = mock_webdriver
    asset_service, settlement_service = mock_services

    # _get_downloadable_dates_from_settlementのテストを模倣するために必要なモックを設定
    last_updated_text = '03 May 2024 10:32:00 PM CT'
    mock_get_element.css.return_value.text = last_updated_text  # Mock#css()が呼ばれた後の.textで返す値を設定
    with patch('src.infrastructure.scraping.cme_scraper.GetElement', return_value=mock_get_element):
        with patch('src.infrastructure.scraping.cme_scraper._scrape_settlement_table') as mock_scrape_func:
            mock_scrape_func.return_value = pd.DataFrame({"month": ["Jan"], "open": ["100"]})
            with patch('src.infrastructure.scraping.cme_scraper._get_downloadable_dates_from_settlement', return_value=["2021-01-01"]):
                scrape_settlements(asset_service, settlement_service)

        # 確認: _scrape_settlement_table関数が呼ばれたか
        mock_scrape_func.assert_called()

        # SettlementServiceのデータ保存関数が呼び出されたことを確認するための別のアプローチ
        # save_settlements_from_dataframe の呼び出しをキャプチャする
        args, kwargs = settlement_service.save_settlements_from_dataframe.call_args

        # 関数呼び出しの引数を確認
        assert args[0] == 1  # asset_id
        assert args[1] == "2021-01-01"  # trade_date
        assert args[3] == datetime(2024, 5, 4, 3, 32, 0, tzinfo=timezone.utc)

        # DataFrameの内容を比較
        expected_df = pd.DataFrame({"month": ["Jan"], "open": ["100"]})
        assert_frame_equal(args[2], expected_df)  # df

def test_skip_scraping_if_data_is_latest(mock_webdriver: Generator[tuple[Mock, Mock], Any, None], mock_services: tuple[Mock, Mock]):
    asset_service, settlement_service = mock_services

    # モック設定
    settlement_service.check_data_is_latest_or_not_exsist.return_value = True
    with patch('src.infrastructure.scraping.cme_scraper._scrape_settlement_table', MagicMock()) as mock_scrape_table:
        with patch('src.infrastructure.scraping.cme_scraper._get_downloadable_dates_from_settlement', return_value=["2021-01-01"]):
            with patch('src.infrastructure.scraping.cme_scraper._settlement_last_updated_from_web', return_value='03 May 2024 10:32:00 PM CT'):
                scrape_settlements(asset_service, settlement_service)

            # データベースが最新であることのチェックが行われたことを確認
            settlement_service.check_data_is_latest_or_not_exsist.assert_called_once()

            # _scrape_settlement_table が呼び出されないことを確認
            mock_scrape_table.assert_not_called()
