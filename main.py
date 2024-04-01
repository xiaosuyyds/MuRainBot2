# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
# TODO: 适配i18n国际
import atexit
import importlib
import logging
import threading

from flask import Flask, request
from werkzeug.serving import make_server

import Lib.EventManager
from Lib import *

logger = Logger.logger
VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24W13A"  # 版本周

plugins = []  # 插件
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
    data = BotController.Event(request.get_json())
    # 检测是否为重复上报
    logger.debug("收到上报: %s" % data)
    if data in request_list:
        return "ok", 204
    else:
        request_list.append(data)
    if len(request_list) > 100:
        request_list.pop(0)

    if data.post_type + '_type' in data:
        Lib.EventManager.Event((data.post_type, data[data.post_type + '_type']), data)
    else:
        Lib.EventManager.Event(data.post_type, data)

    if data.post_type == "message":
        # 私聊消息
        if data.message_type == 'private':
            message = QQRichText.QQRichText(data['message'])
            if data.sub_type == 'friend':
                logger.info("收到好友 %s(%s) 的消息: %s (%s)" % (
                    data.sender['nick_name'], data.sender['user_id'], str(message), data.message_id)
                            )
            elif data.sub_type == 'group':
                group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
                logger.info("收到来自群 %s(%s) 内 %s(%s) 的临时会话消息: %s (%s)" % (
                    group_name, data.group_id,
                    data.sender['nickname'], data.sender['user_id'],
                    str(message), data.message_id
                )
                            )
            elif data.sub_type == 'other':
                logger.info("收到来自 %s(%s) 的消息: %s (%s)" % (
                    data.sender['nick_name'], data.sender['user_id'], str(message), data.message_id)
                            )

        # 群聊信息
        if data.message_type == 'group':
            user_name = data.sender['nickname']
            if data.sender['card'] != "":
                user_name = data.sender['card']
                # 了群昵称则把用户名设为群昵称
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]

            message = QQRichText.QQRichText(data.message)

            logger.info("收到群 %s(%s) 内 %s(%s) 的消息: %s (%s)" % (
                group_name, data.group_id, user_name, data.sender['user_id'], str(message),
                data.message_id))

            # 获取群文件夹路径
            group_path = os.path.join(data_path, "groups", str(data.group_id))
            # 如果获取群文件夹路径不存在，则创建
            if not os.path.exists(group_path):
                os.makedirs(group_path)

    if data.post_type == 'request':
        # 加好友邀请
        if data.request_type == 'friend':
            logger.info("收到好友 %s(%s) 的加好友邀请" % (data.sender['nickname'], data.sender['user_id']))
        # 加群邀请
        if data.request_type == 'group':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            user_name = api.get("/get_stranger_info", {"user_id": data.user_id})["nickname"]
            if data.sub_type == 'invite':
                logger.info("收到来用户 %s(%s) 加入群%s(%s)的邀请" %
                            (user_name, data.user_id, group_name, data.group_id))
            elif data.sub_type == 'add':
                logger.info("收到来群%s(%s) 内 %s(%s) 加入群的请求" %
                            (group_name, data.group_id, user_name, data.user_id))

    if data.post_type == 'notice':
        if data.notice_type == 'group_upload':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("群%s(%s)内，%s上传了文件：%s" %
                        (group_name, data.group_id, data.user_id, data.file))
        # 戳一戳
        if data.notice_type == 'notify':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("收到群%s(%s)内，%s戳了戳%s" %
                        (group_name, data.group_id, data.user_id, data.target_id))

        # 进群聊
        if data.notice_type == "group_increase":
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("检测到群%s(%s)内，%s进群了，操作者%s" %
                        (group_name, data.group_id, data.user_id, data.operator_id))

        # 退群聊
        if data.notice_type == "group_decrease":
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            user_id = data.user_id
            if data.sub_type == "leave":
                logger.info("检测到%s退出了群聊%s(%s)" % (user_id, group_name, data.group_id))
            elif data.sub_type == "kick":
                logger.info("检测到%s被%s踢出了群聊%s(%s)" % (user_id, data.operator_id, group_name, data.group_id))
            elif data.sub_type == "kick_me" or user_id == bot_uid:
                logger.info("检测到Bot被%s踢出了群聊%s(%s)" % (data.operator_id, group_name, data.group_id))

    # 若插件包含main函数则运行
    for plugin in plugins:
        try:
            if not callable(plugin["plugin"].main):
                continue
        except AttributeError:
            continue

        logger.debug("执行插件%s" % plugin["name"])
        try:
            plugin_thread = threading.Thread(
                target=plugin["plugin"].main,
                args=(
                    data.event_json,
                    work_path)
            )
            plugin_thread.start()
        except Exception as e:
            logger.error("执行插件%s时发生错误：%s" % (plugin["name"], repr(e)))
            continue

    return "ok", 204


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

    bot_uid = Configs.GlobalConfig().user_id
    bot_name = Configs.GlobalConfig().nick_name
    bot_admin = Configs.GlobalConfig().bot_admin

    load_plugins()
    if len(plugins) > 0:
        logger.info("插件导入完成，共成功导入 {} 个插件".format(len(plugins)))
        for plugin in plugins:
            try:
                plugin_info = plugin["plugin"].PluginInfo()
                logger.info("%s: %s 作者:%s" % (plugin["name"], plugin_info.NAME, plugin_info.AUTHOR))
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
        server = make_server(Configs.GlobalConfig().server_host, Configs.GlobalConfig().server_port, app, threaded=True)
        server.serve_forever()
    except Exception as e:
        logger.error("监听服务器启动失败！报错信息：{}".format(repr(e)))
    finally:
        logger.info("监听服务器结束运行！")
