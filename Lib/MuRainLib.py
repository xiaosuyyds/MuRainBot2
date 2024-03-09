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

import logging
import logging.handlers as handlers
import os
import sys

import coloredlogs

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")


def reboot():
    # 获取当前解释器路径
    p = sys.executable
    try:
        # 启动新程序(解释器路径, 当前程序)
        os.execl(p, p, *sys.argv)
    except OSError:
        # 关闭当前程序
        sys.exit()


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
    coloredlogs.install(level='INFO', isatty=True, stream=sys.stdout,
                        field_styles={
                            "asctime": {"color": "green"},
                            "hostname": {"color": "magenta"},
                            "levelname": {"color": "white"}
                        }, fmt=fmt, colors=log_colors_config)

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
