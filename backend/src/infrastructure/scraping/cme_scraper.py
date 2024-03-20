# src/infrastructure/scraping/cme_scraper.py
import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Generator

from src.domain.helpers.path import get_project_root
from src.domain.services.asset_service import AssetService


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


def scrape_settlements(url, asset_id):
    # `settlements` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # ここでDataFrameを作成し、データを永続化するサービスに渡す
    pass

def scrape_volume_and_open_interest(url, asset_id):
    # `volume_and_open_interest` ページからデータをスクレイピングし、DataFrameに格納するロジック
    # このページのテーブル構造は `settlements` と異なるため、異なる処理が必要
    pass
