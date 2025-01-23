# Created by BigCookie233
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from Lib.core.ConfigManager import GlobalConfig
from Lib.utils.Logger import get_logger

import atexit

thread_pool = None
logger = get_logger()


def shutdown():
    global thread_pool
    if isinstance(thread_pool, ThreadPoolExecutor):
        logger.debug("Closing Thread Pool")
        thread_pool.shutdown()
        thread_pool = None


def init():
    global thread_pool
    thread_pool = ThreadPoolExecutor(max_workers=GlobalConfig().thread_pool.max_workers)
    atexit.register(shutdown)


def _wrapper(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # 打印到日志中
        logger.error(
            f"Error in async task({func.__module__}.{func.__name__}): {repr(e)}\n"
            f"{"".join(traceback.format_exception(exc_type, exc_value, exc_traceback))}"
        )


def async_task(func):
    def wrapper(*args, **kwargs):
        if isinstance(thread_pool, ThreadPoolExecutor):
            return thread_pool.submit(_wrapper, func, *args, **kwargs)
        else:
            logger.warning("Thread Pool is not initialized. Please call init() before using it.")
            return func(*args, **kwargs)

    return wrapper

