# src/infrastructure/scraping/cme_scraper.py
import json
import os
import pandas as pd
import requests
import time
from typing import Generator

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.domain.helpers.path import get_project_root
from src.domain.services.asset_service import AssetService
from src.domain.services.settlement_service import SettlementService
from src.domain.services.volume_oi_service import VolumeOIService
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


def _parse_volume_oi_table(soup: BeautifulSoup) -> Generator[dict[str, str], None, None]:
    trs = soup.select('.multiline .main-table-wrapper tbody > tr')
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
            'change': tr.select_one('td:last-of-type').text
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


def _get_downloadable_dates_from_settlement(driver: WebDriver, get_element: GetElement) -> list[str]:
    trade_date_button = get_element.xpath('//label[contains(text(), "Trade date")]/parent::div/div/button')
    driver.execute_script("arguments[0].click();", trade_date_button)  # type: ignore
    date_lists = get_element.css_all_elements('.trade-date-row .simplebar-content .link')
    return [date.text for date in date_lists]


def _get_downloadable_dates_from_volume_oi(driver: WebDriver, get_element: GetElement) -> list[str]:
    trade_date_button = get_element.xpath('//label[contains(text(), "Trade Date")]/parent::div/div/button')
    driver.execute_script("arguments[0].click();", trade_date_button)  # type: ignore
    date_lists = get_element.xpath_all_elements('//label[contains(text(), "Trade Date")]/parent::div//a')
    return [date.text for date in date_lists]


def _settlement_web_data_is_final(driver: WebDriver, get_element: GetElement) -> bool:
    final_label_element = get_element.xpath('//h4[contains(@class, "data-type")]')
    logger.info(final_label_element.text)
    return 'FINAL' in final_label_element.text


def _volume_oi_web_data_is_final(driver: WebDriver, get_element: GetElement) -> bool:
    final_label_element = get_element.xpath('//h5[contains(@class, "data-type")]')
    logger.info(final_label_element.text)
    return 'FINAL' in final_label_element.text


def _scrape_settlement_table(driver: WebDriver, get_element: GetElement, date: str) -> pd.DataFrame:
    date_button = get_element.xpath(f'//a[contains(text(), "{date}")]')
    driver.execute_script("arguments[0].click();", date_button)  # type: ignore
    time.sleep(3)

    get_element_for_load_all = GetElement(driver, retries_count=0, error_handling=False)
    try:
        load_all_button = get_element_for_load_all.xpath('//button[contains(@class, "load-all")]')
        driver.execute_script("arguments[0].click();", load_all_button) # type: ignore
    except Exception:
        logger.debug('Load all button not found.')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    return pd.DataFrame(list(_parse_settlements_table(soup)))


def _scrape_volume_oi_table(driver: WebDriver, get_element: GetElement, date: str) -> pd.DataFrame:
    date_button = get_element.xpath(f'//a[contains(text(), "{date}")]')
    driver.execute_script("arguments[0].click();", date_button)  # type: ignore
    time.sleep(3)

    get_element_for_load_all = GetElement(driver, retries_count=0, error_handling=False)
    try:
        load_all_button = get_element_for_load_all.xpath('//button[contains(@class, "load-all")]')
        driver.execute_script("arguments[0].click();", load_all_button) # type: ignore
    except Exception:
        logger.debug('Load all button not found.')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    return pd.DataFrame(list(_parse_volume_oi_table(soup)))


def scrape_settlements(asset_service: AssetService, settlement_service: SettlementService):
    # `settlements` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # ここでDataFrameを作成し、データを永続化するサービスに渡す
    logger.info('Scraping settlements data...')
    webdriver_setup = WebDriverSetup(headless=False)
    driver = webdriver_setup.get_driver()
    get_element = GetElement(driver)

    asset_ids_urls = _fetch_asset_ids_urls('settlements', asset_service)
    try:
        for asset_id, url in asset_ids_urls.items():
            logger.info(f'Scraping data for asset ID: {asset_id} - URL: {url}')
            driver.get(url)
            time.sleep(3)

            downloadable_dates = _get_downloadable_dates_from_settlement(driver, get_element)
            logger.info(downloadable_dates)

            for date in downloadable_dates:
                data_is_final = settlement_service.check_data_is_final(asset_id, date)

                if data_is_final is None:
                    logger.info(f'No data found for asset ID: {asset_id} on {date}. Scraping data...')
                    df = _scrape_settlement_table(driver, get_element, date)

                    is_final = _settlement_web_data_is_final(driver, get_element)
                    # TODO: ここでデータを永続化するサービスに渡す
                    logger.info(f'is_final: {is_final}')
                    logger.info(df)
                elif not data_is_final:
                    if _settlement_web_data_is_final(driver, get_element):
                        logger.info(f'Data in Database is preliminary, but web data is final. So, scraping data for asset ID: {asset_id} on {date}...')
                        df = _scrape_settlement_table(driver, get_element, date)

                        # TODO: ここでデータを更新するサービスに渡す
                        logger.info(df)

            # TODO: breakは開発中のみ。全てのアセットを取得する場合はコメントアウトする。
            break
        else:
            logger.info('settlements data is up to date.')
    finally:
        driver.quit()


def scrape_volume_and_open_interest(asset_service: AssetService, volume_oi_service: VolumeOIService):
    # `volume_and_open_interest` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # このページのテーブル構造は `settlements` と異なるため、異なる処理が必要
    logger.info('Scraping volume and open interest data...')
    webdriver_setup = WebDriverSetup(headless=False)
    driver = webdriver_setup.get_driver()
    get_element = GetElement(driver)

    asset_ids_urls = _fetch_asset_ids_urls('volume_and_open_interest', asset_service)
    try:
        for asset_id, url in asset_ids_urls.items():
            logger.info(f'Scraping data for asset ID: {asset_id} - URL: {url}')
            driver.get(url)
            time.sleep(3)

            downloadable_dates = _get_downloadable_dates_from_volume_oi(driver, get_element)
            logger.info(downloadable_dates)

            for date in downloadable_dates:
                data_is_final = volume_oi_service.check_data_is_final(asset_id, date)

                if data_is_final is None:
                    logger.info(f'No data found for asset ID: {asset_id} on {date}. Scraping data...')
                    df = _scrape_volume_oi_table(driver, get_element, date)

                    is_final = _volume_oi_web_data_is_final(driver, get_element)
                    # TODO: ここでデータを永続化するサービスに渡す
                    logger.info(f'is_final: {is_final}')
                    logger.info(df)
                elif not data_is_final:
                    if _volume_oi_web_data_is_final(driver, get_element):
                        logger.info(f'Data in Database is preliminary, but web data is final. So, scraping data for asset ID: {asset_id} on {date}...')
                        df = _scrape_volume_oi_table(driver, get_element, date)

                        # TODO: ここでデータを更新するサービスに渡す
                        logger.info(df)

            # TODO: breakは開発中のみ。全てのアセットを取得する場合はコメントアウトする。
            break
        else:
            logger.info('volume and open interest data is up to date.')
    finally:
        driver.quit()
