# src/infrastructure/scraping/cme_scraper.py
import json
import os
import pandas as pd
import requests
import time
from datetime import datetime
from typing import Generator

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.domain.helpers.path import get_project_root
from src.domain.logics.date_time_utilities import parse_datetime
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
            'prior_day_oi': tr.select_one('td:last-of-type').text
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
    config_filename = os.getenv('URLS_CONFIG', 'urls.json')
    config_path = os.path.join(get_project_root(), 'config', config_filename)
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
    trade_dates = get_element.css_all_elements('.trade-date-row .simplebar-content .link')
    return [trade_date.text for trade_date in trade_dates]


def _get_downloadable_dates_from_volume_oi(driver: WebDriver, get_element: GetElement) -> list[str]:
    trade_date_button = get_element.xpath('//label[contains(text(), "Trade Date")]/parent::div/div/button')
    driver.execute_script("arguments[0].click();", trade_date_button)  # type: ignore
    trade_dates = get_element.xpath_all_elements('//label[contains(text(), "Trade Date")]/parent::div//a')
    return [trade_date.text for trade_date in trade_dates]


def _settlement_last_updated_from_web(driver: WebDriver, get_element: GetElement, trade_date: str) -> datetime:
    date_button = get_element.xpath(f'//a[contains(text(), "{trade_date}")]')
    driver.execute_script("arguments[0].click();", date_button)  # type: ignore
    time.sleep(3)

    last_updated_element = get_element.css('.data-information > .timestamp > div')
    last_updated_text = last_updated_element.text.replace('Last Updated ', '')
    logger.info(f'last updated: {last_updated_text}')
    last_updated = parse_datetime(last_updated_text)
    return last_updated


def _volume_oi_web_data_is_final(driver: WebDriver, get_element: GetElement) -> bool:
    final_label_element = get_element.xpath('//h5[contains(@class, "data-type")]')
    logger.info(f'web data is {final_label_element.text}')
    return 'FINAL' in final_label_element.text


def _scrape_settlement_table(driver: WebDriver) -> pd.DataFrame:
    get_element_for_load_all = GetElement(driver, retries_count=0, error_handling=False)
    try:
        load_all_button = get_element_for_load_all.xpath('//button[contains(@class, "load-all")]')
        driver.execute_script("arguments[0].click();", load_all_button) # type: ignore
    except Exception:
        logger.debug('Load all button not found.')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    return pd.DataFrame(list(_parse_settlements_table(soup)))


def _scrape_volume_oi_table(driver: WebDriver, get_element: GetElement, trade_date: str) -> pd.DataFrame:
    date_button = get_element.xpath(f'//a[contains(text(), "{trade_date}")]')
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

            for trade_date in downloadable_dates:
                last_updated = _settlement_last_updated_from_web(driver, get_element, trade_date)
                data_is_latest_or_not_exsist = settlement_service.check_data_is_latest_or_not_exsist(asset_id, trade_date, last_updated)

                if data_is_latest_or_not_exsist is None:
                    logger.info(f'No data found for asset ID: {asset_id} on {trade_date}. Scraping data...')
                    df = _scrape_settlement_table(driver)

                    settlement_service.save_settlements_from_dataframe(asset_id, trade_date, df, last_updated)
                    logger.debug(f'last_updated: {last_updated}')
                    logger.debug(df)
                elif not data_is_latest_or_not_exsist:
                    logger.info(f'Data in Database is not latest, but web data is latest. So, scraping data for asset ID: {asset_id} on {trade_date}...')
                    df = _scrape_settlement_table(driver)

                    settlement_service.update_settlements_from_dataframe(asset_id, trade_date, df, last_updated)
                    logger.debug(f'last_updated: {last_updated}')
                    logger.debug(df)
                else:
                    logger.info(f'Data in Database is latest for asset ID: {asset_id} on {trade_date}.')

            # TODO: breakは開発中のみ。全てのアセットを取得する場合はコメントアウトする。
            # break
        else:
            logger.info(' ﾟ+｡*ﾟ+｡｡+ﾟ*｡+ﾟ settlements data is up to date. ﾟ+｡*ﾟ+｡｡+ﾟ*｡+ﾟ ')
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

            for trade_date in downloadable_dates:
                data_is_final = volume_oi_service.check_data_is_final(asset_id, trade_date)

                if data_is_final is None:
                    logger.info(f'No data found for asset ID: {asset_id} on {trade_date}. Scraping data...')
                    df = _scrape_volume_oi_table(driver, get_element, trade_date)
                    is_final = _volume_oi_web_data_is_final(driver, get_element)

                    volume_oi_service.save_volume_oi_from_dataframe(asset_id, trade_date, df, is_final)
                    logger.debug(f'is_final: {is_final}')
                    logger.debug(df)
                elif not data_is_final:
                    if _volume_oi_web_data_is_final(driver, get_element):
                        logger.info(f'Data in Database is preliminary, but web data is final. So, scraping data for asset ID: {asset_id} on {trade_date}...')
                        df = _scrape_volume_oi_table(driver, get_element, trade_date)

                        volume_oi_service.update_volume_oi_from_dataframe(asset_id, trade_date, df, True)
                        logger.debug(df)
                else:
                    logger.info(f'Data in Database is final for asset ID: {asset_id} on {trade_date}.')

            # TODO: breakは開発中のみ。全てのアセットを取得する場合はコメントアウトする。
            # break
        else:
            logger.info(' ﾟ+｡*ﾟ+｡｡+ﾟ*｡+ﾟ volume and open interest data is up to date. ﾟ+｡*ﾟ+｡｡+ﾟ*｡+ﾟ ')
    finally:
        driver.quit()
