"""
插件管理器
"""

import dataclasses
import importlib
import sys
import traceback

from Lib.constants import *
from Lib.core.EventManager import event_listener
from Lib.core.ListenerServer import EscalationEvent
from Lib.utils.Logger import get_logger

logger = get_logger()

plugins: list[dict] = []
has_main_func_plugins: list[dict] = []

if not os.path.exists(PLUGINS_PATH):
    os.makedirs(PLUGINS_PATH)


class NotEnabledPluginException(Exception):
    """
    插件未启用的异常
    """
    pass


def load_plugins():
    """
    加载插件
    """
    global plugins
    plugins = []
    # 获取插件目录下的所有文件
    for plugin in os.listdir(PLUGINS_PATH):
        if plugin == "__pycache__":
            continue
        full_path = os.path.join(PLUGINS_PATH, plugin)
        try:
            if (
                    os.path.isdir(full_path) and
                    os.path.exists(os.path.join(full_path, "__init__.py")) and
                    os.path.isfile(os.path.join(full_path, "__init__.py"))
            ):
                file_path = os.path.join(os.path.join(full_path, "__init__.py"))
                name = plugin
            elif os.path.isfile(full_path) and full_path.endswith(".py"):
                file_path = full_path
                name = os.path.split(file_path)[1]
            else:
                logger.warning(f"{full_path} 不是一个有效的插件")
                continue
            logger.debug(f"正在加载插件 {file_path}")
            plugin = {"name": name, "plugin": None, "info": None, "file_path": file_path}
            plugins.append(plugin)

            # 创建模块规范
            spec = importlib.util.spec_from_file_location(name, file_path)

            # 创建新模块
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)
            try:
                if callable(module.main):
                    logger.warning(f"插件 {name} 仍在使用 main 函数，main函数已被弃用，请尽快修改")
                    has_main_func_plugins.append({"name": name, "plugin": module})
            except AttributeError:
                pass

            plugin_info = None
            try:
                if isinstance(module.plugin_info, PluginInfo):
                    plugin_info = module.plugin_info
                else:
                    logger.warning(f"插件 {name} 的 plugin_info 并非 PluginInfo 类型，无法获取插件信息")
            except AttributeError:
                logger.warning(f"插件 {name} 未定义 plugin_info 属性，无法获取插件信息")

            plugin["info"] = plugin_info
            plugin["plugin"] = module
            logger.debug(f"插件 {name}({file_path}) 加载成功！")
        except NotEnabledPluginException:
            logger.warning(f"插件 {full_path} 已被禁用，将不会被加载")
            plugins.remove(plugin)
            continue

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()

            logger.error(f"尝试加载插件 {full_path} 时失败！ 原因:{repr(e)}\n"
                         f"{"".join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")

            plugins.remove(plugin)


@dataclasses.dataclass
class PluginInfo:
    """
    插件信息
    """
    NAME: str  # 插件名称
    AUTHOR: str  # 插件作者
    VERSION: str  # 插件版本
    DESCRIPTION: str  # 插件描述
    HELP_MSG: str  # 插件帮助
    ENABLED: bool = True  # 插件是否启用
    IS_HIDDEN: bool = False  # 插件是否隐藏（在/help命令中）

    def __post_init__(self):
        if self.ENABLED is not True:
            raise NotEnabledPluginException


# 该方法已被弃用
def run_plugin_main(event_data):
    """
    运行插件的main函数
    Args:
        event_data: 事件数据
    """
    global has_main_func_plugins
    for plugin in has_main_func_plugins:
        logger.debug(f"执行插件: {plugin['name']}")
        try:
            plugin["plugin"].main(event_data, WORK_PATH)
        except Exception as e:
            logger.error(f"执行插件{plugin['name']}时发生错误: {repr(e)}")
            continue


@event_listener(EscalationEvent)
def run_plugin_main_wrapper(event):
    """
    运行插件的main函数
    Args:
        event: 事件
    """
    run_plugin_main(event.event_data)
