# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
# Code with by Xiaosu & Evan. Copyright (c) 2024 GuppyTEAM. All rights reserved.
# 本代码由校溯 和 XuFuyu编写。版权所有 （c） 2024 Guppy团队。保留所有权利。
"""
MuRainLib
用于MuRain Bot框架
"""

import logging
import logging.handlers as handlers
import os

import coloredlogs

VERSION = "2.0.0-dev"
VERSION_WEEK = "24Y07W"

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")


# MuRainLib信息
class LibInfo:
    def __init__(self):
        self.version = VERSION
        self.version_week = VERSION_WEEK

    def get_version(self):
        return self.version, self.version_week


def log_init():
    # 设置日志颜色
    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    # 日志格式
    fmt = '[%(asctime)s] [%(filename)s] [%(levelname)s]: %(message)s'
    # 设置终端日志
    coloredlogs.install(level='INFO', fmt=fmt, colors=log_colors_config)

    # 设置文件日志
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_name = "today.log"
    log_path = os.path.join(logs_path, log_name)
    # 如果指定路径不存在，则尝试创建路径
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    file_handler = handlers.TimedRotatingFileHandler(
        log_path,
        when="MIDNIGHT",
        encoding='utf-8'
    )

    def namer(filename):
        dir_name, base_name = os.path.split(filename)
        base_name = base_name.replace(log_name + '.', "")
        rotation_filename = os.path.join(dir_name, base_name)
        return rotation_filename

    file_handler.namer = namer
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    print("这是一个Lib库，为其他程序提供一些方法，函数。")
    print("不可直接运行！")
    input("Enter或按Ctrl+C以退出")
    exit(0)
