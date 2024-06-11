import logging
import os

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from src.selenium_wrapper.webdriver.WebDriverSingleton import WebDriverSingleton


class Page:
    __DEFAULT_TIME_OUT_SECONDS = float(os.getenv("DEFAULT_TIME_OUT_SECONDS"))

    def __init__(self):
        self.__driver = WebDriverSingleton.get_driver()

    # Actions
    def open_page(self, url: str):
        logging.info(f"Opening page with URL: {url}")
        self.__driver.get(url)
        self.__driver.maximize_window()

    @staticmethod
    def close_browser():
        logging.info(f"Closing browser")
        WebDriverSingleton.close_driver()

    def refresh_page(self):
        logging.info(f"Refreshing the current page with URL: {self.get_url()}")
        self.__driver.refresh()

    def close_page(self):
        logging.info(f"Closing the current page with URL: {self.get_url()}")
        self.__driver.close()

    def go_back(self):
        logging.info("Going back to the previous page")
        self.__driver.back()

    def go_forward(self):
        logging.info("Going forward to the next page")
        self.__driver.forward()
        return self

    def get_cookies(self) -> list[dict]:
        logging.info("Getting cookies")
        return self.__driver.get_cookies()

    def clear_cookies(self):
        logging.info("Clearing cookies")
        self.__driver.delete_all_cookies()

    def make_screenshot(self, file_path: str):
        logging.info(f"Making screenshot of the page with URL: {self.get_url()}. Saving the screenshot to {file_path}")
        return self.__driver.get_screenshot_as_file(file_path)

    def make_screenshot_as_png(self):
        logging.info(f"Making screenshot of the page with URL as PNG: {self.get_url()}")
        return self.__driver.get_screenshot_as_png()

    def get_url(self):
        logging.info("Getting the URL of the current page")
        return self.__driver.current_url

    def switch_to_last_window(self):
        logging.info("Switching to the last window of the browser")
        current_window = self.__driver.current_window_handle
        all_windows: list = self.__driver.window_handles
        if current_window == all_windows[0]:
            self.__driver.switch_to.window(all_windows[len(all_windows) - 1])

    def switch_to_first_window(self):
        logging.info("Switching to the first window of the browser")
        all_windows: list = self.__driver.window_handles
        if len(all_windows) > 1:
            self.__driver.switch_to.window(all_windows[0])

    def execute_javascript(self, script, *args):
        logging.info(f"Executing javascript: {script} with arguments: {args}")
        return self.__driver.execute_script(script, *args)

    def scroll_page_to_top(self):
        logging.info("Scrolling the current page to top")
        return self.execute_javascript("window.scrollTo(0, 0);")

    def scroll_page_to_bottom(self):
        logging.info("Scrolling the current page to bottom")
        return self.execute_javascript("window.scrollTo(0, document.body.scrollHeight)")

    def open_page_in_new_tab(self, url: str):
        logging.info(f"Opening page in new tab with URL: {url}")
        return self.execute_javascript("window.open('{}');".format(url))

    def close_last_tab(self):
        logging.info("Closing last tab of the browser")
        all_windows: list = self.__driver.window_handles
        if len(all_windows) > 1:
            self.__driver.switch_to.window(all_windows[len(all_windows) - 1])
            self.__driver.close()
            self.__driver.switch_to.window(all_windows[len(all_windows) - 2])

    def accept_alert(self):
        logging.info("Accepting the alert")
        Alert(self.__driver).accept()

    def dismiss_alert(self):
        logging.info("Dismissing the alert")
        Alert(self.__driver).dismiss()

    def send_keys_to_alert(self, text: str):
        logging.info("Sending keys to the alert")
        Alert(self.__driver).send_keys(text)

    def get_alert_text(self):
        text = Alert(self.__driver).text
        logging.info(f"Getting text from the Alert. Returning '{text}'")
        return text

    # Waits
    def wait_for_number_of_windows_to_be(self, number_of_windows: int, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting for number of windows to be: {number_of_windows}. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.number_of_windows_to_be(number_of_windows))

    def wait_until_title_contains_text(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting for the title of the current page to contain text: {text}. Timeout set to {timeout} "
                     f"seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.title_contains(text))

    def wait_for_title_to_be(self, title: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting for the title of the current page to be: {title}. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.title_is(title))

    def wait_until_url_changes(self, expected_url: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting until the URL of the current page changes to: {expected_url}. Timeout set to {timeout}"
                     f" seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.url_changes(expected_url))

    def wait_until_url_contains(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting until the URL of the current page contains text: {text}. Timeout set to {timeout} "
                     f"seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.url_contains(text))

    def wait_until_url_matches_pattern(self, pattern: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting until the URL of the current page matches the pattern: {pattern}. Timeout set to "
                     f"{timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.url_matches(pattern))

    def wait_for_url_to_be(self, expected_url: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(f"Waiting until the URL of the current page is: {expected_url}. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.url_to_be(expected_url))

    def wait_for_ajax_requests_to_finish(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info("Waiting for all Ajax queries to finish")
        return self.__get_web_driver_wait(timeout).until(lambda d: d.execute_script("document.readyState == 'complete'"))

    # WebDriver related
    @staticmethod
    def __get_web_driver_wait(timeout=__DEFAULT_TIME_OUT_SECONDS) -> WebDriverWait:
        return WebDriverWait(WebDriverSingleton.get_driver(), timeout)

    @staticmethod
    def _get_web_driver() -> WebDriver:
        return WebDriverSingleton.get_driver()
