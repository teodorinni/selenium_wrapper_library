import os
from pathlib import Path

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
        browser = _get_env_transformed("BROWSER")
        headless = _get_env_transformed("HEADLESS")
        if browser == "chrome" or not browser:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            # Path(os.getenv("DOWNLOAD_DIR")).mkdir(parents=True, exist_ok=True)
            options.add_experimental_option("prefs", {"download.default_directory": os.getenv("DOWNLOAD_DIR")})
            if headless in ("true",  "1", "yes", "on", "enabled"):
                options.add_argument("--headless=new")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif browser == "edge":
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        else:
            raise RuntimeError("Browser not supported. Supported browsers: Chrome, Firefox, Edge")
        return driver


def _get_env_transformed(env_var):
    env_var = os.getenv(env_var)
    try:
        env_var = env_var.lower()
    except AttributeError:
        pass
    return env_var
