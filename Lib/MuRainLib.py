#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

"""
MuRainLib
用于MuRain Bot框架
"""
import atexit
import hashlib
import logging
import os
import sys
import requests
import shutil
import time
import random
from collections import OrderedDict
import Lib.Logger as Logger

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")
cache_path = os.path.join(data_path, "cache")
logger = Logger.logger


class LimitedSizeDict(OrderedDict):
    def __init__(self, max_size):
        self._max_size = max_size
        super().__init__()

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        elif len(self) >= self._max_size:
            oldest_key = next(iter(self))
            del self[oldest_key]
        super().__setitem__(key, value)


def restart() -> None:
    # 获取当前解释器路径
    p = sys.executable
    try:
        # 启动新程序(解释器路径, 当前程序)
        os.execl(p, p, *sys.argv)
    except OSError:
        # 关闭当前程序
        sys.exit()


def download_file_to_cache(url: str, headers=None, file_name: str = "",
                           download_path: str = None, stream=False, fake_headers: bool = True) -> str | None:
    if headers is None:
        headers = {}

    if fake_headers:
        headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42")
        headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7,ko;q=0.6"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Accept"] = ("text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                             "application/signed-exchange;v=b3;q=0.7")
        headers["Connection"] = "keep-alive"
        headers["Upgrade-Insecure-Requests"] = "1"
        headers["Cache-Control"] = "max-age=0"
        headers["Sec-Fetch-Dest"] = "document"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "none"
        headers["Sec-Fetch-User"] = "?1"
        headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"113\""
        headers["Sec-Ch-Ua-Mobile"] = "?0"
        headers["Sec-Ch-Ua-Platform"] = "\"Windows\""
        headers["Host"] = url.split("/")[2]

    # 路径拼接
    flag = False
    if file_name == "":
        file_name = hex(int(hash(url.split("/")[-1]) + random.randint(10000, 99999) + time.time()))[2:] + ".cache"
    else:
        flag = True

    if download_path is None:
        file_path = os.path.join(cache_path, file_name)
    else:
        file_path = os.path.join(download_path, file_name)

    # 路径不存在特判
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    try:
        # 下载
        if stream:
            with open(file_path, "wb") as f, requests.get(url, stream=True, headers=headers) as res:
                for chunk in res.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        break
                    f.write(chunk)
        else:
            # 不使用流式传输
            res = requests.get(url, headers=headers)

            with open(file_path, "wb") as f:
                f.write(res.content)
    except requests.exceptions.RequestException as e:
        logging.warning(f"下载文件失败: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return None

    if not flag:
        # 计算MD5
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
            rename = md5_hash.hexdigest() + ".cache"
            rename_path = os.path.join(cache_path, rename)

        # 重命名（MD5）
        if os.path.exists(rename_path):
            os.remove(rename_path)

        os.rename(file_path, rename_path)

        return rename_path
    else:
        return file_path


# 删除缓存文件
def clean_cache() -> None:
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path, ignore_errors=True)
        except Exception as e:
            logging.warning("删除缓存时报错，报错信息: %s" % repr(e))


# 函数缓存
def function_cache(max_size: int, expiration_time: int = -1):
    cache = LimitedSizeDict(max_size)

    def cache_decorator(func):
        def wrapper(*args, **kwargs):
            key = str(func.__name__) + str(args) + str(kwargs)
            if key in cache and (expiration_time == -1 or time.time() - cache[key][1] < expiration_time):
                return cache[key][0]
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        def clear_cache():
            """清理缓存"""
            cache.clear()

        def get_cache():
            """获取缓存"""
            return dict(cache)

        def original_func(*args, **kwargs):
            """调用原函数"""
            return func(*args, **kwargs)

        wrapper.clear_cache = clear_cache
        wrapper.get_cache = get_cache
        wrapper.original_func = original_func
        return wrapper

    return cache_decorator


# 结束运行
@atexit.register
def finalize_and_cleanup():
    logger.info("MuRainBot即将关闭，正在删除缓存")

    clean_cache()

    logger.warning("MuRainBot结束运行！")
    logger.info("再见！\n")
    os._exit(0)
