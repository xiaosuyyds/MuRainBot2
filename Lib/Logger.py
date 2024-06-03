# coding: utf-8

# Created by BigCookie233

import logging
import logging.handlers as handlers
import os
import sys

import coloredlogs

work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(work_path, "data")
logs_path = os.path.join(work_path, "logs")


def init(logs_path: str = logs_path):
    # 日志颜色
    log_colors = {
        "DEBUG": "white",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    log_field_styles = {
        "asctime": {"color": "green"},
        "hostname": {"color": "magenta"},
        "levelname": {"color": "white"}
    }
    # 日志格式
    fmt = "[%(asctime)s] [%(filename)s] [%(levelname)s]: %(message)s"
    # 设置日志
    coloredlogs.install(isatty=True, stream=sys.stdout, field_styles=log_field_styles, fmt=fmt, colors=log_colors)

    # 设置文件日志
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_name = "latest.log"
    log_path = os.path.join(logs_path, log_name)
    # 如果指定路径不存在，则尝试创建路径
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    def namer(filename):
        dir_name, base_name = os.path.split(filename)
        base_name = base_name.replace(log_name + '.', "")
        rotation_filename = os.path.join(dir_name, base_name)
        return rotation_filename

    file_handler = handlers.TimedRotatingFileHandler(log_path, when="MIDNIGHT", encoding="utf-8")
    file_handler.namer = namer
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(file_handler)
    return logger


logger = init()
