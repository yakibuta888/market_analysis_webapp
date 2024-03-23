# src/infrastructure/scraping/web_driver_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSetup:
    def __init__(self, headless: bool=False):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless') # type: ignore
        self.options.add_argument('--no-sandbox') # type: ignore
        self.options.add_argument('--disable-dev-shm-usage') # type: ignore
        self.options.add_argument('--disable-gpu') # type: ignore
        self.options.add_argument('--disable-extensions') # type: ignore

    def get_driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.options)
        driver.implicitly_wait(3)  # 指定したドライバーが見つかるまでの待ち時間を設定
        return driver
