# coding: utf-8

# Created by BigCookie233

import importlib
import logging
from concurrent.futures import ThreadPoolExecutor

import atexit

thread_pool = None


def init():
    global thread_pool
    config = importlib.import_module(name="Lib.Configs").GlobalConfig()
    thread_pool = ThreadPoolExecutor(max_workers=config.max_workers)


def async_task(func):
    def wrapper(*args, **kwargs):
        if isinstance(thread_pool, ThreadPoolExecutor):
            return thread_pool.submit(func, *args, **kwargs)

    return wrapper


@atexit.register
def shutdown():
    if isinstance(thread_pool, ThreadPoolExecutor):
        logging.info("Closing Thread Pool")
        thread_pool.shutdown()


init()