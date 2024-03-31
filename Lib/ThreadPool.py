# coding: utf-8

# Created by BigCookie233

from concurrent.futures import ThreadPoolExecutor

import Lib.Configs as Configs

thread_pool = None


def init():
    global thread_pool
    config = Configs.global_config
    thread_pool = ThreadPoolExecutor(max_workers=config.max_workers)


def async_task(func):
    def wrapper(*args, **kwargs):
        if isinstance(thread_pool, ThreadPoolExecutor):
            return thread_pool.submit(func, *args, **kwargs)

    return wrapper
