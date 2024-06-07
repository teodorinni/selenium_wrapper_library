import time
import platform

from selenium.webdriver import Keys


def retry_function_until_success(function, retry_interval: float, num_retries: int) -> bool:
    for i in range(num_retries):
        try:
            function()
            return True
        except:
            time.sleep(retry_interval)
    return False


def get_os_name():
    return platform.system()


def get_control_or_command_for_current_os():
    os_name = get_os_name()
    if os_name == "Darwin":
        return Keys.COMMAND
    else:
        return Keys.CONTROL
