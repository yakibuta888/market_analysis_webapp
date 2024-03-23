# src/infrastructure/scraping/cme_scraper.py
import json
import os
import pandas as pd
import requests
import time
from typing import Generator

from bs4 import BeautifulSoup

from src.domain.helpers.path import get_project_root
from src.domain.services.asset_service import AssetService
from src.infrastructure.scraping.get_element import GetElement
from src.infrastructure.scraping.web_driver_setup import WebDriverSetup
from src.settings import logger


def _parse_settlements_table(soup: BeautifulSoup) -> Generator[dict[str, str], None, None]:
    trs = soup.select('.main-table-wrapper tbody > tr')
    for tr in trs:
        yield {
            'month': tr.select_one('td:first-of-type').text,
            'open': tr.select_one('td:nth-of-type(2)').text,
            'high': tr.select_one('td:nth-of-type(3)').text,
            'low': tr.select_one('td:nth-of-type(4)').text,
            'last': tr.select_one('td:nth-of-type(5)').text,
            'change': tr.select_one('td:nth-of-type(6)').text,
            'settle': tr.select_one('td:nth-of-type(7)').text,
            'est_volume': tr.select_one('td:nth-of-type(8)').text,
            'prior_day_OI': tr.select_one('td:last-of-type').text
        }


def _parse_volume_and_open_interest_table(soup: BeautifulSoup) -> Generator[dict[str, str], None, None]:
    # TODO: セレクタは仮のものです。実際のページの構造に合わせて修正してください。
    trs = soup.select('.main-table-wrapper tbody > tr')
    for tr in trs:
        yield {
            'month': tr.select_one('td:first-of-type').text,
            'globex': tr.select_one('td:nth-of-type(2)').text,
            'open_outcry': tr.select_one('td:nth-of-type(3)').text,
            'clear_port': tr.select_one('td:nth-of-type(4)').text,
            'total_volume': tr.select_one('td:nth-of-type(5)').text,
            'block_trades': tr.select_one('td:nth-of-type(6)').text,
            'efp': tr.select_one('td:nth-of-type(7)').text,
            'efr': tr.select_one('td:nth-of-type(8)').text,
            'tas': tr.select_one('td:nth-of-type(9)').text,
            'deliveries': tr.select_one('td:nth-of-type(10)').text,
            'at_close': tr.select_one('td:nth-of-type(11)').text,
            'change': tr.select_one('td:nth-of-type(12)').text
        }


def _fetch_asset_ids_urls(table_name: str, asset_service: AssetService) -> dict[int, str]:
    config_path = os.path.join(get_project_root(), 'config', 'urls.json')
    with open(config_path) as f:
        urls_config = json.load(f)

    id_url_dict: dict[int, str] = dict()
    for asset, urls in urls_config.items():
        asset_id = asset_service.fetch_asset_id(asset)  # アセット名に基づいてDBからIDを取得
        url = urls[table_name]
        id_url_dict[asset_id] = url

    return id_url_dict


def scrape_settlements(asset_service: AssetService):
    # `settlements` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # ここでDataFrameを作成し、データを永続化するサービスに渡す
    webdriver_setup = WebDriverSetup(headless=False)
    driver = webdriver_setup.get_driver()
    get_element = GetElement(driver)

    asset_ids_urls = _fetch_asset_ids_urls('settlements', asset_service)
    try:
        for asset_id, url in asset_ids_urls.items():
            driver.get(url)
            time.sleep(3)

            trade_date_button = get_element.xpath('//label[contains(text(), "Trade date")]/parent::div/div/button')
            driver.execute_script("arguments[0].click();", trade_date_button) # type: ignore
            date_lists = get_element.css_all_elements('.trade-date-row .simplebar-content .link')
            downloadable_dates = [date.text for date in date_lists]
            logger.info(downloadable_dates)


            load_all_button = get_element.xpath('//button[contains(@class, "load-all")]')
            driver.execute_script("arguments[0].click();", load_all_button)  # type: ignore

            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            df = pd.DataFrame(list(_parse_settlements_table(soup)))
            # TODO: ここでデータを永続化するサービスに渡す
            logger.info(df)
            # TODO: breakは開発中のみ。全てのアセットを取得する場合はコメントアウトする。
            break
    finally:
        driver.quit()


def scrape_volume_and_open_interest(url, asset_id):
    # `volume_and_open_interest` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # このページのテーブル構造は `settlements` と異なるため、異なる処理が必要
    pass
