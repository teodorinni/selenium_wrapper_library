import time
import platform

from selenium.webdriver import Keys


def retry_function_until_success(function, wait_time: float, retry_interval: float) -> bool:
    remaining_time = wait_time
    while remaining_time > 0:
        try:
            function()
            return True
        except:
            if remaining_time > retry_interval:
                time.sleep(retry_interval)
                remaining_time -= retry_interval
            else:
                time.sleep(remaining_time)
                remaining_time = 0
    return False


def get_os_name():
    return platform.system()


def get_control_or_command_for_current_os():
    os_name = get_os_name()
    if os_name == "Darwin":
        return Keys.COMMAND
    else:
        return Keys.CONTROL
