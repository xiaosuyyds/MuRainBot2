# Created by BigCookie233

from concurrent.futures import ThreadPoolExecutor
from Lib.core.ConfigManager import GlobalConfig
from Lib.utils.Logger import get_logger

import atexit

thread_pool = None
logger = get_logger()


def init():
    global thread_pool
    thread_pool = ThreadPoolExecutor(max_workers=GlobalConfig().thread_pool.max_workers)


def async_task(func):
    def wrapper(*args, **kwargs):
        if isinstance(thread_pool, ThreadPoolExecutor):
            return thread_pool.submit(func, *args, **kwargs)

    return wrapper


@atexit.register
def shutdown():
    if isinstance(thread_pool, ThreadPoolExecutor):
        logger.debug("Closing Thread Pool")
        thread_pool.shutdown()
