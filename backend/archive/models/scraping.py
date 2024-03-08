#!/usr/bin/env my_python
# coding: utf-8
"""CMEのサイトから先物の価格テーブルを取得する"""


from datetime import datetime
import json
import logging
import os
import sys
import time

import pandas as pd
from archive.infrastructure.database.database import db_session
from archive.infrastructure.database.database import engine
from archive.infrastructure.database.database import init_db
from archive.models.models import dtype
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from typing import Generator, Dict


logging.basicConfig(level=logging.INFO)


def get_element(driver: webdriver.Chrome, css_selector: str | None = None, xpath: str | None = None, wait_second: int = 20, retries_count: int = 3):
    """
    cssセレクタ、もしくはxpathで要素を指定する。
    リトライして失敗したらエラーメッセージを通知する。成功したらelementを返す。

    Parameters
    ----------
    css_selector : str, default None
        cssセレクタ。（Xpathより優先される）
    xpath : str, default None
        Xpath。キーワード引数を用いること。（引数にcssセレクタがあるときは無視される）
    driver : class, default None（Noneの時はグローバル変数のdriverを代入）
        selenium.webdriverのオブジェクト。
    wait_second : int, default 20
        指定の要素が表示されるまでの待機時間。
    retries_count : int, default 3
        待機時間経過後も要素が表示されない場合のリトライ回数。

    Returns
    -------
    element : class 'selenium.webdriver.remote.webelement.WebElement'
        指定した要素のオブジェクト。

    Raises
    ------
    TimeoutException
        指定の要素が表示されずタイムアウトした場合。
        リトライが全部失敗したときは、"error_log"ディレクトリに
        エラー内容(error)、実行時間、操作中のURL、セレクタ、スクショを記録する。

    Notes
    -----
    cssセレクタは位置引数で指定できる。
    Xpathはキーワード引数を用いることで指定できる。
    cssセレクタとXpathの2つが引数に渡された時はcssセレクタが優先されるため、
    Xpathを利用したいときは、cssセレクタを引数に渡さないこと。

    See Also
    --------
    presence_of_element_located: 指定した要素がDOM上に現れるまで待機する
    visibility_of_element_located: 指定した要素が表示されるまで待機する

    Examples
    --------
    >>> element = get_element('CSSセレクタ', wait_second=待機時間, retries_count=リトライ回数)
    >>> element.click()
    >>> element.text
    >>> element.get_attribute('属性名')
    >>> element.send_keys('入力する文字列')
    >>> element.clear()

    >>> element = get_element('h1.classname')
    >>> print(element.text)
    text

    >>> element = get_element(xpath='//div[@id="id"]/a)
    >>> print(element.get_attribute('href'))
    https://www.example.com

    """

    if css_selector is None:
        method, selector = By.XPATH, xpath
    else:
        method, selector = By.CSS_SELECTOR, css_selector

    error = ''
    for _ in range(retries_count):
        try:
            element = WebDriverWait(driver, wait_second).until(
                EC.presence_of_element_located((method, selector or ''))
            )
        # エラーメッセージを格納する
        except TimeoutException as e:
            error = e
        # 失敗しなかった場合は、ループを抜ける
        else:
            break
    # リトライが全部失敗したときの処理
    else:
        log_dir = os.path.join(os.path.dirname(__file__), 'error_log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        entry_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f'log{entry_time}.txt')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f'{error}\n')
            f.write(
                f'time:{datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}\n'
                f'url:{driver.current_url}\n'
                f'selector:{selector}\n'
            )
            driver.save_screenshot(os.path.join(
                log_dir, f'screenshot{entry_time}.png'))

        # プログラムを強制終了する
        try:
            driver.quit()
            sys.exit(1)
        except Exception as e:
            print(f'エラー:get_element\n{e}')
    return element


class GetTables(object):

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'urls.json'), 'r') as f:
            self.urls = json.load(f)

        logging.info(self.urls)

    def parse(self, soup: BeautifulSoup) -> Generator[Dict[str, str], None, None]:
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

    def to_database(self, df, asset):
        df.to_sql('crude_oil', engine, index=False, if_exists='append', dtype=dtype)

    def get_data(self):

        options = webdriver.ChromeOptions()

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(3)  # implicitly_wait:指定したドライバーが見つかるまでの待ち時間を設定

        for asset, url in self.urls.items():
            driver.get(url)
            time.sleep(3)

            get_element(driver, xpath='//button[contains(@class, "load-all")]').click()

            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')
            df = pd.DataFrame(list(self.parse(soup)))

            self.to_database(df, asset)

            break

        time.sleep(2)

        driver.quit()
