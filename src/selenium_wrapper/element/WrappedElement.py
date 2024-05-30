import logging
import os

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium_wrapper.webdriver.WebDriverSingleton import WebDriverSingleton
from src.selenium_wrapper.generic import (get_control_or_command_for_current_os)


class WrappedElement:
    __DEFAULT_TIME_OUT_SECONDS = float(os.getenv("DEFAULT_TIME_OUT_SECONDS"))

    def __init__(self, by, locator, web_element: WebElement = None):
        self.__driver = WebDriverSingleton.get_driver()
        self.__by = by
        self.__locator = locator
        self.__web_element = web_element

    # Actions

    def click(self):
        self.__get_web_driver_actions().click(self.wait_for_presence()).perform()
        logging.info(f"Clicking the Element located by {self.__by}: '{self.__locator}'")

    def double_click(self):
        self.__get_web_driver_actions().double_click(self.wait_for_presence()).perform()
        logging.info(f"Double clicking the Element located by {self.__by}: '{self.__locator}'")

    def click_js(self):
        self.execute_javascript("arguments[0].click();", self.__get_web_element())
        logging.info(f"JS clicking  the Element located by {self.__by}: '{self.__locator}'")

    def click_invisible_element(self):
        script: str = ("var object = arguments[0];var theEvent = document.createEvent(\"MouseEvent\");"
                       "theEvent.initMouseEvent(\"click\", true, true, window, 0, 0, 0, 0, 0, false, false, false, "
                       "false, 0, null);object.dispatchEvent(theEvent);")
        self.execute_javascript(script, self.__get_web_element())
        logging.info(f"Clicking the invisible Element located by {self.__by}: '{self.__locator}'")

    def mouse_over(self):
        self.__get_web_driver_actions().move_to_element(self.wait_for_presence()).perform()
        logging.info(f"Hovering over the Element located by {self.__by}: '{self.__locator}'")

    def mouse_down(self):
        self.__get_web_driver_actions().click_and_hold(self.wait_for_presence())
        logging.info(f"Clicking and holding LMB on the Element located by {self.__by}: '{self.__locator}'")

    def mouse_up(self):
        self.__get_web_driver_actions().release(self.wait_for_presence())
        logging.info(f"Releasing LMB from the Element located by {self.__by}: '{self.__locator}'")

    def right_click(self):
        self.__get_web_driver_actions().context_click(self.wait_for_presence()).perform()
        logging.info(f"Right clicking the Element located by {self.__by}: '{self.__locator}'")

    def drag_and_drop_to_element(self, element: "WrappedElement"):
        self.__get_web_driver_actions().drag_and_drop(self.wait_for_presence(), element.wait_for_presence()).perform()
        logging.info(
            f"Dragging the Element located by {self.__by}: '{self.__locator}' onto the Element located by "
            f"{element.__by}: '{element.__locator}'")

    def drag_and_drop_by_offset(self, xoffset: int, yoffset: int):
        self.__get_web_driver_actions().drag_and_drop_by_offset(self.wait_for_presence(), xoffset, yoffset).perform()
        logging.info(
            f"Dragging the Element located by {self.__by}: '{self.__locator}' "
            f"by X offset: {xoffset}, Y offset: {yoffset}")

    def key_down(self, key: Keys):
        self.wait_for_presence()
        self.__get_web_driver_actions().key_down(str(key))
        logging.info(f"Pressing and holding the key: '{key}' on the Element located by {self.__by}: '{self.__locator}'")

    def key_up(self, key: Keys):
        self.wait_for_presence()
        self.__get_web_driver_actions().key_up(str(key))
        logging.info(f"Releasing the key: '{key}' from the Element located by {self.__by}: '{self.__locator}'")

    def perform(self):
        self.wait_for_presence()
        self.__get_web_driver_actions().perform()
        logging.info(f"Performing the previously queued actions on the Element located by {self.__by}: "
                     f"'{self.__locator}'")

    def move_by_offset(self, xoffset: int, yoffset: int):
        self.wait_for_presence()
        self.__get_web_driver_actions().move_by_offset(xoffset, yoffset).perform()
        logging.info(f"Moving the mouse by X offset: {xoffset}, Y offset: {yoffset}")

    def move_to_element_with_offset(self, element: "WrappedElement", xoffset: int, yoffset: int):
        self.wait_for_presence()
        (self.__get_web_driver_actions().move_to_element_with_offset(element.wait_for_presence(), xoffset, yoffset)
         .perform())
        logging.info(f"Moving the mouse to the Element located by {self.__by}: '{self.__locator}' with "
                     f"X offset: {xoffset}, Y offset: {yoffset}")

    def scroll_by_offset(self, xoffset: int, yoffset: int):
        self.wait_for_presence()
        self.__get_web_driver_actions().scroll_by_amount(xoffset, yoffset).perform()
        logging.info(f"Scrolling the page by X offset: {xoffset}, Y offset: {yoffset}")

    def scroll_to_element(self, element: "WrappedElement"):
        self.wait_for_presence()
        self.__get_web_driver_actions().scroll_to_element(element.wait_for_presence()).perform()
        logging.info(f"Scrolling the Page to the Element located by {self.__by}: '{self.__locator}'")

    def clear_text(self):
        self.wait_for_presence()
        self.__get_web_element().clear()
        logging.info(f"Clearing the text from the Element located by {self.__by}: '{self.__locator}'")

    def clear_field(self):
        self.wait_for_presence()
        self.send_keys(get_control_or_command_for_current_os() + 'a')
        self.send_keys(Keys.BACKSPACE)
        logging.info(f"Clearing the text from the Element located by {self.__by}: '{self.__locator}'")

    def send_keys(self, *text):
        self.wait_for_presence().send_keys(*text)
        logging.info(f"Typing text: '{''.join(text)}' into the Element located by {self.__by}: '{self.__locator}'")

    def switch_frame(self):
        self.__driver.switch_to.frame(self.__get_web_element())
        logging.info(f"Switching to the Frame located by {self.__by}: '{self.__locator}'")

    def execute_javascript(self, script, *args):
        logging.info(f"Executing javascript: {script} with arguments: {args}")
        return self.__driver.execute_script(script, *args)

    # Get data from element
    def get_attribute(self, attribute: str):
        element_attribute = self.wait_for_presence().get_attribute(attribute)
        logging.info(f"Getting attribute: '{attribute}' from the Element located by {self.__by}: '{self.__locator}'. "
                     f"Returning '{element_attribute}'")
        return element_attribute

    def get_text(self):
        element_text = self.wait_for_presence().text
        logging.info(f"Getting text from the Element located by {self.__by}: '{self.__locator}'. "
                     f"Returning '{element_text}'")
        return element_text

    def get_css_property(self, css_property: str):
        element_css_property = self.wait_for_presence().value_of_css_property(css_property)
        logging.info(f"Getting CSS property: '{css_property}' from the Element located by "
                     f"{self.__by}: '{self.__locator}'. Returning '{element_css_property}'")
        return element_css_property

    def get_class_name(self):
        element_class = self.wait_for_presence().get_attribute("class")
        logging.info(f"Getting class name from the Element located by "
                     f"{self.__by}: '{self.__locator}'. Returning '{element_class}'")
        return element_class

    def get_id(self):
        element_id = self.wait_for_presence().get_attribute("id")
        logging.info(f"Getting id from the Element located by "
                     f"{self.__by}: '{self.__locator}'. Returning '{element_id}'")
        return element_id

    def get_value(self):
        element_value = self.wait_for_presence().get_attribute("value")
        logging.info(f"Getting value from the Element located by "
                     f"{self.__by}: '{self.__locator}'. Returning '{element_value}'")
        return element_value

    def get_size(self) -> dict:
        element_size = self.wait_for_presence().size
        logging.info(f"Getting size from the Element located by {self.__by} '{self.__locator}'. "
                     f"Returning {element_size}")
        return element_size

    def get_height(self):
        element_height = self.get_size()["height"]
        logging.info(f"Getting height from the Element located by {self.__by} '{self.__locator}'. Returning "
                     f"{element_height}")
        return element_height

    def get_width(self):
        element_width = self.get_size()["width"]
        logging.info(f"Getting width from the Element located by {self.__by} '{self.__locator}'. Returning "
                     f"{element_width}")
        return element_width

    # Check states

    def is_present(self) -> bool:
        try:
            self.__get_web_element()
            logging.info(f"Checking presence of the Element located by {self.__by} '{self.__locator}'. Returning True")
            return True
        except NoSuchElementException:
            logging.info(
                f"Checking presence of the Element located by {self.__by} '{self.__locator}'. Returning False")
            return False

    def is_visible(self) -> bool:
        is_element_visible = self.wait_for_presence().is_displayed()
        logging.info(f"Checking visibility of the Element located by {self.__by} '{self.__locator}'. "
                     f"Returning {is_element_visible}")
        return is_element_visible

    def is_clickable(self) -> bool:
        is_element_clickable = self.wait_for_presence().is_enabled()
        logging.info(f"Checking if the Element located by {self.__by} '{self.__locator}' is clickable. "
                     f"Returning {is_element_clickable}")
        return is_element_clickable

    def is_selected(self) -> bool:
        is_element_selected = self.wait_for_presence().is_selected()
        logging.info(f"Checking if the Element located by {self.__by} '{self.__locator}' is selected. "
                     f"Returning {is_element_selected}")
        return is_element_selected

    # Multiple elements

    def get_all_elements(self) -> list["WrappedElement"]:
        web_elements_list = WebDriverSingleton.get_driver().find_elements(self.__by, self.__locator)
        elements_list = []
        if len(web_elements_list) > 0:
            for web_element in web_elements_list:
                elements_list.append(WrappedElement(self.__by, self.__locator, web_element))
            logging.info(f"Getting all elements located by {self.__by} '{self.__locator}'. "
                         f"Returning a list of {len(elements_list)} Elements")
        return elements_list

    # Waits

    def wait_for_presence(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.debug(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be present. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.presence_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_attribute_in_element(self, attribute: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the attribute '{attribute}' to be included in the Element located by {self.__by}: "
            f"'{self.__locator}'. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.element_attribute_to_include(self.__get_element_by_and_locator(), attribute))

    def wait_until_selected(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be selected. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.element_located_to_be_selected(self.__get_element_by_and_locator()))

    def wait_until_clickable(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be clickable. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.element_to_be_clickable(self.__get_element_by_and_locator()))

    def wait_for_visibility(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be visible. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_invisibility(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be invisible. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.invisibility_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_absence(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for the Element located by {self.__by}: '{self.__locator}' to be absent. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.staleness_of(self.__get_web_element()))

    def wait_until_text_is_present_in_element(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for text '{text}' to be present in the Element located by {self.__by}: '{self.__locator}'. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element(self.__get_element_by_and_locator(), text))

    def wait_until_text_is_present_in_attribute(self, attribute: str, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for text '{text}' to be present in the attribute '{attribute}' of the Element located by "
            f"{self.__by}: '{self.__locator}'. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element_attribute(self.__get_element_by_and_locator(), attribute, text))

    def wait_until_text_is_present_in_value(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for text '{text}' to be present in the value of the Element located by {self.__by}: "
            f"'{self.__locator}'. Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element_value(self.__get_element_by_and_locator(), text))

    def wait_for_visibility_of_all_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting all Elements located by {self.__by}: '{self.__locator}' to be visible. Timeout set to {timeout} "
            f"seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_all_elements_located(self.__get_element_by_and_locator()))

    def wait_for_presence_of_all_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for all Elements located by {self.__by}: '{self.__locator}' to be present. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.presence_of_all_elements_located(self.__get_element_by_and_locator()))

    def wait_for_visibility_of_any_of_the_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        logging.info(
            f"Waiting for all Elements located by {self.__by}: '{self.__locator}' to be visible. "
            f"Timeout set to {timeout} seconds")
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_any_elements_located(self.__get_element_by_and_locator()))

    # WebDriver related
    def __get_web_element(self) -> WebElement:
        if self.__web_element is None:
            logging.info(f"Locating Element by {self.__by}: {self.__locator}")
            return WebDriverSingleton.get_driver().find_element(self.__by, self.__locator)
        else:
            return self.__web_element

    @staticmethod
    def __get_web_driver_wait(timeout=__DEFAULT_TIME_OUT_SECONDS) -> WebDriverWait:
        return WebDriverWait(WebDriverSingleton.get_driver(), timeout)

    @staticmethod
    def __get_web_driver_actions() -> ActionChains:
        return ActionChains(WebDriverSingleton.get_driver())

    def __get_element_by_and_locator(self) -> (str, str):
        return self.__by, self.__locator

    def wait_for_visibility_and_click(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        self.wait_for_visibility(timeout)
        self.click()
