# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

"""
MuRainLib
用于MuRain Bot框架
"""
import hashlib
import logging
import os
import sys
import requests
import shutil
import time
import random

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")
cache_path = os.path.join(data_path, "cache")


def reboot() -> None:
    # 获取当前解释器路径
    p = sys.executable
    try:
        # 启动新程序(解释器路径, 当前程序)
        os.execl(p, p, *sys.argv)
    except OSError:
        # 关闭当前程序
        sys.exit()


def download_file_to_cache(url: str, headers=None, file_name: str = "", download_path: str = None) -> str | None:
    if headers is None:
        headers = {}

    # 路径拼接
    flag = False
    if file_name == "":
        file_name = url.split("/")[-1] + str(random.randint(10000, 99999)) + str(time.time()) + ".cache"
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
        with open(file_path, "wb") as f, requests.get(url, stream=True, headers=headers) as res:
            for chunk in res.iter_content(chunk_size=64 * 1024):
                if not chunk:
                    break
                f.write(chunk)
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
