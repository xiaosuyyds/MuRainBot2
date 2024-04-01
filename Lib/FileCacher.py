# coding: utf-8

# Created by BigCookie233

import os

import Lib.ThreadPool as ThreadPool

cache = {}


def read_file(path, encoding="utf-8"):
    if path in cache.keys():
        return cache[path]
    with open(path, encoding=encoding) as file:
        cache[path] = file.read()
    return cache[path]


def write_file(path, data, encoding="utf-8"):
    cache[path] = data
    write_file_task(path, data, encoding)


def write_non_existent_file(path, data, encoding="utf-8"):
    cache[path] = data
    write_non_existent_file_task(path, data, encoding)


def write_cache(path, item):
    if path in cache:
        cache[path] = item
    else:
        raise KeyError("Path not found or Not in Cache")


@ThreadPool.async_task
def write_file_task(path, data, encoding="utf-8"):
    with open(path, "w", encoding=encoding) as file:
        file.write(data)


def write_non_existent_file_task(path, data, encoding="utf-8"):
    if not os.path.exists(path):
        write_file_task(path, data, encoding)
