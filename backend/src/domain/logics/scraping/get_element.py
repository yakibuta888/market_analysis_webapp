# src/domain/logics/scraping/get_element.py
import os
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import Literal

from src.domain.helpers.path import get_project_root
from src.settings import logger


class GetElement:
    """
    cssセレクタ、もしくはxpathで要素を指定する。
    リトライして失敗したらエラーメッセージを通知する。成功したらelementを返す。

    Attributes
    ----------
    driver : class
        selenium.webdriverのオブジェクト。
    wait_second : int, default 20
        指定の要素が表示されるまでの待機時間。
    retries_count : int, default 3
        待機時間経過後も要素が表示されない場合のリトライ回数。

    Methods
    -------
    css(selector: str) -> WebElement
        cssセレクタで要素を指定する。
    xpath(selector: str) -> WebElement
        xpathで要素を指定する。
    _logging_error(error: TimeoutException | Literal[''], selector: str)
        エラーメッセージを記録する。
    _get_element(method: str, selector: str) -> WebElement
        指定した要素を取得する。

    Raises
    ------
    TimeoutException
        指定の要素が表示されずタイムアウトした場合。
        リトライが全部失敗したときは、"error_log"ディレクトリに
        エラー内容(error)、実行時間、操作中のURL、セレクタ、スクショを記録する。
    SystemExit
        プログラムを強制終了する。
    Exception
        プログラムを強制終了する際にエラーが発生した場合。

    Notes
    -----
    driverはselenium.webdriverのオブジェクトを渡す。
    wait_secondは指定の要素が表示されるまでの待機時間を秒で指定する。
    retries_countは待機時間経過後も要素が表示されない場合のリトライ回数を指定する。

    See Also
    --------
    presence_of_element_located: 指定した要素がDOM上に現れるまで待機する
    visibility_of_element_located: 指定した要素が表示されるまで待機する

    Examples
    --------
    >>> driver = webdriver.Chrome()
    >>> get_element = GetElement(driver)
    >>> element = get_element.css('CSSセレクタ', wait_second=待機時間, retries_count=リトライ回数)
    >>> element.click()
    >>> element.text
    >>> element.get_attribute('属性名')
    >>> element.send_keys('入力する文字列')
    >>> element.clear()
    >>> driver.quit()

    >>> driver = webdriver.Chrome()
    >>> get_element = GetElement(driver)
    >>> element = get_element('h1.classname')
    >>> print(element.text)
    text
    >>> element = get_element.xpath(xpath='//div[@id="id"]/a)
    >>> print(element.get_attribute('href'))
    https://www.example.com

    """
    def __init__(self, driver: webdriver.Chrome, wait_second: int = 20, retries_count: int = 3):
        """
        Initialize the GetElement class.

        Parameters
        ----------
        driver : webdriver.Chrome
            The Chrome webdriver instance.
        wait_second : int, default 20
            The number of seconds to wait for an element to be found.
        retries_count : int, default 3
            The number of times to retry finding an element.
        """
        self.driver = driver
        self.wait_second = wait_second
        self.retries_count = retries_count


    def css(self, selector: str) -> WebElement:
        """
        Find and return a web element using CSS selector.

        Parameters
        ----------
        selector : str
            The CSS selector used to locate the web element.

        Returns
        -------
        WebElement
            The web element found using the CSS selector.
        """
        method = By.CSS_SELECTOR
        return self._get_element(method, selector)


    def xpath(self, selector: str) -> WebElement:
        """
        Find and return a web element using XPath.

        Parameters
        ----------
        selector : str
            The XPath used to locate the web element.

        Returns
        -------
        WebElement
            The web element found using the XPath.
        """
        method = By.XPATH
        return self._get_element(method, selector)


    def _logging_error(self, error: TimeoutException | Literal[''], selector: str):
        """
        Log the error details and save a screenshot.

        Parameters
        ----------
        error : TimeoutException | Literal['']
            The error that occurred during scraping.
        selector : str
            The selector used for scraping.

        Returns
        -------
        None
            This method does not return anything.
        """
        progect_root = get_project_root()
        log_dir = os.path.join(progect_root, 'src', 'log', 'error_log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        entry_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f'log{entry_time}.txt')
        screenshot_file = os.path.join(log_dir, f'screenshot{entry_time}.png')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(
                f'{error}\n'
                f'time:{datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}\n'
                f'url:{self.driver.current_url}\n'
                f'selector:{selector}\n'
            )
        self.driver.save_screenshot(screenshot_file)
        logger.error(f'error_logを参照してください\n{error}')


    def _get_element(self, method: str, selector: str):
        """
        Get the element using the specified method and selector.

        Parameters
        ----------
        method : str
            The method to locate the element (e.g., 'css selector', 'xpath').
        selector : str
            The selector used to locate the element.

        Returns
        -------
        element : WebElement
            The located element.

        Raises
        ------
        TimeoutException
            If the element cannot be located within the specified time.
        SystemExit
            If all retry attempts fail and the program needs to be forcefully terminated.

        """
        error = ''
        for _ in range(self.retries_count):
            try:
                element = WebDriverWait(self.driver, self.wait_second).until(
                    EC.presence_of_element_located((method, selector or ''))
                )
            except TimeoutException as e:
                error = e
            # 失敗しなかった場合は、ループを抜ける
            else:
                break
        # リトライが全部失敗したときの処理
        else:
            self._logging_error(error, selector)
            try:
                self.driver.quit()
                logger.error('プログラムを強制終了しました')
                raise SystemExit(1)
            except Exception as e:
                logger.error(f'強制終了エラー:get_element\n{e}')
                raise e
        return element
