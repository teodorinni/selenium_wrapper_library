from selenium.webdriver.common.by import By

from framework.ui.element.WrappedElement import WrappedElement


class Element:

    # Instantiation Strategies

    @staticmethod
    def by_xpath(xpath: str):
        return WrappedElement(By.XPATH, xpath)

    @staticmethod
    def by_css(css: str):
        return WrappedElement(By.CSS_SELECTOR, css)

    @staticmethod
    def by_class_name(class_name: str):
        return WrappedElement(By.CLASS_NAME, class_name)

    @staticmethod
    def by_id(element_id: str):
        return WrappedElement(By.ID, element_id)

    @staticmethod
    def by_name(name: str):
        return WrappedElement(By.NAME, name)

    @staticmethod
    def by_link_text(link_text: str):
        return WrappedElement(By.NAME, link_text)

    @staticmethod
    def by_partial_link_text(partial_link_text: str):
        return WrappedElement(By.PARTIAL_LINK_TEXT, partial_link_text)

    @staticmethod
    def by_tag_name(tag_name: str):
        return WrappedElement(By.TAG_NAME, tag_name)
