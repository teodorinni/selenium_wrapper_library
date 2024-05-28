import os
import urllib3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


os.environ['WDM_SSL_VERIFY'] = '0'
os.environ['WDM_LOCAL'] = '1'
# os.environ['WDM_LOG'] = str(logging.NOTSET)   # Disable webdriver_manager logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebDriverFactory:

    @staticmethod
    def get_web_driver():
        browser = get_browser().lower()
        if browser == "chrome" or not browser:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                      options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif browser == "edge":
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        else:
            raise RuntimeError("Browser not supported. Supported browsers: Chrome, Firefox, Edge")
        return driver


def get_browser():
    return os.getenv("BROWSER")
