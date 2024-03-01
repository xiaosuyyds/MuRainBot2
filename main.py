# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

from Lib import MuRainLib
from Lib import OnebotAPI
from Lib import QQRichText
from flask import Flask, request
import yaml
import os
import logging
import threading
import importlib
from werkzeug.serving import make_server

logger = MuRainLib.log_init()
VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24Y07W"  # 版本周

plugins = {}  # 插件
app = Flask(__name__)

api = OnebotAPI.OnebotAPI()

request_list = []


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data in request_list:
        return "OK"
    else:
        request_list.append(data)
    # TODO: 上报事件处理，写一个事件(上报)的class

    if data['post_type'] == "message":
        if data['message_type'] == 'group':  # 如果是群聊信息
            group_id = data['group_id']  # 获取群号
            user_id = data['sender']['user_id']  # 获取信息发送者的 QQ号码
            username = data['sender']['nickname']  # 获取信息发送者的昵称
            message = data['raw_message']  # 获取原始信息
            msg_id = data['message_id']  # 获取信息ID
            group_user_name = data['sender']['card']  # 获取信息发送者的群昵称
            if group_user_name != "":
                username = group_user_name  # 若用户设置
                # 了群昵称则把用户名设为群昵称
            group_name = api.get("/get_group_info", {"group_id": group_id})["group_name"]

            message = QQRichText.cq_decode(message)

            logger.info("收到群 %s(%s) 内 %s(%s) 的消息: %s (%s)" % (
                group_name, group_id, username, user_id, message.replace("\n", ""), msg_id))

            # 获取组文件路径
            grou_path = os.path.join(data_path, "groups", str(group_id))
            # 如果组文件路径不存在，则创建
            if not os.path.exists(grou_path):
                os.makedirs(grou_path)

        # 加群邀请
        if data['post_type'] == 'request':
            if data['request_type'] == 'group':
                user_id = data['user_id']
                group_id = data['group_id']
                type_ = data['sub_type']
                flag = data['flag']
                if type_ == "invite":
                    logger.info("收到来自%s的加群邀请，群号是%s已默认同意(flag:%s)" % (user_id, group_id, flag))

        # 戳一戳
        if data['post_type'] == "notice":
            if data['notice_type'] == 'notify':
                user_id = data['user_id']
                tid = data['target_id']
                group_id = data['group_id']
                logger.info("检测到群号为%s内，%s戳了戳%s" % (group_id, user_id, tid))

        # 进群聊
        if data['post_type'] == "notice":
            if data['notice_type'] == "group_increase":
                oid = data['operator_id']
                user_id = data['user_id']
                group_id = data['group_id']
                logger.info("检测到群号为%s内，%s进群了，操作者%s" % (group_id, user_id, oid))

        # 退群聊
        if data['post_type'] == "notice":
            if data['notice_type'] == "group_decrease":
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

    # TODO: 异步执行

    # 插件
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
def import_config(yml_path):
    try:
        with open(yml_path, encoding="utf-8") as f:
            file_content = f.read()
        config = yaml.load(file_content, yaml.FullLoader)
        # print(content)
        logger.info("配置文件导入成功！")
        return config
    except FileNotFoundError or OSError:
        logger.critical('配置文件导入失败！')
        return None


def import_plugins():
    global plugins
    # 获取插件目录下的所有文件
    things_in_plugin_dir = os.listdir(plugins_path)

    # 筛选出后缀为.py的文件
    def pick_module(name, plugin_suffix=".py"):
        if name.endswith(plugin_suffix):
            return name.split(".")[0]
        else:
            return ""

    things_in_plugin_dir = map(pick_module, things_in_plugin_dir)
    things_in_plugin_dir = [_ for _ in things_in_plugin_dir if _ != ""]

    plugins = {}

    for i in things_in_plugin_dir:
        try:
            plugins[i] = importlib.import_module('.' + i, package='plugins')
        except Exception as e:
            logger.warning("导入插件 {} 失败！ 原因:{}".format(i, e))
    return plugins


# 主函数
if __name__ == '__main__':
    pass
else:
    logger.warning("您当前正在使用非常规手段运行MuRain Bot，这可能会造成严重的错误！\n"
                   "注意：我们将不会受理在此模式下运行的报错")

work_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(work_path, 'data')
yaml_path = os.path.join(work_path, 'config.yml')
plugins_path = os.path.join(work_path, "plugins")

logger.info(f"MuRain Bot开始运行，当前版本：{VERSION}")
logger.info("Github: https://github.com/xiaosuyyds/MuRainBot2/")


# 版本检测
if MuRainLib.LibInfo().version == VERSION:
    logger.info("MuRainLib版本校验成功！")
else:
    logger.warning("MuRainLib版本检测未通过，可能会发生异常\n"
                   f"MuRainLib版本:{MuRainLib.LibInfo().version} MuRain Bot版本:{VERSION}\n"
                   "注意：我们将不会受理在此模式下运行的报错")
    os.system("pause")
    logger.warning("MuRainLib版本检测未通过，可能会发生异常，将继续运行！")

config = import_config(yaml_path)

bot_uid = config["account"]["user_id"]
bot_name = config["account"]["nick_name"]
bot_admin = config["account"]["bot_admin"]

import_plugins()
if len(plugins) > 0:
    logger.info("插件导入完成，共成功导入 {} 个插件".format(len(plugins)))
    for plugin in plugins:
        plugin_info = plugins[plugin].PluginInfo(config)
        logger.info("%s 作者:%s", plugin_info.NAME, plugin_info.AUTHOR)
else:
    logger.warning("无插件成功导入！")

logger.info("读取到监听服务器ip，将以此ip启动监听服务器:{}:{}"
            .format(config["server"]["host"], config["server"]["port"]))

api.set_ip(config["api"]["host"], config["api"]["port"])

logger.info("读取到监听api，将以此url调用API:{}"
            .format(str(api)))

# 启动监听服务器
server = make_server(config["server"]["host"], config["server"]["port"], app)
logger.info("启动监听服务器")
# 禁用werkzeug的日志记录
log = logging.getLogger('werkzeug')
log.disabled = True
server.serve_forever()

logger.warning("监听服务器结束运行！")
logger.warning("MuRain Bot运行结束！")
