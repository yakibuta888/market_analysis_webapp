# src/infrastructure/scraping/get_element.py
import os
import traceback
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
    error_handling : bool, default True
        エラー処理を行うかどうか。

    Methods
    -------
    css(selector: str) -> WebElement
        cssセレクタで要素を指定する。
    css_all_elements(selector: str) -> list[WebElement]
        cssセレクタで複数の要素を指定する。
    xpath(selector: str) -> WebElement
        xpathで要素を指定する。
    xpath_all_elements(selector: str) -> list[WebElement]
        xpathで複数の要素を指定する。
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
    >>> element = get_element.css('h1.classname')
    >>> print(element.text)
    text
    >>> element = get_element.xpath('//div[@id="id"]/a')
    >>> print(element.get_attribute('href'))
    https://www.example.com

    """
    def __init__(self, driver: webdriver.Chrome, wait_second: int = 20, retries_count: int = 3, error_handling: bool = True):
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
        error_handling : bool, default True
            Whether to handle errors or not.
        """
        self.driver = driver
        self.wait_second = wait_second
        self.retries_count = retries_count
        self.error_handling = error_handling


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


    def css_all_elements(self, selector: str) -> list[WebElement]:
        """
        Find and return a web elements using CSS selector.

        Parameters
        ----------
        selector : str
            The CSS selector used to locate the web elements.

        Returns
        -------
        list[WebElement]
            The web elements found using the CSS selector.
        """
        method = By.CSS_SELECTOR
        return self._get_elements(method, selector)


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


    def xpath_all_elements(self, selector: str) -> list[WebElement]:
        """
        Find and return a web elements using XPath.

        Parameters
        ----------
        selector : str
            The XPath used to locate the web elements.

        Returns
        -------
        list[WebElement]
            The web elements found using the XPath.
        """
        method = By.XPATH
        return self._get_elements(method, selector)


    def _logging_error(self, error: TimeoutException | Exception, selector: str):
        """
        Log the error details and save a screenshot.

        Parameters
        ----------
        error : TimeoutException | Exception
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

        error_type = type(error).__name__
        error_message = f"message: {str(error)}"
        stack_trace = traceback.format_exc()

        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(
                f'Error Type: {error_type}\n'
                f'{error_message}\n'
                f'Stack Trace:\n{stack_trace}\n'
                f'time: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}\n'
                f'url: {self.driver.current_url}\n'
                f'selector: {selector}\n'
            )
        self.driver.save_screenshot(screenshot_file) # type: ignore
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
        error = Exception('')
        element = None
        for _ in range(self.retries_count + 1):
            try:
                element = WebDriverWait(self.driver, self.wait_second).until(
                    EC.presence_of_element_located((method, selector or ''))
                )
                # 要素が見つかった場合は、ループを抜ける
                break
            except TimeoutException as e:
                error = e
                continue # タイムアウトした場合は、リトライする
            except Exception as e:
                # タイムアウト以外のエラーの場合はループを抜けてエラー処理
                error = e
                break

        if element is None: # 要素が取得できなかった場合
            if self.error_handling:
                self._logging_error(error, selector)
                try:
                    self.driver.quit()
                    logger.error('プログラムを強制終了しました')
                    raise SystemExit(1)
                except Exception as e:
                    logger.error(f'強制終了エラー:get_element\n{e}')
                    raise e
            else:
                raise error

        return element


    def _get_elements(self, method: str, selector: str):
        """
        Get the elements using the specified method and selector.

        Parameters
        ----------
        method : str
            The method to locate the elements (e.g., 'css selector', 'xpath').
        selector : str
            The selector used to locate the elements.

        Returns
        -------
        elements : list[WebElement]
            The located elements.

        Raises
        ------
        TimeoutException
            If the element cannot be located within the specified time.
        SystemExit
            If all retry attempts fail and the program needs to be forcefully terminated.

        """
        error = Exception('')
        elements = None
        for _ in range(self.retries_count + 1):
            try:
                elements = WebDriverWait(self.driver, self.wait_second).until(
                    EC.presence_of_all_elements_located((method, selector or ''))
                )
                # 要素が見つかった場合は、ループを抜ける
                break
            except TimeoutException as e:
                error = e
                continue # タイムアウトした場合は、リトライする
            except Exception as e:
                # タイムアウト以外のエラーの場合はループを抜けてエラー処理
                error = e
                break

        if elements is None: # 要素が取得できなかった場合
            if self.error_handling:
                self._logging_error(error, selector)
                try:
                    self.driver.quit()
                    logger.error('プログラムを強制終了しました')
                    raise SystemExit(1)
                except Exception as e:
                    logger.error(f'強制終了エラー:get_element\n{e}')
                    raise e
            else:
                raise error

        return elements
