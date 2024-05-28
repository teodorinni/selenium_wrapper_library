from framework.ui.webdriver.WebDriverFactory import WebDriverFactory


class WebDriverSingleton:

    driver = None

    @staticmethod
    def get_driver():
        if WebDriverSingleton.driver is None:
            WebDriverSingleton.driver = WebDriverFactory.get_web_driver()
        return WebDriverSingleton.driver

    @staticmethod
    def close_driver():
        if WebDriverSingleton.driver is not None:
            WebDriverSingleton.driver.quit()
            WebDriverSingleton.driver = None
