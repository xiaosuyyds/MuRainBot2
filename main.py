# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
# TODO: 适配i18n国际化
import atexit
import importlib
import shutil

from Lib import *

logger = Logger.logger
VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24W13A"  # 版本周

plugins = []  # 插件

api = OnebotAPI.OnebotAPI()

request_list = []

work_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(work_path, 'data')
yaml_path = os.path.join(work_path, 'config.yml')
plugins_path = os.path.join(work_path, "plugins")
cache_path = os.path.join(data_path, "cache")

if not os.path.exists(data_path):
    os.makedirs(data_path)

if not os.path.exists(plugins_path):
    os.makedirs(plugins_path)

if not os.path.exists(cache_path):
    os.makedirs(cache_path)


# 结束运行
@atexit.register
def finalize_and_cleanup():
    logger.info("MuRainBot即将关闭，正在删除缓存")

    MuRainLib.clean_cache()

    logger.warning("MuRainBot结束运行！\n")


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
            logger.debug("正在加载插件: {}:".format(i))
            plugins.append({"name": i, "plugin": importlib.import_module('.' + i, package='plugins')})
            logger.debug("插件 {} 加载成功！".format(i))
        except Exception as e:
            logger.error("导入插件 {} 失败！ 原因:{}".format(i, repr(e)))
    return plugins


# 主函数
if __name__ == '__main__':
    logger.info(f"MuRain Bot开始运行，当前版本：{VERSION}({VERSION_WEEK})")
    logger.info("Github: https://github.com/xiaosuyyds/MuRainBot2/")

    # 版本检测
    if LibInfo().version == VERSION:
        logger.info("MuRainLib版本校验成功！")
    else:
        logger.warning("MuRainLib版本检测未通过，可能会发生异常\n"
                       f"MuRainLib版本:{LibInfo().version} MuRain Bot版本:{VERSION}\n"
                       "注意：我们将不会受理在此模式下运行的报错")
        if input("Continue?(Y/n)").lower() != "y":
            sys.exit()
        logger.warning("MuRainLib版本检测未通过，可能会发生异常，将继续运行！")

    logger.info("MuRainLib当前版本：{}({})".format(LibInfo().version, LibInfo().version_week))

    bot_uid = Configs.GlobalConfig().user_id
    bot_name = Configs.GlobalConfig().nick_name
    bot_admin = Configs.GlobalConfig().bot_admin

    load_plugins()
    if len(plugins) > 0:
        logger.info("插件导入完成，共成功导入 {} 个插件:".format(len(plugins)))
        for plugin in plugins:
            try:
                plugin_info = plugin["plugin"].PluginInfo()
                logger.info(" - %s: %s 作者:%s" % (plugin["name"], plugin_info.NAME, plugin_info.AUTHOR))
            except ArithmeticError:
                logger.warning("插件{} 没有信息".format(plugin["name"]))
            except Exception as e:
                logger.warning("插件{} 信息获取失败: {}".format(plugin["name"], repr(e)))
    else:
        logger.warning("无插件成功导入！")

    logger.info("读取到监听服务器ip，将以此ip启动监听服务器: {}:{}"
                .format(Configs.GlobalConfig().server_host, Configs.GlobalConfig().server_port))

    # 设置API
    api.set_ip(Configs.GlobalConfig().api_host, Configs.GlobalConfig().api_port)

    logger.info("读取到监听api，将以此url调用API: {}"
                .format(str(api)))

    # 检测bot名称与botUID是否为空或未设置
    if bot_uid is None or bot_name == "" or bot_uid == 123456 or bot_name is None:
        logger.warning("配置文件中未找到BotUID或昵称，将自动获取！")
        try:
            bot_info = api.get("/get_login_info")
            bot_uid, bot_name = bot_info["user_id"], bot_info["nickname"]
            raw_config = Configs.GlobalConfig().raw_config
            raw_config["account"]["user_id"] = bot_uid
            raw_config["account"]["nick_name"] = bot_name
            Configs.GlobalConfig().write_cache(raw_config)
            logger.debug("已成功获取BotUID与昵称！")
        except Exception as e:
            logger.error("获取BotUID与昵称失败！可能会导致严重问题！报错信息：{}".format(repr(e)))

    logger.info("欢迎使用 {}({})".format(Configs.GlobalConfig().nick_name, Configs.GlobalConfig().user_id))

    # 禁用werkzeug的日志记录
    log = logging.getLogger('werkzeug')
    log.disabled = True

    # 启动监听服务器
    try:
        logger.info("启动监听服务器")
        ListeningServer.server.serve_forever()
    except Exception as e:
        logger.error("监听服务器启动失败！报错信息：{}".format(repr(e)))
    finally:
        logger.info("监听服务器结束运行！")


