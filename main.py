# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
import Lib.EventManager
from Lib import *
from flask import Flask, request
import yaml
import os
import logging
import threading
import importlib
import atexit
from werkzeug.serving import make_server

logger = MuRainLib.log_init()
VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24W11A"  # 版本周

plugins = {}  # 插件
app = Flask(__name__)

api = OnebotAPI.OnebotAPI()

request_list = []


# 结束运行
@atexit.register
def finalize_and_cleanup():
    # TODO: 清理缓存文件等
    logger.warning("MuRainBot结束运行！\n")


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    logger.debug(data)
    if data in request_list:
        return "OK"
    else:
        request_list.append(data)

    type_ = data['post_type']
    if type_ + '_type' in data:
        Lib.EventManager.Event((type_, data[type_ + '_type']), data)
    else:
        Lib.EventManager.Event(type_, data)

    if data['post_type'] == "message" and data['message_type'] == 'group':  # 如果是群聊信息
        username = data['sender']['nickname']  # 获取信息发送者的昵称
        if data['sender']['card'] != "":
            username = data['sender']['card']  # 若用户设置
            # 了群昵称则把用户名设为群昵称
        group_name = api.get("/get_group_info", {"group_id": data['group_id']})["group_name"]

        message = QQRichText.cq_decode(data['raw_message'])

        logger.info("收到群 %s(%s) 内 %s(%s) 的消息: %s (%s)" % (
            group_name, data['group_id'], username, data['sender']['user_id'], message,
            data['message_id']))

        # 获取群文件夹路径
        group_path = os.path.join(data_path, "groups", str(data['group_id']))
        # 如果获取群文件夹路径不存在，则创建
        if not os.path.exists(group_path):
            os.makedirs(group_path)

        # 加群邀请
        if data['post_type'] == 'request' and data['request_type'] == 'group':
            logger.info("收到来自%s的加群邀请, 群号%s, flag:%s, 类型: %s" %
                        (data['user_id'], data['group_id'], data['flag'], data['sub_type']))

        # 戳一戳
        if data['post_type'] == "notice" and data['notice_type'] == 'notify':
            logger.info("检测到群号为%s内，%s戳了戳%s" %
                        (data['group_id'], data['user_id'], data['target_id']))

        # 进群聊
        if data['post_type'] == "notice" and data['notice_type'] == "group_increase":
            logger.info("检测到群号为%s内，%s进群了，操作者%s" %
                        (data['group_id'], data['user_id'], data['operator_id']))

        # 退群聊
        if data['post_type'] == "notice" and data['notice_type'] == "group_decrease":
            type_ = data['sub_type']
            oid = data['operator_id']
            group_id = data['group_id']
            user_id = data['user_id']
            if type_ == "leave":
                logger.info("检测到%s退出了群聊%s" % (user_id, group_id))
            elif type_ == "kick":
                logger.info("检测到%s被%s踢出了群聊%s" % (user_id, oid, group_id))
            elif type_ == "kick_me" or user_id == bot_uid:
                logger.info("检测到Bot被%s踢出了群聊%s" % (oid, group_id))

    # 插件
    # TODO: 插件异步执行，替换多线程
    for plugin in plugins.keys():
        plugin_thread = threading.Thread(
            target=plugins[plugin].main,
            args=(
                data,
                work_path)
        )
        plugin_thread.start()

    return "OK"


# 导入配置文件
def load_config(yml_path):
    try:
        with open(yml_path, encoding="utf-8") as f:
            file_content = f.read()
        config = yaml.load(file_content, yaml.FullLoader)
        # print(content)
        logger.info("配置文件加载成功！")
        return config
    except FileNotFoundError or OSError:
        logger.critical('配置文件加载失败！')
        return None


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

    plugins = {}

    for i in things_in_plugin_dir:
        try:
            plugins[i] = importlib.import_module('.' + i, package='plugins')
        except Exception as e:
            logger.error("导入插件 {} 失败！ 原因:{}".format(i, e))
    return plugins


# 主函数
if __name__ == '__main__':
    work_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(work_path, 'data')
    yaml_path = os.path.join(work_path, 'config.yml')
    plugins_path = os.path.join(work_path, "plugins")

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

    config = load_config(yaml_path)

    bot_uid = config["account"]["user_id"]
    bot_name = config["account"]["nick_name"]
    bot_admin = config["account"]["bot_admin"]

    load_plugins()
    if len(plugins) > 0:
        logger.info("插件导入完成，共成功导入 {} 个插件".format(len(plugins)))
        for plugin in plugins:
            plugin_info = plugins[plugin].PluginInfo(config)
            logger.info("%s 作者:%s", plugin_info.NAME, plugin_info.AUTHOR)
    else:
        logger.warning("无插件成功导入！")

    logger.info("读取到监听服务器ip，将以此ip启动监听服务器: {}:{}"
                .format(config["server"]["host"], config["server"]["port"]))

    # 设置API
    api.set_ip(config["api"]["host"], config["api"]["port"])

    logger.info("读取到监听api，将以此url调用API: {}"
                .format(str(api)))

    # 检测bot名称与botUID是否为空或未设置
    if bot_uid is None or bot_name == "" or bot_uid == 123456 or bot_name is None:
        logger.warning("配置文件中未找到BotUID或昵称，将自动获取！")
        try:
            bot_info = api.get("/get_login_info")
            bot_uid, bot_name = bot_info["user_id"], bot_info["nickname"]
        except (TypeError, ConnectionRefusedError):
            logger.error("获取BotUID与昵称失败！可能会导致严重问题！")

    logger.info("欢迎使用 {}({})".format(bot_name, bot_uid))

    # 禁用werkzeug的日志记录
    log = logging.getLogger('werkzeug')
    log.disabled = True

    # 启动监听服务器
    try:
        logger.info("启动监听服务器")
        server = make_server(config["server"]["host"], config["server"]["port"], app)
        server.serve_forever()
    except:
        logger.error("监听服务器启动失败！")
    finally:
        logger.info("监听服务器结束运行！")
