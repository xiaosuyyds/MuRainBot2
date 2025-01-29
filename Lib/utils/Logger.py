"""
日志记录器
"""

import logging
import logging.handlers as handlers
import sys
from ..constants import *

import coloredlogs


logger: logging.Logger = None


def init(logs_path: str = LOGS_PATH, logger_level: int = logging.INFO):
    """
    初始化日志记录器
    Args:
        @param logs_path:
        @param logger_level:
    Returns:
        None
    """
    global logger

    if logger is not None:
        return logger
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
    logger = logging.getLogger()

    logger.setLevel(logger_level)
    coloredlogs.set_level(logger_level)

    log_name = "latest.log"
    log_path = os.path.join(logs_path, log_name)
    # 如果指定路径不存在，则尝试创建路径
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    def namer(filename):
        """
        生成文件名
        Args:
            filename: 文件名
        Returns:
            文件名
        """
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


def set_logger_level(level: int):
    """
    设置日志级别
    Args:
        level: 日志级别
    Returns:
        None
    """
    global logger
    logger.setLevel(level)
    coloredlogs.set_level(level)


def get_logger():
    """
    获取日志记录器
    Returns:
        Logger
    """
    if not logger:
        init()
    return logger
