import os
import importlib
import time
import Lib.Logger as Logger
import threading
import Lib.ThreadPool as ThreadPool

logger = Logger.logger

plugins = None
work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
plugins_path = os.path.join(work_path, "plugins")

if not os.path.exists(plugins_path):
    os.makedirs(plugins_path)


def load_plugins():
    global plugins
    # 获取插件目录下的所有文件
    things_in_plugin_dir = os.listdir(plugins_path)

    # 筛选出后缀为.py的文件
    def mapper(name, plugin_suffix=None):
        if plugin_suffix is None:
            plugin_suffix = [".py", ".pyc"]
        for i in plugin_suffix:
            if name.endswith(i):
                return name.split(".")[0]
            else:
                return ""

    things_in_plugin_dir = map(mapper, things_in_plugin_dir)
    things_in_plugin_dir = [_ for _ in things_in_plugin_dir if _ != ""]

    plugins = []

    for i in things_in_plugin_dir:
        try:
            # 导入插件
            t = time.time()
            logger.debug("正在加载插件: {}:".format(i))
            plugins.append({"name": i, "plugin": importlib.import_module('.' + i, package='plugins')})
            logger.debug("插件 {} 加载成功！ 耗时 {}s".format(i, round(time.time() - t, 2)))
        except Exception as e:
            logger.error("导入插件 {} 失败！ 原因:{}".format(i, repr(e)))
    return plugins


class PluginInfo:
    def __init__(self):
        self.NAME = ""  # 插件名称
        self.AUTHOR = ""  # 插件作者
        self.VERSION = ""  # 插件版本
        self.DESCRIPTION = ""  # 插件描述
        self.HELP_MSG = ""  # 插件帮助
        # TODO: self.ENABLED = True  # 插件是否启用
        self.IS_HIDDEN = False  # 插件是否隐藏（在/help命令中）


@ThreadPool.async_task
def run_plugin_main(data):
    for plugin in plugins:
        try:
            if not callable(plugin["plugin"].main):
                continue
        except AttributeError:
            continue

        logger.debug("执行插件%s" % plugin["name"])
        try:
            # plugin_thread = threading.Thread(
            #     target=plugin["plugin"].main,
            #     args=(
            #         data.event_json,
            #         work_path)
            # )
            # plugin_thread.start()
            plugin["plugin"].main(data.event_json, work_path)
        except Exception as e:
            logger.error("执行插件%s时发生错误：%s" % (plugin["name"], repr(e)))
            continue
