import time
import platform

from selenium.common import WebDriverException
from selenium.webdriver import Keys


def retry_function_until_success(function, wait_time: float, retry_interval: float) -> bool:
    retries = int(wait_time/retry_interval)
    for i in range(retries):
        try:
            function()
            return True
        except WebDriverException:
            time.sleep(retry_interval)
        finally:
            return False


def get_os_name():
    return platform.system()


def get_control_or_command_for_current_os():
    os_name = get_os_name()
    if os_name == "Darwin":
        return Keys.COMMAND
    else:
        return Keys.CONTROL
