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
        self.options.add_argument("--start-maximized") # type: ignore
        self.options.add_argument("--enable-automation") # type: ignore
        self.options.add_argument("--window-size=1280x1696") # type: ignore
        self.options.add_argument("--disable-infobars") # type: ignore
        self.options.add_argument("--disable-browser-side-navigation") # type: ignore
        self.options.add_argument('--ignore-certificate-errors') # type: ignore
        self.options.add_argument('--ignore-ssl-errors') # type: ignore
        self.options.add_argument("--disable-application-cache") # type: ignore
        self.options.add_argument("--hide-scrollbars") # type: ignore
        self.options.add_argument("--enable-logging") # type: ignore
        self.options.add_argument("--log-level=0") # type: ignore
        self.options.add_argument("--single-process") # type: ignore
        self.options.add_argument("--homedir=/tmp") # type: ignore
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3') # type: ignore
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        self.options.add_experimental_option("prefs",prefs) # type: ignore

    def get_driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.options)
        driver.implicitly_wait(3)  # 指定したドライバーが見つかるまでの待ち時間を設定
        return driver
