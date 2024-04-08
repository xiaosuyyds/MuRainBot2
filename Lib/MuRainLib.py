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
import os
import sys
import requests
import time
import random

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")
cache_path = os.path.join(data_path, "cache")


def reboot():
    # 获取当前解释器路径
    p = sys.executable
    try:
        # 启动新程序(解释器路径, 当前程序)
        os.execl(p, p, *sys.argv)
    except OSError:
        # 关闭当前程序
        sys.exit()


def download_file_to_cache(url: str, headers=None):
    if headers is None:
        headers = {}

    # 路径拼接
    file_name = url.split("/")[-1]+str(random.randint(10000, 99999))+str(time.time())+".cache"
    file_path = os.path.join(cache_path, file_name)

    # 路径不存在特判
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    # 下载
    with open(file_path, "wb") as f:
        f.write(requests.get(url, stream=True, headers=headers).content)

    # 计算MD5
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        rename = md5_hash.hexdigest()+".cache"
        rename_path = os.path.join(cache_path, rename)

    # 重命名（MD5）
    if not os.path.exists(rename_path):
        os.rename(file_path, rename_path)
    else:
        os.remove(file_path)

    return rename_path
